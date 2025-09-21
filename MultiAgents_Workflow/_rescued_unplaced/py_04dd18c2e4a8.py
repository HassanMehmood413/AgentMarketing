from langchain_tavily import TavilySearch
from langchain_community.document_loaders import WikipediaLoader
from typing import Any, Dict, List, Optional, Union
import re
import json
from pydantic import BaseModel,Field
from prompt.search_instructions import search_instructions
from llm.llm import chat
from dotenv import load_dotenv

load_dotenv()


# ---- Pydantic model for the parser (kept as in your code) ----
class SearchQuery(BaseModel):
    search_query: str = Field(None, description="Search query for retrieval")


# ---- Helpers ----
def _strip_code_fences(s: str) -> str:
    """Remove leading/trailing Markdown code fences like ```json ... ```."""
    if not isinstance(s, str):
        return s
    s = s.strip()
    if s.startswith("```"):
        # remove starting fence e.g. ```json or ```
        s = re.sub(r"^```[a-zA-Z0-9]*\s*", "", s, flags=re.DOTALL)
    if s.endswith("```"):
        s = s[: s.rfind("```")].strip()
    return s.strip()


def _extract_json_object(s: str) -> Optional[dict]:
    """
    Try to extract the first top-level JSON object from a string.
    Returns dict if successful, else None.
    """
    s = _strip_code_fences(s)
    # find first {...} block
    start = s.find("{")
    end = s.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(s[start : end + 1])
        except Exception:
            return None
    return None


def extract_first_n_words(text, n=80) -> str:
    return " ".join(str(text).split()[:n])


def handle_parsing_error(raw_response, default_message="Failed to retrieve search results.") -> Dict[str, List[str]]:
    """Return the first ~80 words of model output (or a default message) as context."""
    content = getattr(raw_response, "content", None)
    if isinstance(content, str) and content.strip():
        return {"context": [extract_first_n_words(content)]}
    return {"context": [default_message]}


def _format_tavily_results(search_docs: Union[str, List[Any]]) -> str:
    """
    TavilySearch.invoke(...) can return a string or a list of dict/Document.
    Make this tolerant.
    """
    if isinstance(search_docs, str):
        return search_docs

    formatted_chunks: List[str] = []
    for doc in search_docs:
        # dict-like (common case for TavilySearchResults)
        if isinstance(doc, dict):
            url = doc.get("url") or doc.get("source") or ""
            content = doc.get("content") or doc.get("snippet") or doc.get("text") or ""
            formatted_chunks.append(f'<Document href="{url}"/>\n{content}\n</Document>')
        # LangChain Document
        elif hasattr(doc, "metadata") and hasattr(doc, "page_content"):
            url = doc.metadata.get("source") or doc.metadata.get("url") or ""
            content = getattr(doc, "page_content", "")
            formatted_chunks.append(f'<Document href="{url}"/>\n{content}\n</Document>')
        else:
            # fallback stringify
            formatted_chunks.append(str(doc))

    return "\n\n---\n\n".join(formatted_chunks)


# ---- Fixed web search ----
def search_web(state: Any) -> Dict[str, List[str]]:
    """Retrieve docs from web search (Tavily) with robust parsing and formatting."""
    tavily_search = TavilySearch(max_results=5)  # reads TAVILY_API_KEY from env

    raw_response = chat.invoke([search_instructions] + state["messages"])

    if not getattr(raw_response, "content", ""):
        return {"context": [state.get("topic", "No topic found")]}

    # 1) Try strict Pydantic first
    try:
        # Attempt to parse raw JSON (after stripping fences) into our model
        obj = _extract_json_object(raw_response.content)
        if obj is None:
            raise ValueError("No JSON object found in model output.")
        parsed = SearchQuery(**obj)
        search_q = (parsed.search_query or "").strip()
        if not search_q:
            raise ValueError("Empty search_query.")

        # 2) Call Tavily
        search_docs = tavily_search.invoke(search_q)

        # 3) Format safely
        formatted_search_docs = _format_tavily_results(search_docs)
        return {"context": [formatted_search_docs]}

    except Exception as e:
        print(f"Error while parsing or fetching docs: {e}")
        return handle_parsing_error(raw_response, default_message=state.get("topic", "No topic found"))


# ---- Fixed Wikipedia search ----
def search_wikipedia(state: Any) -> Dict[str, List[str]]:
    """Retrieve docs from Wikipedia with robust parsing and formatting."""
    raw_response = chat.invoke([search_instructions] + state["messages"])

    if not getattr(raw_response, "content", ""):
        return {"context": [state.get("topic", "No topic found")]}

    try:
        obj = _extract_json_object(raw_response.content)
        if obj is None:
            raise ValueError("No JSON object found in model output.")
        parsed = SearchQuery(**obj)
        search_q = (parsed.search_query or "").strip()
        if not search_q:
            raise ValueError("Empty search_query.")

        search_docs = WikipediaLoader(query=search_q, load_max_docs=5).load()

        formatted_search_docs = "\n\n---\n\n".join(
            [
                f'<Document source="{getattr(doc, "metadata", {}).get("source", "")}" '
                f'title="{getattr(doc, "metadata", {}).get("title", "")}"/>\n'
                f'{getattr(doc, "page_content", str(doc))}\n</Document>'
                for doc in search_docs
            ]
        )

        return {"context": [formatted_search_docs]}

    except Exception as e:
        print(f"Error while parsing or fetching docs: {e}")
        return handle_parsing_error(raw_response, default_message=state.get("topic", "No topic found"))


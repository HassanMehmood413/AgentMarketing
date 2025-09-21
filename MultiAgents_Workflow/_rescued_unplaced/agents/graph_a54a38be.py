from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from langchain_core.messages import HumanMessage
from schemas.research_schema import ResearchState
from utils.research import generate_questions
from utils.questions import search_web, search_wikipedia
from utils.answer import generate_answer, save_interview, route_messages
from utils.writer import write_section
from dotenv import load_dotenv
import os,sys

load_dotenv()




# Add nodes and edges
interview_builder: StateGraph = StateGraph(ResearchState)
interview_builder.add_node("ask_question", generate_questions)
interview_builder.add_node("search_web", search_web)
interview_builder.add_node("search_wikipedia", search_wikipedia)
interview_builder.add_node("answer_question", generate_answer)
interview_builder.add_node("save_interview", save_interview)
interview_builder.add_node("write_section", write_section)

# Flow
interview_builder.add_edge(START, "ask_question")
interview_builder.add_edge("ask_question", "search_web")
interview_builder.add_edge("ask_question", "search_wikipedia")
interview_builder.add_edge("search_web", "answer_question")
interview_builder.add_edge("search_wikipedia", "answer_question")
interview_builder.add_conditional_edges("answer_question", route_messages,['ask_question','save_interview'])
interview_builder.add_edge("save_interview", "write_section")
interview_builder.add_edge("write_section", END)

async def conduct_all_interviews(state):
    """Conduct interviews with all analysts and collect their sections."""
    analysts = state.get("analysts", [])
    topic = state.get("topic", "Unknown topic")

    print(f"[conduct_all_interviews] Starting interviews for {len(analysts)} analysts on topic: {topic}", file=sys.stderr)

    all_sections = []

    for i, analyst in enumerate(analysts):
        print(f"[conduct_all_interviews] Interviewing analyst {i+1}/{len(analysts)}: {analyst.name}", file=sys.stderr)

        # Create interview state for this analyst
        interview_state = {
            "analyst": analyst,
            "messages": [HumanMessage(content=f"So you said you were writing an article on {topic}?")],
            "max_num_turns": 2,
            "context": [],
            "interview": "",
            "sections": []
        }

        # Run the interview subgraph for this analyst
        memory = MemorySaver()
        interview_graph = interview_builder.compile(checkpointer=memory)

        config = {"configurable": {"thread_id": f"interview-{analyst.name}-{topic.replace(' ', '-')[:30]}" }}

        try:
            result = await interview_graph.ainvoke(interview_state, config)
            if result and "sections" in result and result["sections"]:
                all_sections.extend(result["sections"])
                print(f"[conduct_all_interviews] Analyst {analyst.name} produced {len(result['sections'])} sections", file=sys.stderr)
            else:
                print(f"[conduct_all_interviews] Analyst {analyst.name} produced no sections", file=sys.stderr)
        except Exception as e:
            print(f"[conduct_all_interviews] Error interviewing {analyst.name}: {e}", file=sys.stderr)

    print(f"[conduct_all_interviews] Completed all interviews. Total sections: {len(all_sections)}", file=sys.stderr)
    return {"sections": all_sections}

# Replace the compiled subgraph with our custom function
conduct_all_interviews_node = conduct_all_interviews
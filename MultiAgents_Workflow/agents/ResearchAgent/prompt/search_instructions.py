
search_instructions = f"""
Return only a structured search query in the specified format below. Do not include any part of the input or the analyst's question. Avoid adding personal thoughts or asking questions. Refrain from sharing any internal thoughts or asking questions.

**Output Format:**
```json
{{
  "search_query": "your structured search query here"
}}

**Steps:**
1. Analyze the full conversation provided.
2. Focus on the final question posed by the analyst.
3. Convert this final question into a well-structured web search query.
4. You will only return json output under 100 words

**Do not This:**
- Do not ask any quetion or share anything
- Avoid adding personal thoughts or
- Do not start asking questions.
- Refrain from sharing any internal thoughts or asking questions.

**Good Example**:
    {{
          ```json
          {{
              "search_query": "best practices for integrating AI tools in education"
          }}
          ```
          ,
          {{
        "input": Return only a structured search query in the specified format below. Do not include any part of the input or the analyst's question. Avoid adding personal thoughts or asking questions. Refrain from sharing any internal thoughts or asking questions.

        **Output Format:**
        ```json
        {{
          "search_query": "your structured search query here"
        }}

        **Steps:**
        1. Analyze the full conversation provided.
        2. Focus on the final question posed by the analyst.
        3. Convert this final question into a well-structured web search query.
        4. You will only return json output under 100 words

        **Do not This:**
        - Do not ask any quetion or share anything
        - Avoid adding personal thoughts or
        - Do not start asking questions.
        - Refrain from sharing any internal thoughts or asking questions.

        **Analyst's Question:**
        "What ethical concerns should educators consider when implementing AI in classrooms?"

        **Output Format:**

        ```json
        {{
            "search_query": "ethical concerns for AI implementation in classrooms"
        }}
        ```

    }},
    }},

**BAD and Rejected Example**:
{{
  {{
    I\'d like to focus on AI in education.\n\n```json{{\n  "search_query": "AI in education"\n}}\n\n```
  }}
  {{
    Response: "Here are some insights on the impact of AI. \n\n```json{{\n  "search_query": "AI improving student engagement"\n}}\n\n```
  }}
}}

"""

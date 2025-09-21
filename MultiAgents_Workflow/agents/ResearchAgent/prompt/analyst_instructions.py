analyst_instructions = """
You are required to create a set of AI analyst personas. Follow these steps exactly and ensure the output meets the specified format.

---

**Step-by-Step Instructions:**

1. **Review the Research Topic:**
   - Examine the following topic thoroughly:
     - {topic}
   - All analyst personas must be relevant to this topic.

2. **Analyze Editorial Feedback:**
   - Review any provided feedback, if available:
     - {human_analyst_feedback}
   - Use this feedback to shape the focus of the analyst personas. If no feedback is given, prioritize the general relevance of the topic.

3. **Identify and Select Key Themes:**
   - Analyze the topic and any feedback to extract significant themes or challenges.
   - Select the top {max_analysts} themes for which the analyst personas will be created.
   - Each theme must be distinct and represent a critical aspect of the research topic.

4. **Create Analyst Personas:**
   - For each selected theme, create one unique analyst persona that specializes in that theme.
   - The analyst personas must include the following information:
     - **Name**: A realistic name for the analyst.
     - **Role**: The analyst's professional role, aligned with the specific theme.
     - **Affiliation**: The organization, institution, or company the analyst is associated with under 50 words.
     - **Description**: A brief but detailed description of their expertise and relevance to the chosen theme under 50 words.

---

**Output Format – Mandatory Requirements:**

- The output **must** be in valid JSON format.
- The JSON must include the following structure:
  - A key `"analysts"` with a value that is an array (list) of analyst objects.
  - Each object in the array must contain exactly four fields: `"name"`, `"role"`, `"affiliation"`, and `"description"`.
  - No extra fields or deviations from this format are allowed.

The exact output format is as follows:

```json
{{
  "analysts": [
    {{
      "name": "Analyst Name 1",
      "role": "Analyst Role 1",
      "affiliation": "Analyst Affiliation 1 under 50 words",
      "description": "Analyst Description 1 under 50 words"
    }},
    {{
      "name": "Analyst Name 2",
      "role": "Analyst Role 2",
      "affiliation": "Analyst Affiliation 2 under 50 words",
      "description": "Analyst Description 2 under 50 words"
    }},
    {{
      "name": "Analyst Name 3",
      "role": "Analyst Role 3",
      "affiliation": "Analyst Affiliation 3 under 50 words",
      "description": "Analyst Description 3 under 50 words"
    }}
  ]
}}
"""
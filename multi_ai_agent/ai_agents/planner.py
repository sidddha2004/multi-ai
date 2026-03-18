from ai_agents.llm import get_gemini_model
import json
import re


def create_plan(message):

    model = get_gemini_model()

    prompt = f"""
You are an AI planning system.

Convert the user request into execution steps.

Available agents:
- task_agent
- calendar_agent
- reminder_agent

Return ONLY valid JSON.

Format:

[
  {{"agent":"calendar_agent","task":"Meeting tomorrow"}},
  {{"agent":"reminder_agent","task":"Prepare slides"}}
]

User request:
{message}
"""

    result = model.invoke(prompt)

    content = result.content

    try:
        return json.loads(content)

    except:
        # extract JSON if model adds text
        match = re.search(r"\[.*\]", content, re.DOTALL)

        if match:
            try:
                return json.loads(match.group())
            except:
                pass

    return [{"agent": "task_agent", "task": message}]
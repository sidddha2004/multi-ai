from ai_agents.llm import get_gemini_model
from ai_agents.agents import get_reminder_agent,get_calender_agent,get_task_agent

def get_supervisor():
    model = get_gemini_model()

    task_agent = get_task_agent()
    calendar_agent = get_calender_agent()
    reminder_agent = get_reminder_agent()

    def route(message):

        msg = message.lower()

        if "task" in msg:
                return task_agent

        if "meeting" in msg or "schedule" in msg:
                return calendar_agent

        if "remind" in msg or "reminder" in msg:
                return reminder_agent
        return task_agent
    
    return route

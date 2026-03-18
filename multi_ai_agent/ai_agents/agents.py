from langchain.agents import create_agent
from ai_agents.tools import document_tools
from ai_agents.llm import get_gemini_model

def get_task_agent(model=None,checkpointer=None):
    llm = get_gemini_model(model)

    return create_agent(
        model=llm,
        tools=document_tools,
        system_prompt="You manage user tasks such as creating, listing, or updating tasks.",
        name="task agent",
        checkpointer=checkpointer
    )

def get_calender_agent(model=None,checkpointer=None):
    llm = get_gemini_model(model)

    return create_agent(
        model=llm,
        tools=document_tools,
        system_prompt="You manage calendar events like scheduling meetings.",
        name="task agent",
        checkpointer=checkpointer
    )

def get_reminder_agent(model=None,checkpointer=None):
    llm = get_gemini_model(model)

    return create_agent(
        model=llm,
        tools=document_tools,
        system_prompt="You manage reminders and notifications for users.",
        name="task agent",
        checkpointer=checkpointer
    )



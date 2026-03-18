from langgraph.graph import StateGraph,END
from typing import TypedDict
from ai_agents.llm import get_gemini_model
from langgraph.checkpoint.memory import MemorySaver
from ai_agents.agents import get_calender_agent,get_reminder_agent,get_task_agent
from ai_agents.planner import create_plan

memory = MemorySaver();
#for storing conversation states 
class AgentState(TypedDict):
    message:str
    agent:str
    user_id:str

def supervisor(state):

    plan = create_plan(state["message"])

    msg = state["message"].lower()

    if "task" in msg:
        return {"agent": "task"}

    if "meeting" in msg or "schedule" in msg:
        return {"agent": "calendar"}

    if "remind" in msg:
        return {"agent": "reminder"}

    return {"agent": "task"}

def task_node(state):

    agent = get_task_agent()

    result = agent.invoke(
    {
        "messages":[("user", state["message"])]
    },
    config={
        "configurable":{
            "user_id": state["user_id"]
        }
    }
)

    return {"message": result}

def calendar_node(state):

    agent = get_calender_agent()

    result = agent.invoke(
    {
        "messages":[("user", state["message"])]
    },
    config={
        "configurable":{
            "user_id": state["user_id"]
        }
    }
)

    return {"message": result}

def reminder_node(state):

    agent = get_reminder_agent()

    result = agent.invoke(
    {
        "messages":[("user", state["message"])]
    },
    config={
        "configurable":{
            "user_id": state["user_id"]
        }
    }
)

    return {"message": result}


def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor)
    graph.add_node("task", task_node)
    graph.add_node("calendar", calendar_node)
    graph.add_node("reminder", reminder_node)

    graph.set_entry_point("supervisor")

    graph.add_conditional_edges(
        "supervisor",
        lambda x: x["agent"],
        {
            "task": "task",
            "calendar": "calendar",
            "reminder": "reminder"
        }
    )

    graph.add_edge("task", END)
    graph.add_edge("calendar", END)
    graph.add_edge("reminder", END)

    return graph.compile(checkpointer=memory)
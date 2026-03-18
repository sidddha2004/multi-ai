from ai_agents.tools import (
    create_task,
    create_event,
    create_reminder,
    list_tasks
)

TOOL_REGISTRY = {
    "create_task": create_task,
    "create_event": create_event,
    "create_reminder": create_reminder,
    "list_tasks": list_tasks,
}
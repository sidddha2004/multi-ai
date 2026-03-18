from langchain.tools import tool
from langchain_core.runnables import RunnableConfig
from django.contrib.auth.models import User
from productivity.models import CalendarEvent, Reminder, Task
from django.utils import timezone


@tool
def create_task(title: str, description: str = "", config: RunnableConfig = None):
    """Create a task for the current user."""

    user_id = config["configurable"]["user_id"]
    user = User.objects.get(id=user_id)

    task = Task.objects.create(
        user=user,
        title=title,
        description=description
    )

    return f"Task '{task.title}' created successfully."


@tool
def list_tasks(config: RunnableConfig = None):
    """List all tasks for the current user."""

    user_id = config["configurable"]["user_id"]

    tasks = Task.objects.filter(user_id=user_id)

    if not tasks.exists():
        return "No tasks found."

    return "\n".join([t.title for t in tasks])


@tool
def create_event(title: str, config: RunnableConfig = None):
    """Create a calendar event."""

    user_id = config["configurable"]["user_id"]
    user = User.objects.get(id=user_id)

    event = CalendarEvent.objects.create(
        user=user,
        title=title,
        start_time=timezone.now(),
        end_time=timezone.now()
    )

    return f"Event '{event.title}' scheduled."


@tool
def create_reminder(message: str, config: RunnableConfig = None):
    """Create a reminder for the current user."""

    user_id = config["configurable"]["user_id"]
    user = User.objects.get(id=user_id)

    reminder = Reminder.objects.create(
        user=user,
        message=message,
        remind_at=timezone.now()
    )

    return f"Reminder created: {message}"


document_tools = [
    create_task,
    list_tasks,
    create_event,
    create_reminder
]
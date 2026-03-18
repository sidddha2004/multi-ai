from ai_agents.tool_registry import TOOL_REGISTRY


def execute_plan(plan, user_id):

    results = []

    for step in plan:

        agent = step["agent"]
        task = step["task"]

        if agent == "task_agent":
            tool = TOOL_REGISTRY["create_task"]

            args = {"title": task}

        elif agent == "calendar_agent":
            tool = TOOL_REGISTRY["create_event"]

            args = {"title": task}

        elif agent == "reminder_agent":
            tool = TOOL_REGISTRY["create_reminder"]

            args = {"message": task}

        else:
            continue

        result = tool.invoke(
            args,
            config={"configurable": {"user_id": user_id}}
        )

        results.append(result)

    return results
from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ai_agents.graph import build_graph
from ai_agents.executor import execute_plan
from ai_agents.planner import create_plan

from productivity.models import Conversation,Message
# Create your views here.
app = build_graph()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def chat_agent(request):

    message = request.data.get("message")
    user = request.user

    conversation, _ = Conversation.objects.get_or_create(user=user)

    Message.objects.create(
        conversation=conversation,
        role="user",
        content=message
    )

    plan = create_plan(message)

    results = execute_plan(plan, user.id)

    response = " ".join(results)

    Message.objects.create(
        conversation=conversation,
        role="assistant",
        content=response
    )

    return Response({
        "response": response,
        "plan": plan
    })

from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({"error": "Username and password required"}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken"}, status=400)
    user = User.objects.create_user(username=username, password=password)
    return Response({"message": "Account created successfully"})
from django.urls import path
from.views import chat_agent,signup


urlpatterns = [
    path("chat/", chat_agent),
    path("signup/", signup),
]

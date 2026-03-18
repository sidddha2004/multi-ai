from langchain_google_genai import ChatGoogleGenerativeAI
from django.conf import settings

def get_gemini_model(model=None):
    if model is None:
        model = "gemini-2.5-flash"
    return ChatGoogleGenerativeAI(
        model=model,
        temperature=0,
        google_api_key=settings.GOOGLE_API_KEY,
    )

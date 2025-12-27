import os
from langchain_google_genai import ChatGoogleGenerativeAI


def get_gemini_llm(
    model: str = "gemini-2.5-flash",
    temperature: float = 0.2,
):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY not set")

    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=api_key,
        temperature=temperature,
        max_output_tokens=1024,
    )

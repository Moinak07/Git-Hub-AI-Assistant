import sys
sys.path.append("C:/Users/rohit/OneDrive/Desktop/AI Assistant/langchain_framework") 

from langchain_google_genai import ChatGoogleGenerativeAI
from config import GEMINI_API_KEY, GEMINI_MODEL

def get_llm():
    """Initialize LangChain LLM with the Gemini API."""
    return ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0.2, google_api_key=GEMINI_API_KEY)

if __name__ == "__main__":
    llm = get_llm()
    print("LangChain Gemini model initialized successfully!")

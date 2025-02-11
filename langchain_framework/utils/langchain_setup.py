import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Retrieve the path from environment variables
project_path = os.getenv("PROJECT_PATH")

if project_path:
    sys.path.append(project_path)
else:
    print("Warning: PROJECT_PATH is not set in the .env file.")

from langchain_google_genai import ChatGoogleGenerativeAI
from config import GEMINI_API_KEY, GEMINI_MODEL



def get_llm():
    """Initialize LangChain LLM with the Gemini API."""
    return ChatGoogleGenerativeAI(model=GEMINI_MODEL, temperature=0.2, google_api_key=GEMINI_API_KEY)

if __name__ == "__main__":
    llm = get_llm()
    print("LangChain Gemini model initialized successfully!")

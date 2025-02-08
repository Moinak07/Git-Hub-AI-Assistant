import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-pro"
genai.configure(api_key=GEMINI_API_KEY)


GENERATION_CONFIG = {
    'temperature': 0  
}
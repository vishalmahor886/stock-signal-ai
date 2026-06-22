from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()

def gemini_model():
    model = GoogleGenerativeAI(
        model_name="gemini-1.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    return model
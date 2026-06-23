from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()

def gemini_model():
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.2
    )
    return model
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

def groq_model1():

    model = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.1
    )
    return model


def groq_model2():
    model=ChatGroq(
            model="openai/gpt-oss-120b",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.
    )
    return model
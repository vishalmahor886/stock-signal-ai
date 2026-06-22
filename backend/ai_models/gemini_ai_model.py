from langchain_google_genai import GoogleGenerativeAI

def gemini_model():
    model = GoogleGenerativeAI(
        model = "gemini-1.5-pro",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        max_new_tokens=1024,
        temperature=0.2,
    )
    return model
        
    
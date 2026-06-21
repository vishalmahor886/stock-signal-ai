from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

import os
from dotenv import load_dotenv
load_dotenv()

def technical_llm():
    llm = HuggingFaceEndpoint(
        repo_id="Vansh180/FinBERT-India-v1", 
        task="text-generation",
        huggingfacehub_api_token=os.getenv("HF_ACCESS_TOKEN"), 
        max_new_tokens=256,
        temperature=0.1
    )

    model = ChatHuggingFace(llm=llm)
    return model

def agentic_llm():
    llm = HuggingFaceEndpoint(
        repo_id="openai/gpt-oss-120b",  
        task="text-generation",
        huggingfacehub_api_token=os.getenv("HF_ACCESS_TOKEN"), 
        max_new_tokens=1024,
        temperature=0.2,
    )
    return ChatHuggingFace(llm=llm)

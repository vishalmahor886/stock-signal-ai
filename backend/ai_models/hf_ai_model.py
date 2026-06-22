from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace

import os
from dotenv import load_dotenv
load_dotenv()

def agentic_llm():
    llm = HuggingFaceEndpoint(
        repo_id="openai/gpt-oss-120b",  
        task="text-generation",
        huggingfacehub_api_token=os.getenv("HF_ACCESS_TOKEN"), 
        max_new_tokens=4096,
        temperature=0.2,
    )
    return ChatHuggingFace(llm=llm)

def agentic_llm2():
    llm = HuggingFaceEndpoint(
        repo_id="deepseek-ai/DeepSeek-V4-Flash",  
        task="text-generation",
        huggingfacehub_api_token=os.getenv("HF_ACCESS_TOKEN"), 
        max_new_tokens=4096,
        temperature=0.2,
    )
    return ChatHuggingFace(llm=llm)

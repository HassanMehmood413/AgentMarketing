from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv


load_dotenv()


chat = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

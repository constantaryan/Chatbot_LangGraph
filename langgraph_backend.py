from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_mistralai import ChatMistralAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

load_dotenv()



llm = ChatMistralAI(
    model="mistral-small",  
    temperature=0.7
)

response = llm.invoke("Explain LangChain in simple words")
print(response.content)
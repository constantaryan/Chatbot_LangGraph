from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_mistralai import ChatMistralAI
# from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3

load_dotenv()

llm = ChatMistralAI(
    model="mistral-small",  
    temperature=0.7
)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages': [response]}

conn = sqlite3.connect(database='chatbot.db', check_same_thread=False) # if database exist nhi krta hoga tho create ho jayega
# check_same_thread se hum ek databse ko  multiple thread m access krr skte h but bydefault sqlite humko sirf 1 thread m kaam krne deta h
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)


response = chatbot.invoke({'messages':[HumanMessage(content= 'what is my name?')]}, config = {'configurable':{'thread_id':'thread-2'}})

print(response)

# for message_chunk, metadata in stream:
#     if message_chunk.content:
#         print(message_chunk.content, end = " ", flush = True)

# print(type(stream))
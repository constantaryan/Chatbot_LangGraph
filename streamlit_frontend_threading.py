import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import BaseMessage, HumanMessage
import uuid # it will be used to generate random thread_id

# ---------------------------------------------------------------------------------
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    # we are doing these series of steps for new chat
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_history(st.session_state['thread_id']) # jb bhi new chat banegi tho wo thread_id history m add ho jayegi
    st.session_state['message_history']  = []

def add_history(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    return chatbot.get_state(config={'configurable': {'thread_id':thread_id}}).values['messages']

# ---------------------------------------------------------------------------------

# problem is ki abhi hum conversation ko save nhi krr paa rhe 
# we can use dictionary to story messages of every user & assistant instance
# {'role': 'user', 'content': 'Hi'},
# {'role': 'assistant', 'content': 'How can i help you'}
# message_history = []
# rather than simple dictionary jo refresh bec streamlit hamesa puri script ko chalta h jb bhi koi nya input aata h 
# we will use st.session_state
# ---------------------------------------------------------------------------------
# SESSION SETUP 

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

# creating history of chats
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

add_history(st.session_state['thread_id'])

CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}




# ---------------------------------------------------------------------------------

# abb is list m dictionary jayengi in the form of
# {'role': 'user', 'content': 'Hi'},
# {'role': 'assistant', 'content': 'How can i help you'}
# ---------------------------------------------------------------------------------
st.sidebar.title('LangGraph Chatbot')
if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id) # this will give us list of dictionary  of all messages of that thread_id,[{'role': 'user', 'content': 'Hi'}]

        temp_messages = []

        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'

            temp_messages.append({'role': role, 'content': message.content})

        st.session_state['message_history'] = temp_messages
# ---------------------------------------------------------------------------------

# we are looping to all the messages till now and showing everytime streamlit script runs
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input = st.chat_input("Type Here")

if user_input:

    st.session_state['message_history'].append({'role': 'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)


    # response = chatbot.invoke({'messages':[HumanMessage(content = user_input)]}, config= CONFIG) 
    # ai_message = response['messages'][-1].content   

    
    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            # we need a generator for the write_stream function
            # jo humko stream krna h wo h message_chunk ka content 
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages':[HumanMessage(content = user_input)]},
                config = CONFIG,
                stream_mode= 'messages'
            )
        )
    st.session_state['message_history'].append({'role': 'assistant','content':ai_message})

        
# it will give us an object of a generator
# for message_chunk, metadata in  chatbot.stream(
#     {'messages':[HumanMessage(content = 'What is the recipe of momos?')]}, # this is the initial state
#     config = {'configurable':{'thread_id': 'thread-1'}},
#     stream_mode= 'messages'
# ):
#     if message_chunk.content:
#         print(message_chunk.content, end = " ", flush = True)










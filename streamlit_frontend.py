import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import BaseMessage, HumanMessage


CONFIG = {'configurable': {'thread_id':'thread-1'}}
# problem is ki abhi hum conversation ko save nhi krr paa rhe 
# we can use dictionary to story messages of every user & assistant instance
# {'role': 'user', 'content': 'Hi'},
# {'role': 'assistant', 'content': 'How can i help you'}
# message_history = []
# rather than simple dictionary jo refresh bec streamlit hamesa puri script ko chalta h jb bhi koi nya input aata h 
# we will use st.session_state
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# abb is list m dictionary jayengi in the form of
# {'role': 'user', 'content': 'Hi'},
# {'role': 'assistant', 'content': 'How can i help you'}

# we are looping to all the messages till now and showing everytime streamlit script runs
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])


user_input = st.chat_input("Type Here")

if user_input:

    st.session_state['message_history'].append({'role': 'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    response = chatbot.invoke({'messages':[HumanMessage(content = user_input)]}, config= CONFIG) 
    ai_message = response['messages'][-1].content   

    st.session_state['message_history'].append({'role': 'assistant','content':ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)









# with st.chat_message('user'):
#     st.text('Hi')


# with st.chat_message('assistant'):
#     st.text('Hi')

# inputval = st.chat_input('Type here')

# if inputval:
#     with st.chat_message('user'):
#         st.text(inputval)
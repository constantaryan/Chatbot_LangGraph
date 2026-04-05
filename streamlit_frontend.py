import streamlit as st

# problem is ki abhi hum conversation ko save nhi krr paa rhe 
# we can use dictionary to story messages of every user & assistant instance
# {'role': 'user', 'content': 'Hi'},
# {'role': 'assistant', 'content': 'How can i help you'}
message_history = []


user_input = st.chat_input("Type Here")

if user_input:

    message_history.append({'role': 'user','content':'user_input'})
    with st.chat_message('user'):
        st.text(user_input)

    message_history.append({'role': 'assistant','content':'user_input'})
    with st.chat_message('assistant'):
        st.text(user_input)









# with st.chat_message('user'):
#     st.text('Hi')


# with st.chat_message('assistant'):
#     st.text('Hi')

# inputval = st.chat_input('Type here')

# if inputval:
#     with st.chat_message('user'):
#         st.text(inputval)
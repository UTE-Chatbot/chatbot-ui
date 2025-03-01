import streamlit as st
import random
import time
from core import generate_answer
# Streamed response emulator
def response_generator(question):
    return generate_answer(question)

st.set_page_config(page_title='HCMUTE-Chat', layout='wide', page_icon='../images/icon_1.png')

st.image('../images/icon_2.png')
st.title('TRỢ LÍ ẢO HỖ TRỢ TUYỂN SINH')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#Show chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Viết câu hỏi của bạn ở đây?"):
    #Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    #Show user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    #Show assistant response in chat message container
    with st.chat_message("assistant"):
        response_container = st.empty()  
        full_response = ""  
        for word in response_generator(prompt):
            full_response += word
            response_container.markdown(full_response)  
        response = full_response.strip()  

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

with st.expander('Liên hệ với chúng tôi'):
    with st.form(key='contact', clear_on_submit=True):
        email = st.text_input('Email liên hệ của bạn')
        text = st.text_area('Nội dung', '')
        submit_button = st.form_submit_button(label='Gửi thông tin')
        if submit_button:
            with open(f'contacts/{email}.txt', 'wb') as file:
                file.write(text.encode('utf-8'))
            st.success('Thông tin đã được gửi!')

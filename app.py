import streamlit as st
from utils.app_utils import *

st.set_page_config(
    page_title="My Car",
    layout="wide"
)

st.markdown('''
    <h1>
        &nbsp<img src = 'app/static/vw.png' width = "50"> 
        &nbsp &nbsp 
        My Volkswagen
    </h1>
    ''', unsafe_allow_html=True)

input_string = st.chat_input("Type a message")

if 'setup' not in st.session_state.keys():
    st.session_state["setup"] = 1

    with st.chat_message("assistant"):
        render_message(message= '''
        Hi, I am your personal vehicle assistant ! 
        How may I help you today?''', 
        smooth=True)

if input_string:
    with st.chat_message("human"):
        render_message(message = input_string, smooth=False)
    
    with st.spinner("Processing your command"):
        reply = process_command(input_string)

    with st.chat_message("assistant"):
        render_message(message= reply, smooth=True)
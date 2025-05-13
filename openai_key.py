import streamlit as st
from dotenv import load_dotenv
import os

def get_openai_key():
    if 'use_openai_env' not in st.session_state:
        st.session_state.use_openai_env = True
    
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = "sk-None-gcnsj4WayQdIGKQ0retQT3BlbkFJSzW0nXnO0Apd1Xm4cypX"
        
    if st.session_state.use_openai_env:
        load_dotenv()
        openai_api_key = os.getenv('OPENAI_API_KEY')
        if not openai_api_key:
            st.error("Error: OpenAI API key not set in environment.")
            st.write("> Please put your OpenAI API key in the .env file or enter the key manually.")
            st.stop()
        else:
            st.session_state.openai_api_key = openai_api_key
    else:
        openai_api_key = st.text_input("OpenAI API ključ", type="password", value=st.session_state.openai_api_key)
        if not openai_api_key:
            st.write("> However, before proceeding, please enter your OpenAI API key. If you don't have it, you can get it at [OpenAI](https://platform.openai.com/signup).")
            st.error("Error: I don't have an OpenAI API key.")
            st.stop()
        else:
            st.session_state.openai_api_key = openai_api_key
    
    os.environ['OPENAI_API_KEY'] = st.session_state.openai_api_key
    return st.session_state.openai_api_key

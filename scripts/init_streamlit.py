import streamlit as st


def init_streamlit():
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
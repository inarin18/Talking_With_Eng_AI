import streamlit as st


def init_streamlit():
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
        

# 会話履歴をチャット形式で表示
def show_conversation():
        
        for message in st.session_state.conversation_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
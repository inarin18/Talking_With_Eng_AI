import streamlit as st

from .prompt import INSTRUCTION


def init_streamlit():
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
        
        # gpt への指示を履歴に追加
        st.session_state.conversation_history.append(
            {
                "role": "system", 
                "content": INSTRUCTION
            }
        )
        

# 会話履歴をチャット形式で表示
def show_conversation():
        
        for message in st.session_state.conversation_history[1:]:
            with st.chat_message(message["role"]):
                st.write(message["content"])
""" 
Date : 2023-12-30

Author : Hinata Inaoka

Description : 
    This is a main file of this project.

"""

import os
import streamlit as st

from openai import OpenAI


from scripts.utils_streamlit import (
    init_streamlit, 
    show_conversation, 
    change_mic_state_to_disabled
)

from scripts.widget_handler import (
    locate_input_widget,
    handle_user_input,
    handle_gpt_response,
)


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def main():
    
    if st.session_state.curr_state == "initializing":
        
        # 会話履歴の初期化等を行う．
        init_streamlit()
        
        st.title("English Conversation with GPT")
        
        # チャット形式で会話履歴の表示
        show_conversation()
        
        locate_input_widget()
    
    elif st.session_state.curr_state == "speech_2_text":
        handle_user_input()
    
    elif st.session_state.curr_state == "gpt_response":
        handle_gpt_response()
    
    st.session_state.curr_state = "waiting_for_sound_response"
    
    
    # gpt の回答を音声化して再生
    # text_2_speech(
    #     text  = gpt_response,
    #     model = "tts-1",
    #     voice = "alloy"
    # )
    
    # 現在の状態を初期化
    st.session_state.curr_state ="initializing"
    
    st.rerun()


if __name__ == "__main__":
    main() 
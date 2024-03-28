""" 
Date : 2023-12-30

Author : Hinata Inaoka

Description : 
    This is a main file of this project.

"""

import os
import queue
import streamlit as st

from openai import OpenAI


from scripts import utils_streamlit
from scripts import widget_handler
from scripts import t2s


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def main():
    
    # 会話履歴の初期化等を行う．
    utils_streamlit.init_streamlit()
    
    st.title("English Conversation with GPT")
    
    # チャット形式で会話履歴の表示
    widget_handler.show_conversation()
    
    # 録音開始ボタンをサイドバーに配置
    widget_handler.locate_input_widget()

    # ユーザの入力処理
    widget_handler.handle_user_input()
    
    # ユーザの入力を処理できていれば，gpt の回答を表示
    if st.session_state.user_sentence is not None:
        
        widget_handler.handle_gpt_response(
            gpt_model = "gpt-3.5-turbo-0125"
        )
        
        # gpt の回答を音声化して再生
        t2s.text_2_speech(
            text  = st.session_state.gpt_response,
            model = "tts-1",
            voice = "alloy"
        )
        
        # ユーザの入力を初期化
        st.session_state.user_sentence = None
    
    # 現在の状態を初期化
    st.session_state.curr_state ="initializing"
    
    st.rerun()


if __name__ == "__main__":
    main() 
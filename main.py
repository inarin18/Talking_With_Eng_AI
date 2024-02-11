""" 
Date : 2023-12-30

Author : Hinata Inaoka

Description : 
    This is a main file of this project.

"""

import os
import streamlit as st

from openai import OpenAI

from scripts.s2t_google_recognition import realtime_textise
from scripts.s2t_whisper import speech_2_text
from scripts.gpt import generate_gpt_response 
from scripts.t2s import text_2_speech
from scripts.utils_streamlit import init_streamlit, show_conversation


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def dummy():
    return "dummy"


def main():
    
    RECORD_SECONDS          = 5
    MAX_CONVERSATION_LENGTH = 2
    
    # 会話履歴の初期化等を行う．
    init_streamlit()
    
    st.title("English Conversation with GPT")
    
    st.warning("The History of the conversation will be banished in case you raload.")
    
    # チャット形式で会話履歴の表示
    show_conversation()
    
    prompt = st.chat_input("Say something")
        
    # ユーザーの発言を取得
    user_sentence = speech_2_text(RECORD_SECONDS)
    
    # streamlit 画面にユーザの発言を表示
    with st.chat_message("user"):
        st.write(user_sentence)
    
    # user の発言を履歴に追加
    st.session_state.conversation_history.append(
        {
            "role": "user", 
            "content": user_sentence
        }
    )

    # ユーザの発言から gpt による回答を取得
    gpt_response  = generate_gpt_response(
        conversation_history = st.session_state.conversation_history,  
        gpt_model            = "gpt-3.5-turbo"
    )
    
    # gpt の回答を streamlit 画面に表示
    with st.chat_message("assistant"):
        st.write(gpt_response)
    
    # gpt の回答を履歴に追加
    st.session_state.conversation_history.append(
        {
            "role": "assistant", 
            "content": gpt_response
        }
    )
    
    # gpt の回答を音声化して再生
    # text_2_speech(
    #     text  = gpt_response,
    #     model = "tts-1",
    #     voice = "alloy"
    # )
        
    for conversation in st.session_state.conversation_history:
        print(conversation["content"])
        
    st.button("Next Conversation")


if __name__ == "__main__":
    main() 
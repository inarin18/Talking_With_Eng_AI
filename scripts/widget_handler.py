
import streamlit as st

from scripts.s2t_google_recognition import realtime_textise
from scripts.s2t_whisper import speech_2_text
from scripts.gpt import generate_gpt_response 
from scripts.t2s import text_2_speech

from scripts.utils_streamlit import (
    init_streamlit, 
    show_conversation, 
    change_mic_state_to_disabled
)



def locate_input_widget() :
    
    # 録音開始ボタンの配置
    with st.sidebar:
        st.button(
            label    = "Recording Start 🎤",
            key      = "mic",
            type     = "secondary",
            disabled = st.session_state.mic_disabled,
            on_click = change_mic_state_to_disabled,
            args     = (True, )
        )
    
    # テキスト入力欄を配置しておく
    st.chat_input("Say something", key="prompt")



def handle_user_input() :
    
    # ユーザーの発言を取得
    # 録音でもよいし，テキスト入力でもよい
    if   st.session_state.mic : 
        st.session_state.user_sentence = speech_2_text()
        
    elif st.session_state.prompt is not None   : 
        st.session_state.user_sentence = st.session_state.prompt
        
    else : 
        st.stop()
    
    # streamlit 画面にユーザの発言を表示
    with st.chat_message("user"):
        st.write(st.session_state.user_sentence)
    
    # user の発言を履歴に追加
    st.session_state.conversation_history.append(
        {
            "role": "user", 
            "content": st.session_state.user_sentence
        }
    )
    

def handle_gpt_response(gpt_model :str = "gpt-3.5-turbo"):
    
    # ユーザの発言から gpt による回答を取得
    st.session_state.gpt_response  = generate_gpt_response(
        conversation_history = st.session_state.conversation_history,  
        gpt_model            = gpt_model
    )
    
    # gpt の回答を streamlit 画面に表示
    with st.chat_message("assistant"):
        st.write(st.session_state.gpt_response)
    
    # gpt の回答を履歴に追加
    st.session_state.conversation_history.append(
        {
            "role": "assistant", 
            "content": st.session_state.gpt_response
        }
    )
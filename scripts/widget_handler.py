
import streamlit as st
import threading

from scripts.s2t_google_recognition import realtime_textise
from scripts.s2t_whisper import speech_2_text
from scripts.gpt import generate_gpt_response 
from scripts.t2s import text_2_speech

from scripts.utils_streamlit import (
    change_mic_state_to_disabled,
    change_recording_state_to_true
)


# 会話履歴をチャット形式で表示
def show_conversation():
    
    # システムの発言は表示しない
    for message in st.session_state.conversation_history[1:]:
        with st.chat_message(message["role"]):
            st.write(message["content"])



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
        
        st.button(
            label    = "Recording Stop 🎤",
            key      = f"mic_stop",
            on_click = change_recording_state_to_true
        )



def handle_user_input() :
    
    # 長いので省略している（念のため getter のときのみ使用）
    ss = st.session_state
    
    # テキスト入力欄を配置しておく
    prompt = st.chat_input("You can also type your message here")
    
    # 単なる要約変数
    is_valid_recording    = ss.mic and not ss.is_locked_recording_thread
    is_finished_recording = ss.is_stop_recording and ss.is_locked_recording_thread
    
    # ユーザーの発言を取得，録音でもよいし，テキスト入力でもよい
    if  is_valid_recording : 
        
        # 録音中，再度録音ができないようにスレッドをロックする
        st.session_state.is_locked_recording_thread = True
        
        # スレッドをスタート
        thread = threading.Thread(target=speech_2_text, args=(st.session_state.result_queue, ))
        thread.start()
        
    elif is_finished_recording :
        
        # スレッドの解放
        st.session_state.is_locked_recording_thread = False
        
        # 別スレッドの処理終了後に，ユーザの発言を取得
        st.session_state.user_sentence = st.session_state.result_queue.get()
        
        st.write(f"in is_finished_recording : {st.session_state.user_sentence}")
        
    elif prompt is not None   : 
        st.session_state.user_sentence = prompt
    else : 
        st.stop()
    
    
    # 入力が存在したらその入力を表示
    if st.session_state.user_sentence is not None:
        
        # streamlit 画面にユーザの発言を表示
        with st.chat_message("user"):
            st.write(ss.user_sentence)
        
        # user の発言を履歴に追加
        st.session_state.conversation_history.append(
            {
                "role": "user", 
                "content": ss.user_sentence
            }
        ) 
        
        # 録音停止フラグを初期化
        st.session_state.is_stop_recording = False
    

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
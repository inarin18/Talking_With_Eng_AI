import queue
import streamlit as st

from .prompt import INSTRUCTION


def init_streamlit():
    
    if "result_queue" not in st.session_state:
        
        # 非同期処理とした処理の結果を格納するキュー
        st.session_state.result_queue = queue.Queue()
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
        
        # gpt への指示を履歴に追加
        st.session_state.conversation_history.append(
            {
                "role": "system", 
                "content": INSTRUCTION
            }
        )
    
    if "mic_disabled" not in st.session_state:
        st.session_state.mic_disabled = False
        
    if "is_locked_recording_thread" not in st.session_state:
        st.session_state.is_locked_recording_thread = False
        
    if "is_stop_recording" not in st.session_state:
        st.session_state.is_stop_recording = False
        
    if "user_sentence" not in st.session_state:
        st.session_state.user_sentence = None
        
    if "gpt_response" not in st.session_state:
        st.session_state.gpt_response = None


# コールバック関数として用いることが多い
def change_mic_state_to_disabled(disabled :bool = True):
    
    st.session_state.mic_disabled = disabled
    

def change_recording_state_to_true():
    
    # 録音終了時に録音スキップフラグを立てる
    # st.session_state.is_skip_recording  = True
    
    # 録音停止ボタンを制御するためのフラグを立てる
    st.session_state.is_stop_recording  = True
    
    # 録音中のフラグを立てる
    # st.session_state.is_still_recording = True
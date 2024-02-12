import streamlit as st

from .prompt import INSTRUCTION


# curr_state :
# "init"
# "waiting_for_user_input"
# "in_speech_2_text"
# "waiting_for_gpt_response"
# "waiting_for_sound_response"


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
    
    if "mic_disabled" not in st.session_state:
        st.session_state.mic_disabled = False
        
    if "is_skip_record" not in st.session_state:
        st.session_state.is_skip_record = False
        
    if "prompt" not in st.session_state:
        st.session_state.prompt = None
        
    if "user_sentence" not in st.session_state:
        st.session_state.user_sentence = None
        
    if "gpt_response" not in st.session_state:
        st.session_state.gpt_response = None
        
        

# 会話履歴をチャット形式で表示
def show_conversation():
    
    # システムの発言は表示しない
    for message in st.session_state.conversation_history[1:]:
        with st.chat_message(message["role"]):
            st.write(message["content"])


# コールバック関数として用いることが多い
def change_mic_state_to_disabled(disabled :bool = True):
    
    st.session_state.mic_disabled = disabled
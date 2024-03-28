
import time
import os
import wave
import pyaudio

import streamlit as st

from pathlib import Path
from openai import OpenAI

from .modules.audio_parameter import (
    CHUNK              ,
    FORMAT             ,
    SAMPLE_RATE        ,
    CHANNELS           ,
    INPUT_DEVICE_INDEX ,
    CALL_BACK_FREQUENCY,
)

from .utils_streamlit import (
    change_mic_state_to_disabled, 
    change_recording_state_to_true
)

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

# ファイルのパス
OUTPUT_TXT_FILE = Path(__file__).parent.parent / "data" / "user_speech.txt"
AUDIO_FILE_PATH = Path(__file__).parent.parent / "sounds" / "output.wav"



def record_audio():
    
    with wave.open('sounds/output.wav', 'wb') as wf:
        
        p = pyaudio.PyAudio()
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(SAMPLE_RATE)

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, input=True)

        print('Recording...')
        
        # 録音停止ボタンを配置しておく
        with st.sidebar:
            st.button(
                label    = "Recording Stop 🎤",
                key      = f"mic_stop",
                on_click = change_recording_state_to_true
            ) 
    
        while not st.session_state.is_stop_recording:
            
            # stream から読み込み出力ファイルに書き込み
            in_data = stream.read(CHUNK)
            wf.writeframes(in_data)
                
        print('Done')

        stream.close()
        p.terminate()


# 音声を文字起こしする
def speech_2_text():

    # 録音停止ボタンを押した際にリロードされて録音が二重にされてしまう問題を
    # 回避するために，録音操作をスキップするフラグにより処理を分岐
    if not st.session_state.is_skip_recording :
        record_audio()
    
    audio_file = open(AUDIO_FILE_PATH, "rb")
    transcript = client.audio.transcriptions.create(
        model           = "whisper-1", 
        file            = audio_file,
        language        = "en",
        response_format = "text"
    )
    
    # 音声を文字起こししたのち，ボタンを able に
    change_mic_state_to_disabled(disabled=False)
    
    # 録音関連のフラグを初期化
    st.session_state.is_stop_recording  = False
    st.session_state.is_skip_recording  = False
    st.session_state.is_still_recording = False
    
    return transcript


def main():
    speech_2_text()


if __name__ == '__main__':
    main()
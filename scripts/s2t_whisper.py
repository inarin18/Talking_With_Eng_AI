
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
        
        placeholder = st.empty()
    
        key_suffix  = 0
        while True:
            
            # stream から読み込み出力ファイルに書き込み
            in_data = stream.read(CHUNK)
            wf.writeframes(in_data)

            # ここからは消す予定 ## ## ##
            # サイドバーに録音停止ボタンを配置
            # with stop_button_placeholder.container():
                
            #     is_stop = st.button(
            #         label    = "Recording Stop 🎤",
            #         key      = f"mic_stop_{key_suffix}",
            #         on_click = change_recording_state_to_true
            #     ) 
            
            if st.session_state.is_stop_recording : break
            
            placeholder.write(f"Recording... {key_suffix}")
            ## ## ## ここまで ## ## ## 
            
            # 複製禁止エラーが出るのを防ぐために key_suffix の更新
            key_suffix += 1
            
            # ボタン生成を抑えるために 1 秒待機（消去予定）
            # time.sleep(1)
                
        print('Done')

        stream.close()
        p.terminate()


# 音声を文字起こしする
def speech_2_text():
    
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
    
    return transcript


def main():
    speech_2_text()


if __name__ == '__main__':
    main()
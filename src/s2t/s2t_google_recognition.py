""" speech-to-text """
import os
import time
import sys

from pathlib import Path

import speech_recognition as sr
import pyaudio

from ..modules.concat_stream_data import concat_part_of_sentence

from ..modules.audio_parameter import (
    FORMAT             ,
    SAMPLE_RATE        ,
    CHANNELS           ,
    INPUT_DEVICE_INDEX ,
    CALL_BACK_FREQUENCY,
)


__ALL__ = [
    'look_for_audio_input',
    'realtime_textise'
]


# 以下 import 時に実行されるコード

# ストリームデータを格納するリスト
global stream_data 

# アウトプットファイルのパス
OUTPUT_TXT_FILE = Path(__file__).parent.parent / "data" / "user_speech.txt"


# コールバック関数の定義
def callback(in_data, frame_count, time_info, status):

    stream_data.append(in_data)

    return (None, pyaudio.paContinue)


# リアルタイムで音声を文字起こしする
def realtime_textise():

    # speech recogniserインスタンスを生成
    global sprec
    sprec = sr.Recognizer() 
    
    global stream_data
    stream_data = []
    
    # Audio インスタンス取得
    audio  = pyaudio.PyAudio() 
    
    # ストリームオブジェクトを作成
    stream = audio.open(
        format             = FORMAT,
        rate               = SAMPLE_RATE,
        channels           = CHANNELS,
        input_device_index = INPUT_DEVICE_INDEX,
        input              = True, 
        frames_per_buffer  = SAMPLE_RATE*CALL_BACK_FREQUENCY, # CALL_BACK_FREQUENCY 秒周期でコールバック
        stream_callback    = callback
    )
    
    stream.start_stream()
    
    # 終了判定をとりあえず 10秒 で行う
    i = 0
    while stream.is_active() and i < 1000:
        
        time.sleep(0.01)
        i += 1
        
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # recognizerを作成
    sprec = sr.Recognizer() 

    # チャンクごとに音声を文字起こしして連結後取得
    user_sentence = concat_part_of_sentence(stream_data)
    
    # ファイルの末尾に追記していく
    with open(OUTPUT_TXT_FILE, 'a') as f: 
        f.write("\n" + user_sentence)


def main():
    realtime_textise()


if __name__ == '__main__':
    main()

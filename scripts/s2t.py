""" speech-to-text """
import os
import time
import sys

from pathlib import Path

import speech_recognition as sr
import pyaudio


__ALL__ = [
    'look_for_audio_input',
    'realtime_textise'
]


# 以下 import 時に実行されるコード


global stream_data 


# PyAudio に用いるパラメータ
FORMAT              = pyaudio.paInt16
SAMPLE_RATE         = 44100    # サンプリングレート
CHANNELS            = 1        # モノラルかバイラルか
INPUT_DEVICE_INDEX  = 0        # マイクのチャンネル
CALL_BACK_FREQUENCY = 3        # コールバック呼び出しの周期[sec]

# アウトプットファイルのパス
OUTPUT_TXT_FILE = Path(__file__).parent.parent / "data" / "user_speech.txt"


# コールバック関数の定義
def callback(in_data, frame_count, time_info, status):

    stream_data.append(in_data)

    return (None, pyaudio.paContinue)


def show_speech(in_data):
    
    try :
        audiodata  = sr.AudioData(in_data, SAMPLE_RATE, 2)
        sprec_text = sprec.recognize_google(audiodata, language='eng')
        print("Your Speech : " + sprec_text)
        
    except sr.UnknownValueError as e:
        print(e)
    
    except sr.RequestError as e:
        print(e)
    
    finally:
        pass


# リアルタイムで音声を文字起こしする
def realtime_textise():

    global sprec # speech_recognitionオブジェクトを毎回作成するのではなく、使いまわすために、グローバル変数で定義しておく
    
    # speech recogniserインスタンスを生成
    sprec = sr.Recognizer() 
    
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
        stream_callback    = None
    )
    
    stream.start_stream()
    
    i = 0
    while stream.is_active() and i < 1000:
        
        time.sleep(0.01)
        i += 1
        print("\r" + str(i), end="")
        
    sprec = sr.Recognizer() 

    for in_data in stream_data:
        show_speech(in_data)
    
    stream.stop_stream()
    stream.close()
    audio.terminate()


def main():
    realtime_textise()


if __name__ == '__main__':
    main()

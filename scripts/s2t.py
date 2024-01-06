""" speech-to-text """
import os, sys

# バッファリングの解除
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)
sys.stdin  = os.fdopen(sys.stdin.fileno(),  'r', buffering=1)

from pathlib import Path

import speech_recognition as sr
import time

import pyaudio

FORMAT        = pyaudio.paInt16
SAMPLE_RATE   = 44100        # サンプリングレート
CHANNELS      = 1            # モノラルかバイラルか

INPUT_DEVICE_INDEX  = 0      # マイクのチャンネル
CALL_BACK_FREQUENCY = 2      # コールバック呼び出しの周期[sec]


OUTPUT_TXT_FILE = Path(__file__).parent.parent / "data" / "speech_input.txt"


__ALL__ = [
    'look_for_audio_input',
    'realtime_textise'
]


""" デバイス上でのオーディオ系の機器情報を表示する """
def look_for_audio_input():
    
    pa = pyaudio.PyAudio()

    for i in range(pa.get_device_count()):
        print(pa.get_device_info_by_index(i))
        print()

    pa.terminate()


""" コールバック関数の定義 """
def callback(in_data, frame_count, time_info, status):

    # speech_recognitionオブジェクトを毎回作成するのではなく、使いまわすために、グローバル変数で定義しておく
    global sprec 

    try:
        audiodata  = sr.AudioData(in_data, SAMPLE_RATE, 2)
        sprec_text = sprec.recognize_google(audiodata, language='eng')
        
        with open(OUTPUT_TXT_FILE, 'a') as f: #ファイルの末尾に追記していく
            f.write("\n" + sprec_text)
    
    except sr.UnknownValueError:
        pass
    
    except sr.RequestError as e:
        pass
    
    finally:
        return (None, pyaudio.paContinue)


""" リアルタイムで音声を文字起こしする """
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
        stream_callback    = callback
    )
    
    stream.start_stream()
    
    while stream.is_active() :
        time.sleep(0.01)
    
    stream.stop_stream()
    stream.close()
    audio.terminate()


def main():
    realtime_textise()


if __name__ == '__main__':
    main()

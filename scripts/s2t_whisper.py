
import os
import wave
import pyaudio

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

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

# ファイルのパス
OUTPUT_TXT_FILE = Path(__file__).parent.parent / "data" / "user_speech.txt"
AUDIO_FILE_PATH = Path(__file__).parent.parent / "sounds" / "output.wav"

# 音声を文字起こしする
def speech_2_text(recording_time=5):

    with wave.open('sounds/output.wav', 'wb') as wf:
        
        p = pyaudio.PyAudio()
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(SAMPLE_RATE)

        stream = p.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, input=True)

        print('Recording...')
        for _ in range(0, SAMPLE_RATE // CHUNK * recording_time):
            
            in_data = stream.read(CHUNK)
            
            wf.writeframes(in_data)
                
        print('Done')

        stream.close()
        p.terminate()
    
    audio_file = open(AUDIO_FILE_PATH, "rb")
    transcript = client.audio.transcriptions.create(
        model           = "whisper-1", 
        file            = audio_file,
        response_format = "text"
    )

    return transcript


def main():
    speech_2_text()


if __name__ == '__main__':
    main()
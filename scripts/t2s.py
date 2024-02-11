""" t2s : text-to-speech """

import os
import time
import pygame

from mutagen.mp3 import MP3 as mp3
from openai import OpenAI


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def text_2_speech(text : str, model : str = "tts-1", voice : str = "alloy"):
    
    SPEECH_FILE_PATH = "data/speech_output.mp3"
    
    # テキストから音声を生成
    response = client.audio.speech.create(
        model = model,
        voice = voice,
        input = text
    )
    
    # stream からファイルに書き込み
    response.stream_to_file(SPEECH_FILE_PATH)

    # 再生
    pygame.mixer.init()
    pygame.mixer.music.load(SPEECH_FILE_PATH)
    pygame.mixer.music.play()
    
    # mp3 ファイルの長さだけ待機
    time.sleep(mp3(SPEECH_FILE_PATH).info.length + 0.5)
    
    # 終了
    pygame.mixer.quit()


if __name__ == '__main__':
    pass
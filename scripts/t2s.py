""" t2s : text-to-speech """

import os
import wave
import pyaudio

from pathlib import Path
from openai import OpenAI

from .modules.audio_parameter import (
    CHUNK
)


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def text_2_speech(text : str, model : str = "tts-1", voice : str = "alloy"):
    
    SPEECH_FILE_PATH = Path(__file__).parent.parent / "data" / "speech_output.mp3"
    
    response = client.audio.speech.create(
        model = model,
        voice = voice,
        input = text
    )
    
    response.stream_to_file(SPEECH_FILE_PATH)
    
    with wave.open(SPEECH_FILE_PATH, 'rb') as wf:

        p = pyaudio.PyAudio()

        stream = p.open(
            format    = p.get_format_from_width(wf.getsampwidth()),
            channels  = wf.getnchannels(),
            rate      = wf.getframerate(),
            output    = True
        )

        while len(data := wf.readframes(CHUNK)):
            stream.write(data)

        stream.close()
        p.terminate()
    
    


if __name__ == '__main__':
    pass
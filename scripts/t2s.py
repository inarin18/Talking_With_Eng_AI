""" t2s : text-to-speech """

import os
from pathlib import Path
import openai

from openai import OpenAI


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def t2s(text : str, model : str = "tts-1", voice : str = "alloy"):
    
    speech_file_path = Path(__file__).parent.parent / "data" / "speech_output.mp3"
    
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text
    )
    response.stream_to_file(speech_file_path)


if __name__ == '__main__':
    pass
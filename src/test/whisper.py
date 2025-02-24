
import os

from openai import OpenAI
from pathlib import Path

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

AUDIO_FILE_PATH = Path(__file__).parent.parent.parent / "sounds" / "output.wav"

audio_file = open(AUDIO_FILE_PATH, "rb")
transcript = client.audio.transcriptions.create(
    model = "whisper-1", 
    file  = audio_file,
    response_format="text"
)

print(transcript)
""" 
Date : 2023-12-30

Author : Hinata Inaoka

Description : 
    This is a main file of this project.

"""

import os

from openai import OpenAI

from scripts.s2t_google_recognition import realtime_textise
from scripts.s2t_whisper import speech_2_text
from scripts.gpt import Chat 
from scripts.t2s import t2s


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def main():
    
    realtime_textise()


if __name__ == "__main__":
    main() 
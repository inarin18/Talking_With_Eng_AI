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
from scripts.gpt import generate_gpt_response 
from scripts.t2s import t2s


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def main():
    
    RECORD_SECONDS = 5
    MAX_CONVERSATION_LENGTH = 2
    END_OF_CONVERSATION = "hinata"
    
    # 会話履歴の初期化
    conversation_history = []
    
    # gpt に対する指示
    instruction = """
    You are the native person in English.
    You are going to talk with a person who is not good at English.
    All you have to do is to conversation with him/her.
    You should comply with the following rules.
        1. If you find that 'user' made a mistake, You should inform him/her of the mistake and then correct it.
            ex 1) user : Hello I am a student.
            then you should respond on context.
            ex 2) user : Hello She am a student.
            then you should insist that 'she' is wrong and correct it like this.
            You : Your sentence is wrong. You should say 'I' instead of 'she'.
        2. You should talk with user as if you are a native person in English.
        3. Your resopnse should be on a context.
    """
    
    # gpt への指示を履歴に追加
    conversation_history.append(
        {
            "role": "system", 
            "content": instruction
        }
    )
    
    # ユーザーの発言を取得して終了判定も兼ねる
    for _ in range(MAX_CONVERSATION_LENGTH):
        
        # ユーザーの発言を取得
        user_sentence = speech_2_text(RECORD_SECONDS)
        
        if END_OF_CONVERSATION in user_sentence.lower() :
            break
        
        print("user : " + user_sentence + "\n")
    
        # ユーザの発言から gpt による回答を取得
        gpt_response  = generate_gpt_response(
            conversation_history = conversation_history, 
            user_sentence        = user_sentence, 
            gpt_model            = "gpt-3.5-turbo"
        )
        
        print("gpt  : " + gpt_response + "\n")
        
        # gpt の回答を履歴に追加
        conversation_history.append(
            {
                "role": "assistant", 
                "content": gpt_response
            }
        )
        
    for conversation in conversation_history:
        print(conversation["content"])


if __name__ == "__main__":
    main() 
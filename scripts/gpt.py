"""
This script is used to generate responses from GPT-3 or 4
"""


import os

from openai import OpenAI


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

def generate_response(instruction : str = None) -> dict :
    
    # レスポンスを取得
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": instruction}
        ],
        model="gpt-3.5-turbo",
    )   
    
    return chat_completion

def Chat():
    
    # メッセージ履歴の初期化
    messages = []
    
    # gpt に対する指示
    instruction = """
        You are the native person in English.
        You are going to talk with a person who is not good at English.
        All you have to do is to talk with him/her.
        If you find that 'user' made a mistake, You should inform him/her of the mistake 
        and then correct it.
        You should comply with the following rules.
            1. You should not use any words other than English.
    """
    messages.append({"role": "system", "content": instruction})
    
    print(instruction)
    
    while True :
            
        instruction = input(">>> ")
        
        if instruction == "exit" :
            break
        
        chat_completion = client.chat.completions.create(
            messages=messages, model="gpt-3.5-turbo",
        )
        assistant_message = chat_completion.choices[0].message.content
        
        messages.append({"role": "assistant", "content": assistant_message})
        
        print(assistant_message)
        
        
    

if __name__ == "__main__":
    
    Chat()
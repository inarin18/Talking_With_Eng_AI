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
    messages.append({"role": "system", "content": instruction})
    
    print(instruction)
    
    while True :
            
        user_content = input(">>> ")
        
        if user_content == "exit" :
            break
        
        messages.append({"role": "user", "content": user_content})
        
        chat_completion = client.chat.completions.create(
            messages=messages, model="gpt-3.5-turbo",
        )
        assistant_message = chat_completion.choices[0].message.content
        
        messages.append({"role": "assistant", "content": assistant_message})
        
        print(assistant_message)
        
        
    

if __name__ == "__main__":
    
    Chat()
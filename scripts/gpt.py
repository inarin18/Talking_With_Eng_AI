"""
This script is used to generate responses from GPT-3
"""


import os

from openai import OpenAI


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

# for personal
# openai.organization = "org-NCk1NUFa2Aw0WAB0lUKsbE9u"

def generate_response():
    
    # レスポンスを取得
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say this is a test",
            }
        ],
        model="gpt-3.5-turbo",
    )   
    
    print(chat_completion.choices[0].message.content)
    

if __name__ == "__main__":
    
    generate_response()
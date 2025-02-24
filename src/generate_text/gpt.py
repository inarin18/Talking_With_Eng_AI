"""
This script is used to generate responses from GPT-3 or 4
"""
import os

from openai import OpenAI


# ユーザの発言から gpt による回答を取得
def generate_gpt_response(client: OpenAI, conversation_history :list, gpt_model :str) -> str:
    
    # レスポンスを取得
    chat_completion = client.chat.completions.create(
        messages = conversation_history, 
        model    = gpt_model,
    )
    assistant_message = chat_completion.choices[0].message.content
    
    return assistant_message
    

if __name__ == "__main__":
    
    generate_gpt_response()
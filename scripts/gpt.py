"""
This script is used to generate responses from GPT-3 or 4
"""
import os

from openai import OpenAI


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


# ユーザの発言から gpt による回答を取得
def generate_gpt_response(conversation_history :list, user_sentence :str, gpt_model :str) -> str:
    
    # user の発言を履歴に追加
    conversation_history.append({"role": "user", "content": user_sentence})
    
    # レスポンスを取得
    chat_completion = client.chat.completions.create(
        messages = conversation_history, 
        model    = gpt_model,
    )
    assistant_message = chat_completion.choices[0].message.content
    
    return assistant_message
    

if __name__ == "__main__":
    
    generate_gpt_response()
# 
# OPENAI-Reference
# https://platform.openai.com/docs/api-reference
# https://github.com/openai/openai-python
#

import os
from openai import OpenAI

# for personal
# openai.organization = "org-NCk1NUFa2Aw0WAB0lUKsbE9u"

# API キーを用いてクライアントを初期化
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

""" completion """
def single_completion():
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

""" stream """ 
def stream_completion():
    
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Say this is a test"}],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")


""" image  """
# 一枚につき 0.04 USD
def generate_image():
    
    res = client.images.generate(
        model="dall-e-3",
        prompt="A painting of a glass of water on a table.",
        n=1,
        size="1024x1024"
    )

    print(res.data)
    
if __name__ == "__main__":
    # single_completion()
    # stream_completion()
    generate_image()
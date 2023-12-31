# 
# OPENAI-Reference
# https://platform.openai.com/docs/api-reference
#

import os
import openai

# for personal
openai.organization = "org-NCk1NUFa2Aw0WAB0lUKsbE9u"
# redefine after importing __init__.py of openai
openai.api_key = os.getenv("OPENAI_API_KEY")

completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role": "user", "content": "Hello!"}
    ]
)

print(completion.choices[0].message.content)

res = openai.Image.create(
    prompt = "A cute baby sea otter",
    n = 2,
    size = "1024x1024"
)

print(res.data)
import os
import json
import requests
from dotenv import load_dotenv
from deepseek import DeepSeekAPI

load_dotenv()
import io
import sys

# 强制修改标准输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openai import OpenAI
def call_deepseek(prompt):
    client = OpenAI(api_key="sk-aba47399db334ec9ae57fa17034a4006", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": prompt}, 
            {"role": "user", "content": "Hello"},
        ],
        stream=False
    )

    return response.choices[0].message.content

print(call_deepseek("今天是星期几"))
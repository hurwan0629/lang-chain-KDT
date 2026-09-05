from dotenv import load_dotenv
import os
import openai
from openai import OpenAI
import pprint

load_dotenv()
api_key = os.getenv("OPEN_AI_KEY")

print("OPEN_AI_KEY:", api_key[:8])

client = OpenAI(
    api_key=api_key,
)

response = client.responses.create(
    model="gpt-5-nano",
    input=[
        {
            "role": "user",
            "content": "openai의 response.crate의 messages 인자의 형태 알려줘"
        }
    ]
)

pprint.pprint(response)


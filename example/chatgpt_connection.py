from openai import OpenAI
import json

# Load API Key from Config Json
with open('../config/config.json') as f:
    data = json.load(f)
    api_key = data['openai_api_key']

client = OpenAI(
    api_key=api_key
)

completion = client.chat.completions.create(
    model="gpt-4o-mini-2024-07-18",
    messages=[{
        "role": "user",
        "content": "Write a one-sentence bedtime story about a unicorn."
    }]
)

print(completion.choices[0].message.content)
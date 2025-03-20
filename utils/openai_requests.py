from openai import OpenAI
from utils.common import config_load
from utils.openai_prompts import classification_prompt
import datetime
import json
from pydantic import BaseModel
from typing import Optional, Literal

config = config_load()

client = OpenAI(
    api_key=config['openai_api_key']
)

class ClassificationReport(BaseModel):
    name: Optional[str] = None
    question: Literal['Question', 'Weather Data', 'Miscellaneous']
    english: Optional[Literal['Good', 'Bad', 'Average']] = None
    time: Optional[str] = None

def classification_request(message):
    messages = [{
        "role": "developer",
        "content": classification_prompt
    }, {
        "role": "user",
        "content": f"""
            # Message
            {message}

            # Context
            Date and Time: {datetime.datetime.now(datetime.timezone.utc).isoformat()}
        """
    }]
    for _ in range(5):
        completion = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=messages,
        )

        response = completion.choices[0].message.content

        if response.startswith('```'):
            response = response[3:]
        if response.endswith('```'):
            response = response[:-3]
        if response.startswith('json'):
            response = response[4:]

        try:
            return ClassificationReport.model_validate_json(response).model_dump(exclude_none=True)
        except Exception as e:
            messages.append({
                "role": "user",
                "content": f'Error Parsing JSON: {e}'
            })
            continue
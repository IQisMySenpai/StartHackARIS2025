from openai import OpenAI
from utils.common import config_load
from utils.openai_prompts import classification_prompt, classic_response_prompt
import datetime
from pydantic import BaseModel
from typing import Optional, Literal

config = config_load()

client = OpenAI(
    api_key=config['openai_api_key']
)

def remove_response_formating(response, type):
    response = response.strip('```')
    if response.startswith(type):
        response = response[len(type):]
    response = response.strip('\n')

    return response

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
            model=config['openai_model'],
            messages=messages,
        )

        response = completion.choices[0].message.content
        response = remove_response_formating(response, 'json')

        try:
            return ClassificationReport.model_validate_json(response).model_dump(exclude_none=True)
        except Exception as e:
            messages.append({
                "role": "user",
                "content": f'Error Parsing JSON: {e}'
            })
            continue

def classic_response_request(message):
    messages = [{
        "role": "developer",
        "content": classic_response_prompt
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
            model=config['openai_model'],
            messages=messages,
        )

        response = completion.choices[0].message.content
        response = remove_response_formating(response, 'text')

        if response:
            return response

    return None


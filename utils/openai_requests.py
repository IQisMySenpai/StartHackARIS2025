from openai import OpenAI
from utils.common import config_load
from utils.openai_prompts import classification_prompt, classic_response_prompt, syngenta_bio_prompt
import datetime
from pydantic import BaseModel
from typing import Optional, Literal
from geopy.geocoders import Nominatim

config = config_load()

client = OpenAI(
    api_key=config['openai_api_key']
)

geoLoc = Nominatim(user_agent="GetLoc")

def remove_response_formating(response, type):
    response = response.replace(f'```{type}', '')
    response = response.replace('```', '')
    response = response.replace('\t', '  ')
    response = response.strip()
    response = response.strip('\n')
    response = response.strip()

    return response

class ClassificationReport(BaseModel):
    name: Optional[str] = None
    question: Literal['Syngenta Biological Question', 'Question', 'Weather Data', 'Miscellaneous']
    language: Optional[str] = None
    plant: Optional[str] = None
    literacy: Optional[Literal['Good', 'Bad', 'Average']] = None
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

def context_factory(user, message):
    context = f"Date and Time: {datetime.datetime.now(datetime.timezone.utc).isoformat()}"
    if 'name' in user:
        context += f"\nUser Name: {user['name']}"
    if 'language' in user:
        context += f"\nUser Preferred Language: {user['language']}"
    if 'plant' in user:
        context += f"\nGrowing Plant on Field: {user['plant']}"
    if 'literacy' in user:
        context += f"\nUser Literacy Level: {user['literacy']}"
    if 'target_time' in message:
        context += f"\nTarget Time: {message['target_time']}"
    if 'latitude' in user and 'longitude' in user:
        lat = user['latitude']
        lon = user['longitude']
        context += f"\nField Location: Latitude: {lat}, Longitude: {lon}, Address: {geoLoc.reverse(f'{lat}, {lon}').address}"
    if 'latitude' not in user or 'longitude' not in user:
        context += f"\n\nRemind User to Provide the Location Message of their Field, as we need it to provide accurate weather data."

    return context

def classic_response_request(message, user, past_messages):
    msg = message['original_message']

    messages = [{
        "role": "developer",
        "content": classic_response_prompt
    }]

    past_messages.reverse()

    for past_message in past_messages:
        messages.append({
            "role": "user",
            "content": f"""
                # Message
                {past_message['original_message']}
            """
        })
        messages.append({
            "role": "assistant",
            "content": f"""
                ```text
                {past_message['responded']}
                ```
            """
        })


    messages.append({
        "role": "user",
        "content": f"""
            # Message
            {msg}

            # Context
            {context_factory(user, message)}
        """
    })

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

def syngenta_bio_request(message, user, past_messages):
    msg = message['original_message']

    messages = [{
        "role": "developer",
        "content": syngenta_bio_prompt
    }]

    past_messages.reverse()

    for past_message in past_messages:
        messages.append({
            "role": "user",
            "content": f"""
                # Message
                {past_message['original_message']}
            """
        })
        messages.append({
            "role": "assistant",
            "content": f"""
                ```text
                {past_message['responded']}
                ```
            """
        })

    messages.append({
        "role": "user",
        "content": f"""
            # Message
            {msg}

            # Context
            {context_factory(user, message)}
        """
    })

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

def speech_to_text_request(audio_data):
    # Send the audio to OpenAI Whisper for transcription
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_data
    )

    return transcription.text

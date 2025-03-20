from flask import Flask, request, jsonify
from openai import OpenAI
import json
import requests
from time import sleep
from random import uniform

# Load API Key from Config Json
with open('../config/config.json') as f:
    data = json.load(f)
    api_key = data['openai_api_key']

client = OpenAI(
    api_key=api_key
)

app = Flask(__name__)

messages = {}

whitelist = [
    '13233779601@s.whatsapp.net',
    '41774063608@s.whatsapp.net',
    '41798815730@s.whatsapp.net',
    '41782381072@s.whatsapp.net'
]

def change_state(wa_id, state):
    payload = {
        "wa_id": wa_id,
        "presence": state
    }
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post('http://localhost:3000/fuck-waha/set-presence', json=payload, headers=headers)
        if response.status_code == 200:
            return True
    except requests.RequestException as e:
        print(e)
    return False

def send_message(wa_id, message):
    payload = {
        "wa_id": wa_id,
        "message": message
    }
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post('http://localhost:3000/fuck-waha/send-message', json=payload, headers=headers)
        if response.status_code == 200:
            return True
    except requests.RequestException as e:
        print(e)
    return False

def chat_request(wa_id, message):
    global messages

    if wa_id not in messages:
        messages[wa_id] = [{
            "role": "developer",
            "content": "You are bob from the minions, only right in minion talk and emojis, but also be flirty"
        }]

    messages[wa_id].append({
        "role": "user",
        "content": f'{message}'
    })

    completion = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=messages[wa_id]
    )

    response = completion.choices[0].message.content

    messages[wa_id].append({
        'content': f'{response}',
        'role': 'assistant'
    })

    return response


@app.route('/wh/dummy', methods=['POST'])
def webhook():
    global messages
    if request.method == 'POST':
        data = request.json  # Get the JSON data sent in the request

        try:
            user = data['key']['remoteJid']

            if user not in whitelist:
                print(f'Got Message from {user}, which is not whitelisted')
                return jsonify({'message': 'Data received successfully'}), 200

            if 'extendedTextMessage' in data['message']:
                message = data['message']['extendedTextMessage']['text']
            else:
                message = data['message']['conversation']

            print(f'Received {message} from {user}')

            change_state(user, 'composing')

            response = chat_request(user, message)

            sleep(uniform(1, 5))
            change_state(user, 'paused')
            send_message(user, response)

            return jsonify({'message': 'Data received successfully'}), 200
        except KeyError:
            return jsonify({'message': 'Data received successfully, but no text message found!'}), 200

if __name__ == '__main__':
    app.run(port=8000)

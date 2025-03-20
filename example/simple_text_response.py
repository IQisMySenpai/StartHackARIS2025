from flask import Flask, request, jsonify
from openai import OpenAI
import json
import requests

# Load API Key from Config Json
with open('../config/config.json') as f:
    data = json.load(f)
    api_key = data['openai_api_key']

client = OpenAI(
    api_key=api_key
)

app = Flask(__name__)

@app.route('/wh/dummy', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json  # Get the JSON data sent in the request

        try:
            message = data['message']['extendedTextMessage']['text']

            completion = client.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[{
                    "role": "user",
                    "content": f'Write a one-sentence response to "{message}"'
                }]
            )

            response_message = completion.choices[0].message.content

            # Send the response message to the specified endpoint
            payload = {
                "wa_id": data['key']['remoteJid'],
                "message": response_message
            }
            headers = {'Content-Type': 'application/json'}

            try:
                response = requests.post('http://localhost:3000/fuck-waha/send-message', json=payload, headers=headers)
                if response.status_code == 200:
                    print('Message sent successfully!')
                else:
                    print(f'Failed to send message. Status code: {response.status_code}, Response: {response.text}')
            except requests.RequestException as e:
                print(f'Request failed: {e}')

            return jsonify({'message': 'Data received and processed successfully!'}), 200
        except KeyError:
            return jsonify({'message': 'Data received successfully, but no text message found!'}), 200

if __name__ == '__main__':
    app.run(port=8000)

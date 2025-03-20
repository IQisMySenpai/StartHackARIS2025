from mongoAPI import MongoAPI
from utils.common import config_load
from flask import Flask, request, jsonify
import datetime
from utils.openai_requests import classification_request

config = config_load()

mongo = MongoAPI(
    db_username=config['db_user'],
    db_password=config['db_password'],
    db_address=config['db_host'],
    db_name=config['db_name'],
    service=config['db_service'])

app = Flask(__name__)

whitelist = [
    '13233779601@s.whatsapp.net',
    '41774063608@s.whatsapp.net'
]

@app.route('/wh/dummy', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json  # Get the JSON data sent in the request

        # print(data)

        try:
            user = data['key']['remoteJid']

            if user not in whitelist:
                # print(f'Got Message from {user}, which is not whitelisted')
                return jsonify({'message': 'Data received successfully'}), 200

            if 'extendedTextMessage' in data['message']:
                message = data['message']['extendedTextMessage']['text']
            else:
                message = data['message']['conversation']

            print(f'Received {message} from {user}')

            classification = classification_request(message)

            db_message = {
                'wa_id': user,
                'original_message': message,
                'received_time': datetime.datetime.now(tz=datetime.timezone.utc),
                'question_type': classification['question'],
            }

            if 'time' in classification:
                db_message['target_time'] = classification['time']

            mongo.insert_one('messages', db_message)

            return jsonify({'message': 'Data received successfully'}), 200
        except KeyError:
            return jsonify({'message': 'Data received successfully, but no text message found!'}), 200

if __name__ == '__main__':
    app.run(port=8000)


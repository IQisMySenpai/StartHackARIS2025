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
    '41774063608@s.whatsapp.net',
    '41798815730@s.whatsapp.net',
    '41782381072@s.whatsapp.net'
]

def handle_location_update(wa_id, latitude, longitude):
    db_user = {
        'wa_id': wa_id,
        'latitude': latitude,
        'longitude': longitude
    }

    mongo.update_one('users', {'wa_id': wa_id}, {'$set': db_user}, upsert=True)

@app.route('/wh/dummy', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json  # Get the JSON data sent in the request

        try:
            user = data['key']['remoteJid']

            if user not in whitelist:
                # print(f'Got Message from {user}, which is not whitelisted')
                return jsonify({'message': 'Data received successfully, user not on Whitelist'}), 200

            if 'locationMessage' in data['message']:
                handle_location_update(user, data['message']['locationMessage']['degreesLatitude'], data['message']['locationMessage']['degreesLongitude'])
                return jsonify({'message': 'Data received successfully'}), 200

            if 'extendedTextMessage' in data['message']:
                message = data['message']['extendedTextMessage']['text']
            else:
                message = data['message']['conversation']

            if message is None or message == '':
                return jsonify({'message': 'Data received successfully, but no text message found!'}), 200

            print(f'Received {message} from {user}')

            #push_name = data['pushName']

            classification = classification_request(message)

            db_message = {
                'wa_id': user,
                'original_message': message,
                'received_time': datetime.datetime.now(tz=datetime.timezone.utc),
                'question_type': classification['question'],
            }

            if 'target_time' in classification:
                db_message['target_time'] = classification['target_time']

            mongo.insert_one('messages', db_message)

            db_user = {
                'wa_id': user
            }

            if 'name' in classification:
                db_user['name'] = classification['name']

            if 'language' in classification:
                db_user['language'] = classification['language']

            if 'literacy' in classification:
                db_user['literacy'] = classification['literacy']

            if 'plant' in classification:
                db_user['plant'] = classification['plant']

            mongo.update_one('users', {'wa_id': user}, {'$set': db_user}, upsert=True)

            return jsonify({'message': 'Data received successfully'}), 200
        except KeyError:
            return jsonify({'message': 'Data received successfully, but no text message found!'}), 200

if __name__ == '__main__':
    app.run(port=8000)


from mongoAPI import MongoAPI
from utils.common import config_load
from flask import Flask, request, jsonify
import datetime
from utils.openai_requests import classification_request, speech_to_text_request
import base64
from pydub import AudioSegment
import io

config = config_load()

mongo = MongoAPI(
    db_username=config['db_user'],
    db_password=config['db_password'],
    db_address=config['db_host'],
    db_name=config['db_name'],
    service=config['db_service'])

app = Flask(__name__)

def handle_location_update(wa_id, latitude, longitude):
    db_user = {
        'wa_id': wa_id,
        'latitude': latitude,
        'longitude': longitude
    }

    mongo.update_one('users', {'wa_id': wa_id}, {'$set': db_user}, upsert=True)

blacklist = [
    '13233779601@s.whatsapp.net',
]

@app.route('/wh/dummy', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json  # Get the JSON data sent in the request

        try:
            user = data['key']['remoteJid']

            if not user.endswith("@s.whatsapp.net"):
                return jsonify({'message': 'Data received successfully, but I serve no groups'}), 200

            if user in blacklist:
                return jsonify({'message': 'Data received successfully, but I serve no blacklist'}), 200

            # Handle location messages
            if 'locationMessage' in data['message']:
                handle_location_update(user, data['message']['locationMessage']['degreesLatitude'], data['message']['locationMessage']['degreesLongitude'])
                return jsonify({'message': 'Data received successfully'}), 200

            respond_with_audio = False

            # Handle audio messages
            if 'audioData' in data:
                audio_base64 = data['audioData']
                audio_bytes = base64.b64decode(audio_base64)

                # Convert the byte data to an AudioSegment object
                audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format='ogg')

                # Export the audio to a BytesIO object as WAV format
                wav_io = io.BytesIO()
                audio.export(wav_io, format='wav')
                wav_io.seek(0)  # Move to the start of the file-like object

                fake_taxi = ('audio.wav', wav_io, 'audio/wav')

                message = speech_to_text_request(fake_taxi)
                respond_with_audio = True
            elif 'extendedTextMessage' in data['message']:
                message = data['message']['extendedTextMessage']['text']
            else:
                message = data['message'].get('conversation', '')

            if not message:
                return jsonify({'message': 'Data received successfully, but no text message found!'}), 200

            print(f'Received {message} from {user}')

            classification = classification_request(message)

            db_message = {
                'wa_id': user,
                'original_message': message,
                'received_time': datetime.datetime.now(tz=datetime.timezone.utc),
                'question_type': classification['question'],
                'respond_with_audio': respond_with_audio
            }

            if 'target_time' in classification:
                db_message['target_time'] = classification['target_time']

            mongo.insert_one('messages', db_message)

            db_user = {'wa_id': user}

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


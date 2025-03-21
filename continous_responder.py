from time import sleep
from random import uniform
from mongoAPI import MongoAPI
from utils.common import config_load, generate_writing_duration
from utils.openai_requests import classic_response_request, syngenta_bio_request, text_to_speech_request
from utils.whatsapp_requests import send_message, change_state, send_voice

config = config_load()

mongo = MongoAPI(
    db_username=config['db_user'],
    db_password=config['db_password'],
    db_address=config['db_host'],
    db_name=config['db_name'],
    service=config['db_service'])

while True:
    messages = mongo.find(
        'messages',
        {'responded': {'$exists': False}},
        sort=[('received_time', 1)],
        limit=20
    )

    for message in messages:
        past_messages = mongo.find(
            'messages',
            {'wa_id': message['wa_id'], 'responded': {'$exists': True}},
            sort=[('received_time', -1)],
            limit=5
        )

        user = mongo.find_one('users', {'wa_id': message['wa_id']})

        if message['question_type'] == 'Question' or message['question_type'] == 'Miscellaneous':
            response = classic_response_request(message, user, past_messages)
        elif message['question_type'] == 'Syngenta Biological Question':
            response = syngenta_bio_request(message, user, past_messages)

        change_state(message['wa_id'], 'composing')
        sleep(generate_writing_duration())
        change_state(message['wa_id'], 'paused')

        if message['respond_with_audio']:
            send_voice(message['wa_id'], text_to_speech_request(response))
        else:
            send_message(message['wa_id'], response)

        mongo.update_one(
            'messages',
            {'_id': message['_id']},
            {'$set': {'responded': response}}
        )

        sleep(uniform(3, 7))

    if len(messages) <= 0:
        sleep(uniform(5, 10))


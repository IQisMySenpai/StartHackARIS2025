from time import sleep
from random import uniform
from mongoAPI import MongoAPI
from utils.common import config_load, generate_writing_duration
from utils.openai_requests import classic_response_request
from utils.whatsapp_requests import send_message, change_state

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
        print(message)
        response = classic_response_request(message['original_message'])

        change_state(message['wa_id'], 'composing')
        sleep(generate_writing_duration(response))
        change_state(message['wa_id'], 'paused')
        send_message(message['wa_id'], response)

        mongo.update_one(
            'messages',
            {'_id': message['_id']},
            {'$set': {'responded': True}}
        )

        sleep(uniform(3, 7))

    if len(messages) <= 0:
        sleep(uniform(5, 10))


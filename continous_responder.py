from time import sleep
from random import uniform
from mongoAPI import MongoAPI
from utils.common import config_load, generate_writing_duration
from utils.openai_requests import classic_response_request, syngenta_bio_request, text_to_speech_request
from utils.whatsapp_requests import send_message, change_state, send_voice, send_image
from utils.openai_requests import classic_response_request, syngenta_bio_request
from api_dev.supporting import create_risk_report, get_city_name
from api_dev.img_generation import generate

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

        if message['question_type'] in ['Question', 'Miscellaneous', 'Risk Analysis']:
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

        if message['question_type'] == 'Risk Analysis':
            if 'latitude' in user and 'longitude' in user and 'plant' in user:
                if 'target_time' in message:
                    risks, risks_floats = create_risk_report(user, target_time=message['target_time'])
                else:
                    risks, risks_floats = create_risk_report(user)

                crop_name = user['plant']
                longitude = user['longitude']
                latitude = user['latitude']

                elements = [
                    {"header": "Elevated temperature",
                     "body": "The maximum temperature will be exceeded, I recommend applyig Stress Buster to ensure the well being of your crops.",
                     "type": "warning", "icon": "Icons/temperature-arrow-up-solid.png",
                     "status": (risks['diurnal_stress'] | risks["nighttime_stress"])},
                    {"header": "Low moisture",
                     "body": "A drought is incoming, I recomend appling Stress buster to ensure the well being of your crops.",
                     "type": "warning", "icon": "Icons/sun-plant-wilt-solid.png", "status": risks["frost_stress"]},
                    {"header": "Frost Warning",
                     "body": "Frost is expected in the coming days, I recommend applying Stress Buster to your crops to ensure their well being",
                     "type": "warning", "icon": "Icons/snowflake-regular.png", "status": risks["drought_risk"]},
                    {"header": "Yield Risk",
                     "body": "Based on avilible data, your yield is at a risk of being lower that expected. Apply Yield Booster to your crops to ensure the best possible yield.",
                     "type": "warning", "icon": "Icons/arrow-down-wide-short-solid.png",
                     "status": risks["yield_risk"]}
                ]
                city_name = get_city_name(longitude, latitude)

                send_image(user['wa_id'], generate(elements, crop_name, city_name))

        mongo.update_one(
            'messages',
            {'_id': message['_id']},
            {'$set': {'responded': response}}
        )

        sleep(uniform(3, 7))

    if len(messages) <= 0:
        sleep(uniform(5, 10))


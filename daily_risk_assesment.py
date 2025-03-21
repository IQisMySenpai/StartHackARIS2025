import schedule
import time
import datetime
from mongoAPI import MongoAPI
from utils.common import config_load
from api_dev.img_generation import generate
from api_dev.risks import get_city_name
from api_dev.supporting import create_risk_report
from utils.whatsapp_requests import send_image

config = config_load()

mongo = MongoAPI(
    db_username=config['db_user'],
    db_password=config['db_password'],
    db_address=config['db_host'],
    db_name=config['db_name'],
    service=config['db_service'])

def job():
    users = mongo.find('users', {'latitude': {'$exists': True}, 'longitude': {'$exists': True}, 'plant': {'$exists': True}})

    print(f"Found {len(users)} users")
    print(users)

    for user in users:
        risks, risks_floats = create_risk_report(user, True)

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
             "type": "warning", "icon": "Icons/sun-plant-wilt-solid.png", "status": risks["drought_risk"]},
            {"header": "Frost Warning",
             "body": "Frost is expected in the coming days, I recommend applying Stress Buster to your crops to ensure their well being",
             "type": "warning", "icon": "Icons/snowflake-regular.png", "status": risks["frost_stress"]},
            {"header": "Yield Risk",
             "body": "Based on avilible data, your yield is at a risk of being lower that expected. Apply Yield Booster to your crops to ensure the best possible yield.",
             "type": "warning", "icon": "Icons/arrow-down-wide-short-solid.png", "status": risks["yield_risk"]}
        ]
        city_name = get_city_name(longitude, latitude)

        send_image(user['wa_id'], generate(elements, crop_name, city_name))


# Schedule the task to run at 08:00 AM every day
schedule.every().day.at("08:00").do(job)
while True:
    schedule.run_pending()  # Run the scheduled task if it's time
    time.sleep(60)  # Check every minute if it's time to run the task
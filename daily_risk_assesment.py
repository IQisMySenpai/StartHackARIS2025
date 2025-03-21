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
        risks, risks_floats = create_risk_report(user)

        plant = user['plant']
        longitude = user['longitude']
        latitude = user['latitude']

        elements = [
            {
                "header": "Elevated Temperature Alert!",
                "body": "Hey there! It looks like the maximum temperature is set to rise. To keep your crops happy and healthy, I highly recommend applying Stress Buster. It’s your best friend in tackling heat stress and ensuring your plants thrive!",
                "type": "warning",
                "icon": "Icons/temperature-arrow-up-solid.png",
                "status": (risks['diurnal_stress'] | risks["nighttime_stress"])
            },
            {
                "header": "Low Moisture Warning!",
                "body": "Heads up! A drought is on the horizon. Don’t let your crops suffer—apply Stress Buster to keep them hydrated and flourishing. Your plants will thank you for it!",
                "type": "warning",
                "icon": "Icons/sun-plant-wilt-solid.png",
                "status": risks["drought_risk"]
            },
            {
                "header": "Frost Warning!",
                "body": "Brrr! Frost is expected in the coming days. Protect your precious crops by applying Stress Buster. It’s the perfect shield to ensure they stay safe and sound during chilly nights!",
                "type": "warning",
                "icon": "Icons/snowflake-regular.png",
                "status": risks["frost_stress"]
            },
            {
                "header": "Yield Risk Alert!",
                "body": "Uh-oh! Based on the latest data, your yield might be at risk of falling short. Don’t worry—apply Yield Booster to give your crops the extra boost they need for a bountiful harvest. Let’s make sure you get the best out of your fields!",
                "type": "warning",
                "icon": "Icons/arrow-down-wide-short-solid.png",
                "status": risks["yield_risk"]
            }
        ]

        city_name = get_city_name(longitude, latitude)

        send_image(user['wa_id'], generate(elements, plant, city_name))

job()
# # Schedule the task to run at 08:00 AM every day
# schedule.every().day.at("08:00").do(job)
# while True:
#     schedule.run_pending()  # Run the scheduled task if it's time
#     time.sleep(60)  # Check every minute if it's time to run the task
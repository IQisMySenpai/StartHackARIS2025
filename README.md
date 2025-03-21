# PlantPal - WhatsApp Bot for Farmers

## Overview
PlantPal is a WhatsApp bot developed during the Start-Hack 2025 hackathon. It serves as a smart assistant for farmers, providing them with essential, real-time information to help improve agricultural productivity and crop management. PlantPal leverages data-driven insights to give farmers accurate advice and risk assessments directly through their WhatsApp.

## Features
- 📱 **WhatsApp Integration:** Farmers can interact with the bot via simple messages on WhatsApp.
- 🌱 **Personalized Responses:** Provides tailored information based on farmer queries.
- 📊 **Daily Risk Assessment:** Notifies farmers of potential risks based on weather, soil data, and other relevant metrics.
- 🤖 **Continuous Monitoring:** The bot operates continuously to ensure that farmers receive timely updates and support.

## Setup & Usage
1. Clone the repository with its required submodules.
   ```bash
   git clone --recurse-submodules
    ```
2. Install the required packages.
    ```bash
    pip install -r requirements.txt
    ```
3. Run the following scripts in order:
   - `python3 request_classifier.py`
   - `python3 continous_responder.py`
   - `python3 daily_risk_assesment.py`

4. Run the baileys API bot by
   ```bash
   cd baileys
   npm i
   ```
   
5. Run the bot by
   ```bash
   npm run build # to build the project
   npm start # to start the bot
   ```

## How It Works
1. **Request Classification:** Incoming messages are classified using `request_classifier.py`.
2. **Continuous Response Handling:** `continous_responder.py` processes incoming messages and generates relevant responses.
3. **Daily Risk Assessment:** `daily_risk_assesment.py` runs periodically to provide proactive notifications about potential risks.

## Future Enhancements
- Adding multilingual support for broader accessibility.
- Expanding data sources to improve the accuracy of predictions.
- Enhancing user experience with more intuitive responses.

## Contributors
- Jannick Schröer
- Matias Betschen
- Victor Elliesen
- Nicolo Massari

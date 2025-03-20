import requests
from pydub import AudioSegment
from io import BytesIO

# Step 1: Download the encrypted audio file
url = "https://mmg.whatsapp.net/v/t62.7117-24/34597152_2004757583343163_556445408732480372_n.enc?ccb=11-4&oh=01_Q5AaIXNvst0stw_6G22M-4n3yHpClvxMUicjf0JD1kuc3Xok&oe=6803E3A7&_nc_sid=5e03e0"
response = requests.get(url)

if response.status_code == 200:
    # Step 2: Save to memory
    audio_data = BytesIO(response.content)

    # Step 3: Load the audio using pydub (assumes the file is not encrypted)
    try:
        audio = AudioSegment.from_file(audio_data, format="ogg")
        print(f"Audio loaded successfully! Duration: {len(audio) / 1000} seconds")

        # Optionally, save the audio to a file
        audio.export("audio_message.wav", format="wav")
        print("Audio saved as audio_message.wav")

    except Exception as e:
        print(f"Error loading audio: {e}")
else:
    print(f"Failed to download audio. Status code: {response.status_code}")
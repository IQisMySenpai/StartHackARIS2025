import requests

def wa_request(endpoint: str, payload):
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(f'http://localhost:3000/fuck-waha{endpoint}', json=payload, headers=headers)
        if response.status_code == 200:
            return True
    except requests.RequestException as e:
        print(e)
    return False

def change_state(wa_id: str, state: str):
    """
    Send a presence update to the whatsapp API
    :param wa_id: WA ID of Target Chat
    :param state: One of the available states.
    :return:
    """
    valid_states = ['unavailable', 'available', 'composing', 'recording', 'paused']

    if state not in valid_states:
        return False

    payload = {
        "wa_id": wa_id,
        "presence": state
    }

    return wa_request('/set-presence', payload)

def send_message(wa_id, message):
    """
    Send a Message to a chat
    :param wa_id:  WA ID of Target Chat
    :param message: Message to send in chat
    :return:
    """

    payload = {
        "wa_id": wa_id,
        "message": message
    }

    return wa_request('/send-message', payload)

def send_voice(wa_id, voice):
    url = 'http://localhost:3000/fuck-waha/send-voice'

    files = {'upload': voice}
    params = {'wa_id': wa_id}

    # Send the request
    upload_response = requests.post(url, files=files, data=params)

    # Print the response from the server
    print(upload_response.text)
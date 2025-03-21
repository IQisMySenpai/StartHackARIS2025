import requests

# The URL where the image will be uploaded
url = 'http://localhost:3000/fuck-waha/send-voice'

# The file you want to upload
file_path = 'frog.opus'

# Prepare the file for upload
files = {'upload': open(file_path, 'rb')}

# Prepare additional parameters with an '@' symbol in the value
params = {'wa_id': '41782381072@s.whatsapp.net'}

# Make the POST request to upload the image along with parameters
response = requests.post(url, files=files, data=params)

# Print the response from the server
print(response.text)

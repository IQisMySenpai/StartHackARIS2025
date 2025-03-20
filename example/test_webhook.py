from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/wh/dummy', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.json  # Get the JSON data sent in the request
        print('Received JSON Data:', data)
        return jsonify({'message': 'Data received successfully!'}), 200

if __name__ == '__main__':
    app.run(port=8000)
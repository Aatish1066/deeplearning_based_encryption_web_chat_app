from flask import *
import json
import requests
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)
# Dictionary to store messages for each room
messages = {}
# Define route for the home page
@app.route('/')
def home():
    # Render the home page template
    return render_template('home.html')


@app.route('/update_data', methods=['POST'])
def update_data():
    new_data = request.json  # Get the data from the POST request
    try:
        with open('data.json', 'r') as file:
            existing_data = json.load(file)
    except Exception as e:
        # Handle file not found or JSON decoding error
        existing_data = []

    if new_data not in existing_data:
        existing_data.append(new_data)
        with open('data.json', 'w') as file:
            json.dump(existing_data, file)
        return jsonify({"message": "Data updated successfully"}), 200
    else:
        return jsonify({"message": "Data already exists"}), 200
@app.route('/chat')
def chat():
    room_code = request.args.get('room')
    # Render the chat application for the specified room code
    # You can pass the room code to the template if needed
    return render_template('chat.html', room_code=room_code)


@app.route('/messages')
@cross_origin(supports_credentials=True)
def get_messages():
    room_code = request.args.get('room')
    userID = request.args.get('userID')

    if room_code in messages:
        decrypted_messages = []
        for msg in messages[room_code]:
            # Decrypt each message before sending it to the client
            data = {
                'message': msg['text'],
                'choice': 'decrypt'
            }
            response = requests.post('http://127.0.0.1:8888/process_message', json=data)
            decrypted_data = response.json()
            decrypted_messages.append({'sender': msg['sender'], 'text': decrypted_data["processed_message"]})

        return jsonify({'messages': decrypted_messages}), 200
    else:
        return jsonify({'messages': []}), 200


@app.route('/send_message', methods=['POST'])
def send_message():

    room_code = request.form.get('room')
    message = request.form.get('message')
    user = request.form.get('userID')
    data = {
        'message': message,
        'choice': 'encrypt'  # or 'decrypt'
    }
    response = requests.post('http://127.0.0.1:8888/process_message', json=data)
    datau = response.json()
    if room_code:
        if room_code not in messages:
            messages[room_code] = []
        messages[room_code].append({'sender': user, 'text': datau["processed_message"]})
        return jsonify({'status': 'Message sent successfully'}), 200
    else:
        return jsonify({'error': 'Room code not provided'}), 400

if __name__ == '__main__':
    app.run()

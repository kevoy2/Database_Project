from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        received_data = data
        return jsonify({'message': 'Login credintials received successfully', 'received': received_data})
    
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        received_data = data
        return jsonify({'message': 'Registration data received successfully', 'received': received_data})
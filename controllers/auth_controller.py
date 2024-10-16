from flask import request, jsonify, current_app
from models.user_model import User
from services.auth_service import generate_token, decode_token
from app import db 


def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.verify_user(username, password):
        token = generate_token(username)
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid username or password'}), 401

def register():
    data = request.get_json()
    # print(data)
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    # with current_app.app_context():
    user = User.register_user(username, password)
    if user:
        return jsonify({'message': 'User registered successfully'}), 201
    
    return jsonify({'message': 'User registration failed'}), 500

def protected():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing'}), 401

    decoded = decode_token(token)
    if decoded == "expired":
        return jsonify({'message': 'Token has expired'}), 401
    elif decoded == "invalid":
        return jsonify({'message': 'Invalid token'}), 401

    return jsonify({'message': 'This is a protected route', 'user': decoded['username']}), 200

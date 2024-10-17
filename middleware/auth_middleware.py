from functools import wraps
from flask import request, jsonify, redirect, url_for
from services.auth_service import generate_token, decode_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token is missing'}), 401

         # Check if the token is in the header (API usage)
        if auth_header:
            if not auth_header.startswith("Bearer "):
                return jsonify({'message': 'Invalid token format'}), 401
            token = auth_header.split(" ")[1]
        else:
            return redirect(url_for('login')) 

        decoded = decode_token(token)
        if decoded == "expired":
            return jsonify({'message': 'Token has expired'}), 401
        elif decoded == "invalid":
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args, decoded_token=decoded, **kwargs)
    return decorated

import jwt
import datetime
from flask import current_app

def generate_token(username):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({'username': username, 'exp': expiration_time}, current_app.config['SECRETKEY_JWT'], algorithm='HS256')
    return token

def decode_token(token):
    try:
        decoded = jwt.decode(token, current_app.config['SECRETKEY_JWT'], algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return "expired"
    except jwt.InvalidTokenError:
        return "invalid"

import os

class Config:
    SECRETKEY_JWT = os.environ.get('SECRETKEY_JWT')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-university-dbms'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///university.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
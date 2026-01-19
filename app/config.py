import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:KLfSXTrnIXCMjzYjugIKORyBnytpcGFJ@crossover.proxy.rlwy.net:31125/railway'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
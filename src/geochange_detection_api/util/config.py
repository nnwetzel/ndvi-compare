from os import environ
from dotenv import load_dotenv

load_dotenv()
class Config():
    GEE_PROJECT_ID = environ.get("GEE_PROJECT_ID")
    HOST = '127.0.0.1'
    PORT = int(environ.get('PORT', '8000'))

def get_config():
    return Config()
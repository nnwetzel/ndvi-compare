from os import environ
from dotenv import load_dotenv

load_dotenv()
class Config():
    GEE_PROJECT_ID = environ.get("GEE_PROJECT_ID")

def get_config():
    return Config()
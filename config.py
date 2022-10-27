import os

from dotenv import load_dotenv

load_dotenv()

config = {
    'token_bot'     : os.getenv('token_bot'),
    'open_ai_token' : os.getenv('open_ai_token')
}   

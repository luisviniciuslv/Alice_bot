import os

from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

config = {
    'token_bot' : os.getenv('bot_token'),
    'open_ai_token' : os.getenv('api_key'),
    'mongo_token' : os.getenv('database_connection')
}   

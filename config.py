import os

from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

config = {
    'token_bot'     : os.getenv('bot_token'),
    'open_ai_token' : os.getenv('open_ai_token'),
    'mongo_db'      : os.getenv('mongo_db')
}   

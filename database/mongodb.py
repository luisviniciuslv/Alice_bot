import os
from datetime import datetime

from dotenv import load_dotenv
from pymongo import MongoClient
from config import config
load_dotenv()

client = MongoClient(config['mongo_token'])
db = client['AI']
async def get_log():
    collection = db['Alice']
    return collection.find_one({'id': 'Alice'})['log']


def set_log(text):
    collection = db['Alice']
    collection.update_one({'id': 'Alice'}, {'$set': {'log': text}})

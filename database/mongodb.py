import os
from datetime import datetime

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("database_connection"))
db = client['AI']
async def get_log():
    collection = db['Alice']
    return collection.find_one({'id': 'Alice'})['log']


def set_log(text):
    collection = db['Alice']
    collection.update_one({'id': 'Alice'}, {'$set': {'log': text}})

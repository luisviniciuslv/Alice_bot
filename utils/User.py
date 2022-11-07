import os
from datetime import datetime
from errors import WrongWord
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("database_connection"))
db = client['AliceBot']
collection = db['Termo']
async def create_account(userID : int):
    if not collection.find_one({'_id': userID}):
        collection.insert_one({'_id': userID, 'actual_word': None, 'attempts': 0, 'points': 0, 'words': []})

def generate_word(words_list : list):
    words = ['banana', 'orangotango', 'quadro']

async def User(userID: int):
    user = _User(userID)
    await user._init()
    return user

class _User:
    def __init__(self, userID):
        self.userID = userID

    async def _init(self):
        await create_account(self.userID)
        self.user = collection.find_one({'_id': self.userID})
    
    @property
    def get(self):
        return self.user
    
    async def try_word(self, word):
        if word == self.actual_word:
            self.words.append(word)
            self.actual_word = None
            self.attempts = 0
            self.points += 1
            collection.update_one({'_id': self.userID}, {'$set': {'words': self.words, 'actual_word': self.actual_word, 'attempts': self.attempts, 'points': self.points}})
            return True
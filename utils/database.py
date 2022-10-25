from config import config
from dotenv import load_dotenv
from pymongo import MongoClient
import datetime 
import pytz

load_dotenv()
client = MongoClient(config['mongo_db'])
db = client['AliceBot']

async def create_account(userID : int):
    collection = db['saves']
    if not collection.find_one({'_id': userID}):
        collection.insert_one({'_id': userID, 'images': [], 'videos': [], 'anotations': []})
      
async def new_anotation(userID : int, anotation_text : str):
    
    await create_account(userID)
    collection = db['saves']
    anotation = {
      'date': datetime.datetime.now(pytz.timezone('America/Santarem')),
      'anotation': anotation_text
    }
    collection.update_one({'_id': userID}, {'$push': {'anotations': anotation}})
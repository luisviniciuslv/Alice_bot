import datetime
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("database_connection"))
db = client['server']
async def create_account(guildID : int, userID : int):
    collection = db[str(guildID)]
    if not collection.find_one({'_id': userID}):
        collection.insert_one({'_id': userID, 'coins': 0, 'banco': 0, 'valor_ganho': 0, 'valor_perdido':0,'valor_apostado':0, 'empresas':[], 'Time_loot': datetime.min, 'Last_time':datetime.min, 'xp': 0, 'lvl': 0, 'mp': 0})

async def user_get(guildID : int, userID : int, field : str):
    await create_account(guildID, userID)
    collection = db[str(guildID)]
    try:
        return collection.find_one({'_id': userID})[field]
    except:
        return None
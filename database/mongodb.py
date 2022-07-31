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
        collection.insert_one({'_id': userID, 'coins': 0, 'banco': 0, 'valor_ganho': 0, 'valor_perdido':0,'valor_apostado':0, 'empresas':[], 'Time_loot': datetime.min, 'Last_time':datetime.min, 'xp': 0, 'lvl': 0, 'mp': 0, 'galo': {"nome": "galo","lvl":1, "xp": 0, "vida": 100, "dano": 10, "dodge": 0, "block": 0, "crit": 0}})

async def user_get(guildID : int, userID : int, field : str):

    await create_account(guildID, userID)
    collection = db[str(guildID)]
    
    try:
        return collection.find_one({'_id': userID})[field]
    except:
        return None

async def update_user(guildID : int, userID : int, field : str, val, updateType : str):

    await create_account(guildID, userID)
    collection = db[str(guildID)]

    if updateType == 'inc':
        collection.update_one({'_id': userID}, {'$inc': {field:val}})
    elif updateType == 'set':
        collection.update_one({'_id': userID}, {'$set':{field:val}})

async def checkGalo(guildId, userId):
    await create_account(guildId, userId)
    if not await user_get(guildId, userId, 'galo'):
        await update_user(guildId, userId, 'galo', {"nome": "galo","lvl":1, "xp": 0, "vida": 100, "dano": 10, "dodge": 0, "block": 0, "crit": 0}, 'set')

async def checkMoney(guildId, userId, value):

    if await user_get(guildId, userId, 'coins') < value:
        return False

    else:
        return True

async def lvlGalo(guildId, userId, value):

    galo = await user_get(guildId, userId, 'galo')
    lvl = galo['lvl']
    xp = galo['xp']
    xp += value
    xpmax = lvl * 40

    while True:

        if xp >= xpmax:
            xp -= xpmax
            lvl += 1
            xpmax = lvl * 40

        else:
            galo['lvl'] = lvl
            galo['xp'] = xp
            await update_user(guildId, userId, 'galo', galo, 'set')
            break

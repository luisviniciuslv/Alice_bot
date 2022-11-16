import os
from datetime import datetime
import random

from dotenv import load_dotenv
from errors.WrongWord import WrongWord
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("database_connection"))
db = client['AliceBot']
collection = db['Termo']


async def create_account(userID: int):
  if not collection.find_one({'_id': userID}):
    collection.insert_one(
      {'_id': userID, 'actual_word': None, 'attempts': 15, 'points': 0, 'words': []})

def generate_word(words_list: list):
  words = ['banana', 'quadro', 'batata', 'rosa', 'careca', 'cabelo', 'macaco']
  
  for word in words_list:
    words.remove(word)
  
  return random.choice(words)

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
    self.words = self.user['words']
    self.points = self.user['points']
    self.attempts = self.user['attempts']
    self.actual_word = self.user['actual_word']
    if self.actual_word == None:
      self.actual_word = generate_word(self.words)
      collection.update_one({'_id': self.userID}, {'$set': {'actual_word': self.actual_word}})
  @property
  def get(self):
    return self.user

  async def try_word(self, word):      
    if word == self.actual_word:
      points = self.attempts + 5
      self.words.append(word)
      self.actual_word = None
      self.attempts = 15
      self.points += points
      collection.update_one(
        {'_id': self.userID},
        {'$set': {
          'words': self.words,
          'actual_word': self.actual_word,
          'attempts': self.attempts,
          'points': self.points
          }
        }
      )
      return points
    else:
      if len(self.actual_word) != len(word):
        raise WrongWord(f'A palavra tem {len(self.actual_word)} letras')
      
      correct_letters = []
      for i in range(len(self.actual_word)):
        if word[i] == self.actual_word[i]:
          correct_letters.append('🟢')
        elif word[i] in self.actual_word:
          correct_letters.append('🟡')
        else:
          correct_letters.append('🔴')

      correct_letters = ''.join(correct_letters)
      msg = f'{word} | {correct_letters} \nTentativas restantes: {self.attempts}'
      self.attempts -= 1
      collection.update_one(
        {'_id': self.userID},
        {'$set': {
          'attempts': self.attempts
        }
        }
      )
      
      raise WrongWord(msg)

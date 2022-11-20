import random
import sqlite3

from errors.WrongWord import WrongWord

banco = sqlite3.connect('database.db')
cursor = banco.cursor()

def create_account(userID: int):
  cursor.execute('CREATE TABLE IF NOT EXISTS users (id int, actual_word text, attempts int, points int)')
  cursor.execute('SELECT * FROM users WHERE id = ?', (userID,))
  if not cursor.fetchone():
    cursor.execute('INSERT INTO users VALUES(?, null, 15, 0)', (userID,))
    banco.commit()

def generate_word():
  words = ['banana', 'quadro', 'batata', 'rosa', 'careca', 'cabelo', 'macaco']  
  return random.choice(words)

class Termo:
  def __init__(self, userID):
    self.userID = userID
    create_account(self.userID)
    banco.commit()
    self.user = cursor.execute('SELECT * FROM users WHERE id = ?', (self.userID,)).fetchone()

    self.actual_word = self.user[1]
    self.attempts    = self.user[2]
    self.points      = self.user[3]

    if self.actual_word == None:
      self.actual_word = generate_word()
      cursor.execute('UPDATE users SET actual_word = ? WHERE id = ?', (self.actual_word, self.userID))
      banco.commit()

  @property
  def ranking(self):
    return cursor.execute('SELECT * FROM users ORDER BY points DESC').fetchall()[0:11]
  
  @property
  def get(self):
    return self.user

  async def try_word(self, word):      
    if word == self.actual_word:
      points = self.attempts + 5
      self.actual_word = None
      self.attempts = 15
      self.points += points
      cursor.execute('UPDATE users SET actual_word = ?, attempts = ?, points = ? WHERE id = ?', (self.actual_word, self.attempts, self.points, self.userID))
      banco.commit()
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
      cursor.execute('UPDATE users SET attempts = ? WHERE id = ?', (self.attempts, self.userID))
      banco.commit()
      raise WrongWord(msg)

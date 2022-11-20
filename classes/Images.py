import sqlite3

banco = sqlite3.connect('database.db')
cursor = banco.cursor()

class Images:
  def __init__(self, userID):
    self._userID = userID
    cursor.execute('CREATE TABLE IF NOT EXISTS images (user_id int, link text, tags text, likes int)')
    banco.commit()
    
  def register(self, link, tags):
    cursor.execute('INSERT INTO images VALUES(?, ?, ?, 0)', (self._userID, link, tags))
    banco.commit()
  
  def get_by_user(self, userID):
    cursor.execute('SELECT * FROM images ORDER BY likes DESC WHERE user_id = ?', (userID))
    return cursor.fetchall()
  
  def delete(self, link):
    cursor.execute('DELETE FROM images WHERE link = ?', (link))
    banco.commit()
    
  def register_like(self, link):
    cursor.execute('UPDATE images SET likes = likes + 1 WHERE link = ?', (link))
    banco.commit()
  
  @property
  def get_all_user_images(self):
    cursor.execute('SELECT * FROM images WHERE user_id = ?', (self._userID))
    return cursor.fetchall()

  def list_by_tag(self, tag):
    cursor.execute('SELECT * FROM images WHERE tags LIKE ?', (f'%{tag}%'))
    return cursor.fetchall()

  
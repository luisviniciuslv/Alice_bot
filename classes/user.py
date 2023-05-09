import sqlite3
from datetime import datetime


class Repository:
  def __init__(self, id):
    self.banco = sqlite3.connect('usuarios.db')
    self.cursor = self.banco.cursor() 
    self.cursor.execute('CREATE TABLE IF NOT EXISTS usuarios (id text, banco int, carteira int, total_ganho int, total_perdido int)')
    self.cursor.execute(f'INSERT INTO usuarios IF NOT EXISTS (id, banco, carteira, total_ganho, total_perdido) VALUES ({id}, 0, 0, 0, 0)')
    self.banco.commit()
    self.user: User = self.cursor.execute(f'SELECT * FROM usuarios WHERE id = {id}').fetchone()
    
  def adicionar_banco(self, valor):
    self.cursor.execute(f'UPDATE usuarios SET banco = {self.banco + valor} WHERE id = {self.id}')
    self.banco.commit()
    
  def adicionar_cart(self, valor):
    self.cursor.execute(f'UPDATE usuarios SET carteira = {self.carteira + valor} WHERE id = {self.id}')
    self.banco.commit()
    
  def sacar_banco(self, valor):
    if self.user.banco < valor:
      return False
    self.cursor.execute(f'UPDATE usuarios SET banco = {self.banco - valor} WHERE id = {self.id}')
    self.cursor.execute(f'UPDATE usuarios SET carteira = {self.carteira + valor} WHERE id = {self.id}')
    self.banco.commit()
    
  def depositar_banco(self, valor):
    if self.user.carteira < valor:
      return False
    self.cursor.execute(f'UPDATE usuarios SET carteira = {self.carteira - valor} WHERE id = {self.id}')
    self.cursor.execute(f'UPDATE usuarios SET banco = {self.banco + valor} WHERE id = {self.id}')
    self.banco.commit()

class User:
  def __init__(self, id):
    self.repository = Repository(id)
    self.id = id
    self.banco = self.repository.user[1]
    self.carteira = self.repository.user[2]
    self.total_ganho = self.repository.user[3]
    self.total_perdido = self.repository.user[4]

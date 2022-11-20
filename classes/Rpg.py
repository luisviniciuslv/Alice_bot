
import json
import sqlite3

import discord

banco = sqlite3.connect('database.db')
cursor = banco.cursor()

class SelectTypeInventory(discord.ui.Select):
    def __init__(self, id):
      self.id = id
      options = [
        discord.SelectOption(label="Armas", value="weapons", description=f"Abra o inventário de armas"),
        discord.SelectOption(label="Armaduras", value="armors", description=f"Abra o inventário de armaduras"),
        ]
      
      super().__init__(placeholder="Escolha um item para equipar",max_values=1,min_values=1,options=options)

    async def callback(self, interaction: discord.Interaction):
      if self.id == interaction.user.id:
          
        game = Rpg(interaction.user.id)
        
        if self.values[0] == "weapons":
          weapons = json.load(open('items/weapons.json', 'r'))
          weapons_inventory_id = game.get_weapons()
          weapons_inventory = []
          for i in weapons:
            if str(i["id"]) in weapons_inventory_id:
              weapons_inventory.append(i)
          if not weapons:
            return await interaction.response.send_message("Você não tem armas para equipar.")
          embed = discord.Embed(title="Inventário de armas", description=f"inventario de {interaction.user.mention}")
          for i in weapons_inventory:
            embed.add_field(name=i['name'], value=f"Tier: {i['tier']}\nDano: {i['damage']}\nValor: {i['price']}", inline=False)
          await interaction.response.send_message(embed=embed)
          
        if self.values[0] == "armors":
          
          armors = json.load(open('items/armors.json', 'r'))   
          armors_inventory_id = game.get_armors()
          armors_inventory = []
          
          for i in armors:
            if str(i["id"]) in armors_inventory_id:
              armors_inventory.append(i)
              
          if not armors:
            return await interaction.response.send_message("Você não tem armaduras para equipar.")
          embed = discord.Embed(title="Inventário de armaduras", description=f"inventario de {interaction.user.mention}")
          for i in armors_inventory:
            embed.add_field(name=i['name'], value=f"Tier: {i['tier']}\nDefesa: {i['defense']}\nValor: {(int(i['tier'])+1* int(i['tier'])) * (int(i['defense']) *3)}", inline=False)
          await interaction.response.send_message(embed=embed)
        else:
          pass
class SelectViewTypeInventory(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=30)
        self.add_item(SelectTypeInventory(ctx.author.id))





class SelectEquip(discord.ui.Select):
    def __init__(self, itens):
      options = []
      if itens[0]["type"]  == 'weapon':
        self.option = "weapon"
        for i in itens:
          options.append(discord.SelectOption(label=i['name'], value=i['id'], description=f"dano {i['damage']}"))
          
      if itens[0]["type"] == 'armor':
        self.option = "armor"
        for i in itens:
          options.append(discord.SelectOption(label=i['name'], value=i['id'], description=f"defesa {i['defense']}"))
          
      super().__init__(placeholder="Escolha um item para equipar",max_values=1,min_values=1,options=options)
      
    async def callback(self, interaction: discord.Interaction):
      game = Rpg(interaction.user.id)
      if self.option == "weapon":
        game.set_weapon(self.values[0])
      if self.option == "armor":
        game.set_armor(self.values[0])
      await interaction.response.send_message(content=f"Você equipou o item de id {self.values[0]}!",ephemeral=False)

class SelectViewEquip(discord.ui.View):
    def __init__(self, ctx, itens):
        super().__init__(timeout=30)
        self.add_item(SelectEquip(itens))

class Rpg:
  def __init__(self, userID):
    cursor.execute('CREATE TABLE IF NOT EXISTS rpg (id int, level int, xp int, money int, armors text, weapons text, armor text, weapon text)')
    cursor.execute('SELECT * FROM rpg WHERE id = ?', (userID,))
    if not cursor.fetchone():
      cursor.execute('INSERT INTO rpg VALUES(?, 1, 0, 0, null, null, 11, 21)', (userID,))
      banco.commit()
    self.user = cursor.execute('SELECT * FROM rpg WHERE id = ?', (userID,)).fetchone()
    self.userID = userID
    self.level = self.user[1]
    self.xp = self.user[2]
    self.money = self.user[3]
    self.armors = str(self.user[4])
    self.weapons = str(self.user[5])
    self.armor = str(self.user[6])
    self.weapon = str(self.user[7])
    self.xp_to_next_level = self.level * 100
  @property
  def get(self):
    return self.user

  def add_xp(self, xp):
    self.xp += xp
    if self.xp >= self.level * 100:
      self.level += 1
      self.xp = 0
    cursor.execute('UPDATE rpg SET level = ?, xp = ? WHERE id = ?', (self.level, self.xp, self.userID))
    banco.commit()
    
  def add_money(self, money):
    self.money += money
    cursor.execute('UPDATE rpg SET money = ? WHERE id = ?', (self.money, self.userID))
    banco.commit()

  def remove_money(self, money):
    self.money -= money
    cursor.execute('UPDATE rpg SET money = ? WHERE id = ?', (self.money, self.userID))
    banco.commit()
    
  def add_item(self, item, type):
    if type == 'armor':
      if self.armors == None:
        self.armors = item
      self.armors += f', {item}'
      cursor.execute('UPDATE rpg SET armors = ? WHERE id = ?', (self.armors, self.userID))
      banco.commit()
      
    elif type == 'weapon':
      if self.weapons == None:
        self.weapons = item
      self.weapons += f', {item}'
      
      cursor.execute('UPDATE rpg SET weapons = ? WHERE id = ?', (self.weapons, self.userID))
      banco.commit()

  def remove_item(self, item, type):
    if type == 'armor':
      self.armors = self.armors.replace(f', {item}', '')
      cursor.execute('UPDATE rpg SET armors = ? WHERE id = ?', (self.armors, self.userID))
      banco.commit()
       
    elif type == 'weapon':
      self.weapons = self.weapons.replace(f', {item}', '')
      cursor.execute('UPDATE rpg SET weapons = ? WHERE id = ?', (self.weapons, self.userID))
      banco.commit()
    
  def has_item(self, item, type):
    if type == 'armor':
      return item in self.armors.split(', ')
    elif type == 'weapon':
      return item in self.weapons.split(', ')

  def get_weapons(self):
    return self.weapons.split(', ')
  def get_armors(self):
    return self.armors.split(', ')
  
  def set_armor(self, armor):
    if self.have_armor():
      self.armors += f', {self.armor}'
      self.armor = None
      cursor.execute('UPDATE rpg SET armors = ? WHERE id = ?', (self.armors, self.userID))
      banco.commit()

    self.armors = self.armors.replace(f', {armor}', '')
    self.armor = armor
    cursor.execute('UPDATE rpg SET armors = ? WHERE id = ?', (self.armors, self.userID))
    cursor.execute('UPDATE rpg SET armor = ? WHERE id = ?', (armor, self.userID))
    banco.commit()
    
  def remove_armor(self):
    self.armors += f', {self.armor}'
    cursor.execute('UPDATE rpg SET armor = ? WHERE id = ?', (self.armor, self.userID))
    cursor.execute('UPDATE rpg SET armors = ? WHERE id = ?', (self.armors, self.userID))
    banco.commit()
    
  def have_armor(self):
    return self.armor != None
  
  def set_weapon(self, weapon):
    if self.have_weapon():
      self.weapons += f', {self.weapon}'
      self.weapon = None
      cursor.execute('UPDATE rpg SET weapons = ? WHERE id = ?', (self.weapons, self.userID))
      banco.commit()
    
    self.weapons = self.weapons.replace(f', {weapon}', '')
    self.weapon = weapon
    cursor.execute('UPDATE rpg SET weapons = ? WHERE id = ?', (self.weapons, self.userID))
    cursor.execute('UPDATE rpg SET weapon = ? WHERE id = ?', (weapon, self.userID))
    banco.commit()
    
  def remove_weapon(self):
    self.weapons += f', {self.weapon}'
    self.weapon = None
    cursor.execute('UPDATE rpg SET weapon = ? WHERE id = ?', (self.weapon, self.userID))
    cursor.execute('UPDATE rpg SET weapons = ? WHERE id = ?', (self.weapons, self.userID))
    banco.commit()
  
  def have_weapon(self):
    return self.weapon != None

  @property
  def get_weapon(self):
    return self.weapon
  
  @property
  def get_armor(self):
    return self.armor
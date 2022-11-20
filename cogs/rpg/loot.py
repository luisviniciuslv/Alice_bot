
import json
import random

import discord
from classes.Rpg import Rpg
from discord.ext import commands


class Loot(commands.Cog):
  def __init__(self, client):
    self.client = client
  # time to loot 
  @commands.hybrid_command(
    name="loot",
    description="Saia para lootear e encontre itens.",
    aliases=["l"]
  ) 
  @commands.cooldown(1, 900, commands.BucketType.user)
  async def loot(self, ctx: commands.Context):
    game = Rpg(ctx.author.id)
    
    swords = json.load(open('items/weapons.json', 'r'))
    armors = json.load(open('items/armors.json', 'r'))    
    tier = random.randint(1, 1000)
    
    if tier <= 500:
      tier = 1
    elif tier <= 800:
      tier = 2
    elif tier <= 900:
      tier = 3
    elif tier <= 950:
      tier = 4  
    else:
      tier = 5
      
    swords = [sword for sword in swords if sword['tier'] == tier]
    armors = [armor for armor in armors if armor['tier'] == tier]
    
    sword = random.choice(swords)
    armor = random.choice(armors)

    item = random.choice([sword, armor])
    
    embed = discord.Embed(title="Loot", description=f"Você encontrou o item")
    embed.add_field(name="Nome", value=item['name'])
    embed.add_field(name="Tier", value=item['tier'])
    if item['type'] == 'weapon':
      embed.add_field(name="Dano", value=item['damage'])
      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1000862872194265088/1043347196445216778/Pngtreebronze_sword_cartoon_illustration_4621258.png")
    if item['type'] == 'armor':
      embed.add_field(name="Defesa", value=item['defense'])
      embed.set_image(url="https://www.pngall.com/wp-content/uploads/4/Armor-PNG-Images.png")

    await ctx.send(embed=embed)
    game.add_item(item["id"], item["type"])
    
 
    
  
async def setup(client):
  await client.add_cog(Loot(client))

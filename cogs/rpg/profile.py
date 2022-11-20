
import json

import discord
from classes.Rpg import Rpg
from discord.ext import commands


class Profile(commands.Cog):
  def __init__(self, client):
    self.client = client
  # time to loot 
  @commands.hybrid_command(
    name="perfil",
    description="Saia para lootear e encontre itens.",
    aliases=["profile", "p"]
  ) 
  async def profile(self, ctx: commands.Context, member: discord.Member = None):
    
    if member == None:
      member = ctx.author
      
    game = Rpg(member.id)
    weapon = game.weapon
    armor = game.armor
    
    for i in json.load(open('items/weapons.json', 'r')):
      if str(i["id"]) == weapon:
        weapon = i
        break
    
    for i in json.load(open('items/armors.json', 'r')):
      if str(i["id"]) == armor:
        armor = i
        break
    
    embed = discord.Embed(
      title=f"Perfil de {member.name}", 
      description=f"**Level:** {game.level}\n**XP:** {game.xp}/{game.xp_to_next_level}\n**Dinheiro:** {game.money}")
    
    embed.add_field(name="Arma", value=f'{weapon["name"]}\ntier: {weapon["tier"]}\ndano: {weapon["damage"]}', inline=False)
    embed.add_field(name="Armadura", value=f'{armor["name"]}\ntier: {armor["tier"]}\ndefesa: {armor["defense"]}', inline=False)
    
    embed.set_thumbnail(url=member.avatar)
    await ctx.send(embed=embed)

async def setup(client):
  await client.add_cog(Profile(client))

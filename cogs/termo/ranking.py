
import discord
from discord import app_commands
from discord.ext import commands
from classes.Termo import Termo


class TermoRanking(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(aliases=['rank', 'ranking', 'top'])
  async def Ranking(self, ctx: commands.Context):
    user = Termo(ctx.author.id) 
    embed = discord.Embed(title='Ranking', color=0x00ff00)
    for i, user in enumerate(user.ranking):
      embed.add_field(name=f'{i+1}º', value=f'<@{user[0]}> - {user[3]} pontos', inline=False)
    await ctx.send(embed=embed)
    
async def setup(client):
  await client.add_cog(TermoRanking(client))  

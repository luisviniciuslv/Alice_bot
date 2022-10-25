
import discord
from discord.ext import commands
import os

class Reload(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.has_guild_permissions(administrator=True)
  @commands.command()
  async def reload(self, ctx):
    for i in os.listdir('./cogs'):
      for e in os.listdir(f'./cogs/{i}'):
        if str(e).startswith('__py'):
          pass
        else:
          self.client.reload_extension(f'cogs.{i}.{e[:-3]}')
          print('loaded ', e)
    await ctx.send('Bot reloaded!')

def setup(client):
    client.add_cog(Reload(client))

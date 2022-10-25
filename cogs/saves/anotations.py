from ast import alias
import string
import discord
from discord.ext import commands
from datetime import datetime
from utils.database import new_anotation
class Anotations(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(aliases=['anotar'])
  async def new_anotation(self, ctx, *, anotation):
    await new_anotation(ctx.author.id, anotation)
    await ctx.send(f'Anotação adicionada com sucesso!')
  
def setup(client):
    client.add_cog(Anotations(client))
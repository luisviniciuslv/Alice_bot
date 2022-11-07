
import discord
from discord import app_commands
from discord.ext import commands
from utils.User import User

class Termo(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @app_commands.command(name='termo', description='Joguinho de acertar a palavra :)')
  async def termo(self, interaction: discord.Interaction, word:str):
    user = await User(interaction.user.id)
    
    print(user.get)

async def setup(client):
  await client.add_cog(Termo(client))

import discord
from discord import app_commands
from discord.ext import commands

from cogs.BBB.classes.brother import Brother
from cogs.BBB.classes.game import Game

from utils.generate import get_event_image

class BBB(commands.Cog):
  def __init__(self, client):
    self.client = client
    self.games = {}
    
  @app_commands.command(name='bbb', description='Coloque seus amigos na casa mais vigiada do Brasil :)')
  async def bbb(self, interaction: discord.Interaction, *, args: str):
    if interaction.guild.id in self.games:
      await interaction.response.send_message('Já existe um jogo em andamento neste servidor!', ephemeral=True)
      return

    brothers = []

    for member in args.split(' '):
      if member.startswith('<@') and member.endswith('>'):
        id = member[2:-1]

        if member.startswith('!'):
          id = member[1:]

      user = await self.client.fetch_user(id)

      brothers.append(Brother(user.id, user.name, f"{user.avatar}"))

    self.games[interaction.guild.id] = Game(brothers)

    week_events = self.games[interaction.guild.id].create_week_events()

    for event in week_events:
      arr = get_event_image(event[0], event[1])
      file = discord.File(arr, filename="events.png")
      await interaction.channel.send(file=file)

async def setup(client):
  await client.add_cog(BBB(client))
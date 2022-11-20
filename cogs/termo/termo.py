
import discord
from classes.Termo import Termo
from discord import app_commands
from discord.ext import commands
from errors.WrongWord import WrongWord


class Termo(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @app_commands.command(name='termo', description='Joguinho de acertar a palavra :)')
  async def termo(self, interaction: discord.Interaction, word:str):
    user = Termo(interaction.user.id)
    
    try:
      points = await user.try_word(word)
      await interaction.response.send_message(f'Você acertou a palavra! ganhou {points} pontos no ranking', ephemeral=False)
    except WrongWord as e:
      await interaction.response.send_message(f'{e}', ephemeral=False)

  @commands.command()
  async def palavra(self, ctx: commands.Context):
    user = Termo(ctx.author.id) 
    await ctx.send(f'A palavra tem {len(user.actual_word)} letras!')
    
async def setup(client):
  await client.add_cog(Termo(client))

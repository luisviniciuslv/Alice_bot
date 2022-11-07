import datetime
import discord
from discord import app_commands
from discord.ext import commands
import pytz

from utils.database import update_user, user_get

class Reward(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @app_commands.command(name='recompensa', description='Recebe uma recompensa diária')
  async def Reward(self, interaction: discord.Interaction):
    current_time = datetime.datetime.now(pytz.timezone('America/Santarem')).replace(microsecond=0, tzinfo=None)
    last_reward_time = await user_get(interaction.user.id, 'last_reward_time')
    print(abs(current_time - last_reward_time))
    if abs(current_time - last_reward_time) > datetime.timedelta(minutes=1):
      pass
    else:
      await interaction.response.send_message('Você já recebeu sua recompensa diária!', ephemeral=True)
      return await interaction.channel.send('espere {} para receber sua próxima recompensa'.format(abs(current_time - last_reward_time)))
    await interaction.response.send_message('Você recebeu sua recompensa diária!', ephemeral=True)
    await update_user(interaction.user.id, 'money', 100, 'inc')
    await update_user(interaction.user.id, 'last_reward_time', current_time, 'set')
async def setup(client):
  await client.add_cog(Reward(client))
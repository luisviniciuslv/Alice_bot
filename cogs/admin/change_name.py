import discord
from discord import app_commands
from discord.ext import commands


class ChangeName(commands.Cog):
  def __init__(self, client):
    self.client = client

  @app_commands.command(name='nick', description='Muda o nickname de um usuário no servidor')
  async def change_nick(self, interaction: discord.Interaction, member: discord.Member, novo_nickname: str):
    if not interaction.user.guild_permissions.change_nickname:
      await interaction.response.send_message('Você não tem permissão para executar esse comando!', ephemeral=True)
      return
    
    if len(novo_nickname) > 32:
      return await interaction.response.send_message('O nickname deve ter no máximo 32 caracteres', ephemeral=True)
    try:
      await member.edit(nick=novo_nickname)
      await interaction.response.send_message(f'Nickname de {member.mention} alterado para ``{novo_nickname}``')
    except discord.Forbidden:
      await interaction.response.send_message('Eu não tenho permissão para mudar o nickname nesse servidor, por favor me de um cargo!', ephemeral=True)
async def setup(client):
  await client.add_cog(ChangeName(client))

from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands


class History(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @app_commands.command(name='history', description='Get the history of a user')
  async def history(self, interaction: discord.Interaction, member:Optional[discord.Member] = None):
    if(member == None): member = interaction.user
    comandos_musica = [".p", "m!p"]
    comandos_musica_counter = 0
    xingamentos = ["porra", "caralho", "cu", "crl", "vsf", "fuder", "fude", "bct", "buceta", "viado", "vsfd", "pqp", "puta", "fdp", "cuzao", "cz", "cuzão"]
    xingamentos_counter = 0
    racista = False
    counter = 0
    await interaction.response.send_message(f'Contando mensagens de {member.mention}, (isso pode demorar um pouquinho)')
    for channel in self.client.get_all_channels():
      if str(channel.type) == 'text':
        async for message in channel.history(limit=None):
          if message.author == member:
            counter += 1 
            
            # Contar xingamentos
            for i in xingamentos:
              if i in message.content.lower():
                for j in message.content.lower().split(" "):
                  for k in xingamentos:
                    if j == k:
                      xingamentos_counter += 1
                    
            if "preto" in message.content.lower() or "macaco" in message.content.lower() or "pretos" in message.content.lower():
              racista = True
            
            # Contar músicas
            for i in comandos_musica:
              if i in message.content.lower():
                comandos_musica_counter += 1

    if(racista == True): racista = "Sim"
    else: racista = "Não"
    
    embed=discord.Embed(title="Total de mensagens", description=counter, color=0x00ff4c)
    embed.set_author(name=str(member), icon_url=member.avatar)
    embed.add_field(name="Xingamentos", value=xingamentos_counter, inline=False)
    embed.add_field(name="Pedidos de musica", value=comandos_musica_counter, inline=False)
    embed.add_field(name="É racista?", value=racista, inline=False)
      
    await interaction.followup.send(embed=embed)
    try:
      await interaction.user.send(embed=embed)
    except:
      pass
    
    
async def setup(client):
  await client.add_cog(History(client))

import unicodedata
from pydoc import stripid

import dataframe_image as dfi
import discord
import pandas as pd
import seaborn as sns
from discord import app_commands
from discord.ext import commands


class Tabela(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  
  @app_commands.command(name='tabela_mensagens', description='Cria uma tabela com os dados que você quiser')
  async def tabela_mensagens(self, interaction: discord.Interaction):
    await interaction.response.send_message('Criando tabela, aguarde!', ephemeral=True)
    def normalize_text(text):
      formatted_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8').strip()
      return formatted_text
    if not interaction.user.guild_permissions.administrator:
      await interaction.followup.send('Você não tem permissão para executar esse comando!', ephemeral=True)
      return
    data = {
      "Usuário": [],
      "Mensagens": [],
    }
    index = []
    count = 0
    embed = discord.Embed(title="Tabela de mensagens", description="acompanhamento", color=0x00ff4c)
    embed.set_author(name="Bot", icon_url=self.client.user.avatar)
    embed.add_field(name="Aguarde", value="Estou contando as mensagens de todos os usuários", inline=False)
    embed.add_field(name="já registrei aproximadamente", value=f"{count} mensagens", inline=False)
    
    try:
      msg = await interaction.user.send(embed=embed)
    except:
      msg = await interaction.followup.send(embed=embed)
      
    aux = False
    for channel in interaction.guild.channels:
      if channel.type == discord.ChannelType.text:
        async for message in channel.history(limit=None):
          if aux == True:
            break
          if count in range(0, 1000000, 1000):
            embed.set_field_at(1, name="já registrei aproximadamente", value=f"{count} mensagens", inline=False)
            await msg.edit(embed=embed)
          if count > 1000000:
            aux = True
            break

          name = normalize_text(message.author.name)
          if name == "":
            name = message.author.id
          count += 1
          print(count)
          if message.author.bot:
            print("bot")
          elif name in data["Usuário"]:
            data["Mensagens"][data["Usuário"].index(name)] += 1
          else:
            data["Usuário"].append(name)
            data["Mensagens"].append(1)
            index.append(message.author.id)
            print("adicionando: ", name)
      if aux == True:
        break
  
    import json
    channels = interaction.guild.channels
    with open ("channels.json", "w") as f:
      json.dump(channels, f)    

    df = pd.DataFrame(data=data, index=index)
    df.sort_values(by=['Mensagens'], inplace=True, ascending=False)
    
    #create folder
    import os
    if not os.path.exists('tabelas'):
      os.makedirs('tabelas')
    if not os.path.exists(f'tabelas/{interaction.guild.id}'):
      os.makedirs(f'tabelas/{interaction.guild.id}')

    # create file
    df.to_csv(f'tabelas/{interaction.guild.id}/{interaction.guild.name}.csv', index=False)
    df.to_excel(f'tabelas/{interaction.guild.id}/{interaction.guild.name}.xlsx', index=False)
    dfi.export(obj=df, max_rows=10, filename=f'tabelas/{interaction.guild.id}/{interaction.guild.name}.png')
    
    # create discord file
    csv = discord.File(f'tabelas/{interaction.guild.id}/{interaction.guild.name}.csv')
    png = discord.File(f'tabelas/{interaction.guild.id}/{interaction.guild.name}.png')
    xlsx = discord.File(f'tabelas/{interaction.guild.id}/{interaction.guild.name}.xlsx')
    
    # send csv file 
    await interaction.channel.send(file=csv)
    await interaction.channel.send(file=png)
    await interaction.channel.send(file=xlsx)
    
    csv = discord.File(f'tabelas/{interaction.guild.id}/{interaction.guild.name}.csv')
    png = discord.File(f'tabelas/{interaction.guild.id}/{interaction.guild.name}.png')
    xlsx = discord.File(f'tabelas/{interaction.guild.id}/{interaction.guild.name}.xlsx')
    
    await interaction.user.send(file=csv)
    await interaction.user.send(file=png)
    await interaction.user.send(file=xlsx)
    
    table = pd.read_csv(f'tabelas/{interaction.guild.id}/{interaction.guild.name}.csv')
    total_messages = table['Mensagens'].sum()
    total_first = table['Mensagens'][0]
    total_second = table['Mensagens'][1]
    total_third = table['Mensagens'][2]
    total_rest = total_messages - total_first - total_second - total_third

    user1 = table['Usuário'][0]
    user2 = table['Usuário'][1]
    user3 = table['Usuário'][2]

    data = {
      "Usuário": [user1, user2, user3, 'Resto'],
      "Mensagens": [total_first, total_second, total_third, total_rest]
    }
    
    df = pd.DataFrame(data)
    png = sns.barplot(x='Usuário', y='Mensagens', data=df)
    png.figure.savefig(f'tabelas/{interaction.guild.id}/{interaction.guild.name}_barplot.png')
    
    png = discord.File(f'tabelas/{interaction.guild.id}/{interaction.guild.name}_barplot.png')
    await interaction.channel.send(file=png)
    
    png = discord.File(f'tabelas/{interaction.guild.id}/{interaction.guild.name}_barplot.png')
    await interaction.user.send(file=png)
    
    # delete paste
    import shutil
    shutil.rmtree(f'tabelas/{interaction.guild.id}')
async def setup(client):
  await client.add_cog(Tabela(client))

import json

import discord
import requests
from discord import app_commands
from discord.ext import commands


class Valorant(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @app_commands.command(name='valorant', description='pega informações da sua conta no valorant')
  async def valorant(self, interaction: discord.Interaction, nome: str, tag: str):
    await interaction.response.send_message("Aguarde, estamos processando as informações...")
    response = requests.get(f"https://api.henrikdev.xyz/valorant/v1/account/{nome}/{tag}")
    data = response.content
    if json.loads(data)['status'] != 200:
      return await interaction.followup.send("Não foi possível encontrar a conta, tente novamente.")
    
    region = json.loads(data)['data']['region']
    level = json.loads(data)['data']['account_level']
    card = json.loads(data)['data']['card']['small']
    puuid = json.loads(data)['data']['puuid']
    response = requests.get(f"https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr/{region}/{puuid}")
    
    rank = json.loads(response.content)['data']['currenttierpatched']
    rankImage = json.loads(response.content)['data']['images']['small']
    name = f"{nome}#{tag}"
    
    response =  requests.get(f"https://api.henrikdev.xyz/valorant/v3/matches/{region}/{nome}/{tag}")
    matches = json.loads(response.content)['data']
    kills = 0
    headshots = 0
    bodyshots = 0
    legshots = 0
    deaths = 0
    for match in matches:
        for player in match['players']['all_players']:
          if player['puuid'] == puuid:
            kills += player['stats']['kills']
            headshots += player['stats']['headshots']
            bodyshots += player['stats']['bodyshots']
            legshots += player['stats']['legshots']
            deaths += player['stats']['deaths']
    tiros_no_corpot = bodyshots + legshots
    porcentagem_headshots = round((headshots / tiros_no_corpot) * 100)
    embed=discord.Embed(title="Valorant", description="Ultimas 5 partidas", color=0x00b3ff)
    embed.set_author(name=f"{name}", icon_url=rankImage)
    embed.set_thumbnail(url=card)
    embed.add_field(name="Level", value=level, inline=True)
    embed.add_field(name="Rank", value=rank, inline=True)
    embed.add_field(name="** **", value="** **", inline=False)
    embed.add_field(name="**Ultimas 5 partidas**", value="** **", inline=False)
    embed.add_field(name="** **", value="** **", inline=False)
    embed.add_field(name=f"Kills: {kills}", value="** **", inline=False)
    embed.add_field(name=f"Mortes: {deaths}", value="** **", inline=False)
    embed.add_field(name="Disparos", value=f"Cabeça: {headshots}\nCorpo: {bodyshots}\nPerna: {legshots}", inline=False)
    embed.add_field(name="% Headshot", value=f"{porcentagem_headshots}%", inline=False)
    await interaction.followup.send(embed=embed)
    
async def setup(client):  
  await client.add_cog(Valorant(client))

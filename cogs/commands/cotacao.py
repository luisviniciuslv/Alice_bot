from discord.ext import commands
import discord
from discord import app_commands
from discord.ext import commands
import forex_python.converter as converter
class CotacaoBot(commands.Cog):
  def __init__(self, client):
    self.client = client

  @app_commands.command()
  @app_commands.describe(moeda1="Moeda 1", moeda2="Moeda 2")
  async def cotacao(self, interaction: discord.Interaction, moeda1: str, moeda2:str):
    await interaction.response.send_message(f"Calculando...")
    try:
      valor1 = converter.CurrencyRates().get_rate(moeda1.upper(), 'USD')
      valor2 = converter.CurrencyRates().get_rate(moeda2.upper(), 'USD')
      await interaction.edit_original_response(content=f"1 {moeda1.upper()} equivale a {round(valor1 / valor2, 2)} {moeda2.upper()}")
    except:
      await interaction.edit_original_response(content=f"Não foi possível obter a cotação da moeda solicitada.")

async def setup(client):
  await client.add_cog(CotacaoBot(client))
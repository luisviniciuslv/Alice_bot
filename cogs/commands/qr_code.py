
import qrcode
import discord
from discord import app_commands
from discord.ext import commands


class QrCode(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @app_commands.command(name='qrcode', description='gerar um QR code com o texto ou link que você quiser')
  async def qrCode(self, interaction: discord.Interaction, texto_ou_link:str):
    image = qrcode.make(texto_ou_link)
    image.save("qr.png", "PNG")
    await interaction.response.send_message(file=discord.File("qr.png"))

async def setup(client):
  await client.add_cog(QrCode(client))
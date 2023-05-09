from discord.ext import commands
import requests
import random
import discord
import io

class Cat(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @commands.command(aliases=['sc' , 'catfact'])
  async def saycat(self, ctx, *, message):
    image = requests.get('https://cataas.com/cat/says/' + message + '?size=350&color=red').content
    await ctx.send(file=discord.File(io.BytesIO(image), 'cat.png'))
    
  @commands.command()
  async def cat(self, ctx):
    links = [
      'https://api.thecatapi.com/v1/images/search',
      'https://api.thecatapi.com/v1/images/search?mime_types=gif'
    ]
    cat = requests.get(random.choice(links)).json()
    await ctx.send(cat[0]['url'])
    
async def setup(client):
  await client.add_cog(Cat(client))
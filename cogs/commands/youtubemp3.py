from discord.ext import commands
import os
import discord
import pytube

class YtMp3(commands.Cog):
  def __init__(self, client):
    self.client = client

  @commands.command(aliasses=['mp3'])
  async def yt(self, ctx, link):
    yt = pytube.YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    video.download(output_path='./archives', filename=f'{video.title}.mp3')
    await ctx.send(file=discord.File(f'./archives/{video.title}.mp3'))
    os.remove(f'./archives/{video.title}.mp3')

async def setup(client):
  await client.add_cog(YtMp3(client))

import os

import discord
from discord.ext import commands

from config import config

class MyClient(commands.Bot):
  def __init__(self):
    super().__init__(
      command_prefix='!',
      intents=discord.Intents.all()
    )

  async def setup_hook(self):
    for i in os.listdir('./cogs'):
      for e in os.listdir(f'./cogs/{i}'):
        if str(e).endswith('.py'):
          print('loaded ', e)
          await client.load_extension(f'cogs.{i}.{e[:-3]}')

      # MY_GUILD = discord.Object(id=933020401632677888)
      # self.client.tree.copy_global_to(MY_GUILD)
      # await self.client.tree.sync(MY_GUILD)

intents = discord.Intents.all()
client = MyClient()

client.run(config['token_bot'])

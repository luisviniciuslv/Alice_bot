import os
from discord.ext import commands
from config import config

client = commands.Bot(command_prefix='!', case_insensitive=True)
client.remove_command('help')

for i in os.listdir('./cogs'):
  for e in os.listdir(f'./cogs/{i}'):
    if str(e).startswith('__py') or str(e).startswith('fonts') :
      pass
    else:
      print('loaded ', e)
      client.load_extension(f'cogs.{i}.{e[:-3]}')


client.run(config['token_bot'])
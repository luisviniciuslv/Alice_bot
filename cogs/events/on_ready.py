
import asyncio
from discord.ext import commands
import discord

class Ready(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('@================@')
        print('    BOT ONLINE    ')
        print('@================@')
        while True:
            await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name="so", type=3))
            await asyncio.sleep(1)
            await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name="foda", type=3))
            await asyncio.sleep(1)
def setup(client):
    client.add_cog(Ready(client))
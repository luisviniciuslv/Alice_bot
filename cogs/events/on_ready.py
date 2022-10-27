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
        
        count_members = self.client.get_guild(933020401632677888).member_count
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name=f'{count_members} members', type=3))
async def setup(client):
    await client.add_cog(Ready(client))
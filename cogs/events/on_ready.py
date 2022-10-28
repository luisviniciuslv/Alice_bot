from discord.ext import commands
import discord

class Ready(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        count_guilds = len(self.client.guilds)
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name=f'{count_guilds} servers!', type=3))

        for guild in self.client.guilds:
            print("sincronizando comandos em ", guild.name)
            # self.client.tree.copy_global_to(guild=discord.Object(id=guild.id))
            # await self.client.tree.sync(guild=discord.Object(id=guild.id))
            
        print('@================@')
        print('    BOT ONLINE    ')
        print('@================@')
        

async def setup(client):
    await client.add_cog(Ready(client))
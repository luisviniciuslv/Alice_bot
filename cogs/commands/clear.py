from discord.ext import commands

class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def clear(self, ctx):
        await ctx.channel.purge(limit=999999999999999)
        await ctx.message.delete()
        return
def setup(client):
    client.add_cog(Clear(client))

from discord.ext import commands
class OnMessage(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
      mensagens_racistas = ["preto", "pretos", "macaco", "pretinho", "macaquinho", "negro", "criolo"]
      for i in mensagens_racistas:
        if i in message.content:
          await message.channel.send(f"{message.author.mention} Não seja racista, respeite o proximo, filho da puta")
            
async def setup(client):
    await client.add_cog(OnMessage(client))
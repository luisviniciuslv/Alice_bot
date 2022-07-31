from discord.ext import commands

from database.mongodb import update_user, user_get
class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Criando comando 
    @commands.command(aliases=['NomeDoGalo'])
    async def setGaloName(self, ctx, name = None):

        # Verificando se o nome do galo foi passado
        if name == None:
            await ctx.send('Digite o nome do galo!')
        else:
            
            # Atualizando o nome do galo
            await ctx.send(f'O nome do galo foi alterado para {name}')
            galo = await user_get(ctx.guild.id, ctx.author.id, 'galo')
            galo['nome'] = name
            await update_user(ctx.guild.id, ctx.author.id, 'galo', galo, 'set')

def setup(client):
  client.add_cog(Profile(client))

from discord.ext import commands
import discord

from database.mongodb import checkGalo, user_get
class Galo(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=['CardDoGalo'])
    async def galo(self, ctx, user: discord.Member = None):

        # Definindo o usuário
        userId = ctx.author.id
        userName = ctx.author.name
        if user:
            userId = user.id    
            userName = user.name

        # Verificando se o usuário tem um Galo
        await checkGalo(ctx.guild.id, userId)

        # Pegando o Galo
        galo = await user_get(ctx.guild.id, userId, 'galo')

        # Criando a embed
        embed = discord.Embed(title="Galo de Briga", description=f"Galo do {userName}", color=0x4FABF7)
        embed.add_field(name="Nome do galo", value=galo['nome'], inline=False)
        embed.add_field(name="Nível do galo", value=galo['lvl'], inline=False)
        embed.add_field(name="Xp do galo", value=f"{galo['xp']}/{galo['lvl']*40}", inline=False)
        embed.add_field(name="Vida do galo", value=galo['vida'], inline=False)
        embed.add_field(name="Força do galo", value=galo['dano'], inline=False)
        embed.add_field(name="Chance de esquiva", value=f'{galo["dodge"]}%', inline=False)
        embed.add_field(name="Chance de critico", value=f'{galo["crit"]}%', inline=False)
        embed.add_field(name="Chance de bloqueio", value=f'{galo["block"]}%', inline=False)

        # Enviando a embed
        await ctx.channel.send(embed=embed)

def setup(client):
  client.add_cog(Galo(client))
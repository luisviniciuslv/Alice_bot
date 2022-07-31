import asyncio
import discord
from discord.ext import commands

from database.mongodb import checkMoney, user_get


class Rinha(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["battle"])
    async def rinha(self, ctx, aposta: int, member: discord.Member):

        # Verificando se o usuário marcou ele mesmo
        if member.id == ctx.author.id:
            await ctx.send(f"@{ctx.author.name}, seu galo não pode duelar contra ele mesmo.")
            return

        # Verificando se o usuário tem dinheiro
        if not await checkMoney(ctx.guild.id, member.id, aposta):
            await ctx.send(f'@{ctx.author.name}, @{member.name} não possui coins suficientes na carteira.')
            return

        # Criando a embed e enviando
        embed = discord.Embed(title="Rinha", description=f"**```{ctx.author.name} quer ter uma rinha de galo com {member.name}! Valendo {aposta}```\nPara aceitar basta reagir com ⚔**", color=0x4FABF7)
        embed.set_author(name=f"{ctx.author.name}", icon_url=f"{ctx.author.avatar_url}")
        msg = await ctx.channel.send(embed=embed)

        # Adicionando reação
        await msg.add_reaction('⚔')

        # Função para validar reações
        def check(reaction, user):
            return user != ctx.author and str(reaction.emoji) and user == member and str(reaction.emoji) == '⚔'
        while True:
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=20.0, check=check)
                print("caiu")
            except asyncio.TimeoutError:
                return await msg.delete()
    
def setup(client):
  client.add_cog(Rinha(client))

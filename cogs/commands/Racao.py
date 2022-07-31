import asyncio

import discord
from database.mongodb import checkGalo, checkMoney, lvlGalo, update_user
from discord.ext import commands


class Racao(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['ração', 'rações', 'racoes'])
    async def racao(self, ctx):

        # Checkando se o User tem um Galo
        await checkGalo(ctx.guild.id, ctx.author.id)

        # Abrindo e enviando a imagem
        img = discord.File(open('racoes.png', 'rb'))
        msg = await ctx.send(file=img)

        # Adicionando reações
        await msg.add_reaction('1️⃣')
        await msg.add_reaction('2️⃣')
        await msg.add_reaction('3️⃣')
        await msg.add_reaction('4️⃣')
        await msg.add_reaction('5️⃣') 

        # Função de verificação das reações
        def check(reaction, user):
            return user.id == ctx.author.id

        # Esperando a reação
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=20.0, check=check)

            escolhas = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
            dinheiro_requerido = [1000, 5000, 7000, 10000, 15000]
            xps = [1, 6, 8, 15, 20]

            for escolha, dinheiro, xp in zip(escolhas, dinheiro_requerido, xps):

                # Verificando se a reação é a correta
                if str(reaction.emoji) == escolha:

                    # Verificando se o usuário tem dinheiro
                    if not await checkMoney(ctx.guild.id, ctx.author.id, dinheiro):
                        await ctx.send(f'@{ctx.author.name}, você não tem dinheiro suficiente para comprar uma ração de {dinheiro} coins.')
                        return

                    # Atualizando o Galo
                    await ctx.send(f'{xp} de xp adicionado ao galo')
                    await lvlGalo(ctx.guild.id, ctx.author.id, xp)
                    await update_user(ctx.guild.id, ctx.author.id, 'coins', -dinheiro, 'inc')

        except asyncio.TimeoutError:
            return await msg.delete()

def setup(client):
  client.add_cog(Racao(client))

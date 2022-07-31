import asyncio

import discord
from database.mongodb import (checkGalo, checkMoney, lvlGalo, update_user)
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
            return user.id == ctx.author.id and str(reaction.emoji) == '1️⃣' or str(reaction.emoji) == '2️⃣' or str(reaction.emoji) == '3️⃣' or str(reaction.emoji) == '4️⃣' or str(reaction.emoji) == '5️⃣' and reaction.message.id == msg.id

        # Esperando a reação
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            return await msg.delete()

        # Quando reagir entra no while
        while True:
            aux = 1

            # Verificando se a pessoa que reagiu é o mesm que o author
            if user.id == ctx.author.id:
                
                # Verificando Reações
                if str(reaction.emoji) == '1️⃣':
                    # Verificando se tem dinheiro
                    if not await checkMoney(ctx.guild.id, ctx.author.id, 1000):
                        await ctx.send('Você não tem 1000$')
                        return
                    # Atualizando o Galo
                    await ctx.send('1 de xp adicionado ao galo')
                    await lvlGalo(ctx.guild.id, ctx.author.id, 1)
                    await update_user(ctx.guild.id, ctx.author.id, 'coins', -1000, 'inc')
                    return

                if str(reaction.emoji) == '2️⃣':
                    if not await checkMoney(ctx.guild.id, ctx.author.id, 5000):
                        await ctx.send('Você não tem 5000$')
                        return
                    await ctx.send('6 de xp adicionado ao galo')
                    await lvlGalo(ctx.guild.id, ctx.author.id, 6)
                    await update_user(ctx.guild.id, ctx.author.id, 'coins', -5000, 'inc')
                    return

                if str(reaction.emoji) == '3️⃣':
                    if not await checkMoney(ctx.guild.id, ctx.author.id, 7000 ):
                        await ctx.send('Você não tem 7000$')
                        return
                    await ctx.send('8 de xp adicionado ao galo')
                    await lvlGalo(ctx.guild.id, ctx.author.id, 8)
                    await update_user(ctx.guild.id, ctx.author.id, 'coins', -7000, 'inc')
                    return

                if str(reaction.emoji) == '4️⃣':
                    if not await checkMoney(ctx.guild.id, ctx.author.id, 10000):
                        await ctx.send('Você não tem 10000$')
                        return
                    await ctx.send('15 de xp adicionado ao galo')
                    await lvlGalo(ctx.guild.id, ctx.author.id, 15)
                    await update_user(ctx.guild.id, ctx.author.id, 'coins', -10000, 'inc')
                    return

                if str(reaction.emoji) == '5️⃣':
                    if not await checkMoney(ctx.guild.id, ctx.author.id, 15000):
                        await ctx.send('Você não tem 15000$')
                        return
                    await ctx.send('20 de xp adicionado ao galo')
                    await lvlGalo(ctx.guild.id, ctx.author.id, 20)
                    await update_user(ctx.guild.id, ctx.author.id, 'coins', -15000, 'inc')
                    return
                aux+=1
                if aux == 15:
                    await msg.delete()
                    return
            else:
                aux+=1
                if aux == 15:
                    await msg.delete()
                    return

def setup(client):
  client.add_cog(Racao(client))

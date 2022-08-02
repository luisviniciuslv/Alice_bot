import asyncio

import discord
from database.mongodb import checkGalo, checkMoney, lvlGalo, update_user
from discord.ext import commands


class Racao(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['ração', 'rações', 'racoes', 'raçoes'])
    async def racao(self, ctx):

        # Checkando se o User tem um Galo
        await checkGalo(ctx.guild.id, ctx.author.id)

        # Criando embed
        embed = discord.Embed(title="Ração de galo", description=f"** **", color=0x00ff00)

        nomes = ['1️⃣ Milho', '2️⃣ Milho protein', '3️⃣ Creatina', '4️⃣ Ração de combatente', '5️⃣ Whey milho verde']
        dinheiro_requerido = [250, 1350, 1800, 3500, 6000]
        xps = [1, 6, 8, 15, 30]

        for nome, dinheiro, xp in zip(nomes, dinheiro_requerido, xps):
            embed.add_field(name=nome, value=f"{xp} xp por {dinheiro}$", inline=True)
            embed.add_field(name="** **", value=f"** **", inline=False)

        msg = await ctx.send(embed=embed)

        # Adicionando reações
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        for i in reactions:
            await msg.add_reaction(i)

        # Função de verificação das reações
        def check(reaction, user):
            return user.id == ctx.author.id and str(reaction.emoji) in reactions

        # Esperando a reação
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=20.0, check=check)

            # Definindo reações e escolhas
            escolhas = reactions

            # Passando por reações e escolhas
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

        # Deletando a mensagem caso user não inserir uma reação
        except asyncio.TimeoutError:
            return await msg.delete()

def setup(client):
  client.add_cog(Racao(client))

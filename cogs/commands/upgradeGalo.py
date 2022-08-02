import asyncio
import discord
from database.mongodb import checkGalo, checkMoney, update_user, user_get
from discord.ext import commands


class UpgradeGalo(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Criando comando
    @commands.command(aliases=['galoStats', 'tunarGalo'])
    async def updateGalo(self, ctx):

        # Verificando se o usuário tem um Galo
        await checkGalo(ctx.guild.id, ctx.author.id)

        # Pegando o Galo  
        galo = await user_get(ctx.guild.id, ctx.author.id, 'galo')
        
        # Verificando se dodge é 0

        if galo['dodge'] == 0:
            dodge_preco = 500
        elif galo['dodge'] == 1:
            dodge_preco = 1000
        else:
            dodge_preco = galo['dodge'] * 500

        # Verificando se block é 0
        if galo['block'] == 0:
            block_preco = 500
        elif galo['block'] == 1:
            block_preco = 1000
        else:
            block_preco = galo['block'] * 500

        # Verificando se crit é 0
        if galo['crit'] == 0:
            crit_preco = 700
        elif galo['crit'] == 1:
            crit_preco = 1400
        else:
            crit_preco = galo['crit'] * 700

        # Definindo opções de embed
        names = ["1️⃣ Vida:", "2️⃣ Força:", "3️⃣ Taxa de desvio:", "4️⃣ Taxa de bloqueio:", "5️⃣ Taxa de acerto critico:"]
        values = [f"{galo['vida']} / {galo['lvl']*100}", f"{galo['dano']} / {galo['lvl']*10}", f"{galo['dodge']}% / {galo['lvl']*1}%", f"{galo['block']}% / {galo['lvl']*2}%", f"{galo['crit']}% / {galo['lvl']*5}%"]
        points = ["10 pontos", "10 pontos", "1 ponto", "1 ponto", "1 ponto"]
        prices = [{round(galo['vida']*1.5)}, {galo['dano']*15}, dodge_preco, block_preco, crit_preco]

        # Criando a embed
        embed = discord.Embed(title="Galo de Briga", description=f"{galo['nome']}", color=0x4FABF7)

        # Adicionando os campos baseado nas opções
        for name, value, point, price in zip(names, values, points, prices):
            embed.add_field(name=name, value=value, inline=True)
            embed.add_field(name="** **", value=f"{point} por {price}", inline=True)
            embed.add_field(name="** **", value=f"** **", inline=False)

        # Enviando a embed
        msg = await ctx.send(embed=embed)

        # Adicionando reações
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
        for i in reactions:
            await msg.add_reaction(i)

        # Função de verificação das reações
        def check(reaction, user):
            return user.id == ctx.author.id and str(reaction.emoji) in reactions

        try:
            # Esperando a reação
            reaction, user = await self.client.wait_for('reaction_add', timeout=20.0, check=check)

            # Definindo opções
            skills = ['vida', 'dano', 'dodge', 'block', 'crit']
            skillsPoints = [10, 10, 1, 1, 1]
            precos = [round(galo['vida']*1.5), galo['dano']*15, dodge_preco, block_preco, crit_preco]
            scales = [galo['lvl']*100, galo['lvl']*10, galo['lvl']*1, galo['lvl']*2, galo['lvl']*5]

            # Passando por todas as opções
            for escolha, skill, skillPoint, preco, scale in zip(reactions, skills, skillsPoints, precos, scales):

                #  Verificando escolha
                if str(reaction.emoji) == escolha:

                    # Verificando se ele pode comprar os pontos
                    if galo[skill] < scale:

                        # Verificando se ele tem dinheiro
                        if not await checkMoney(ctx.guild.id, ctx.author.id, preco):
                            await ctx.send(f"{ctx.author.mention} você não tem {preco}")
                            await msg.delete()
                            return

                        # Enviando mensagem avisando que a compra foi realizada
                        await ctx.send(f"{ctx.author.mention} você comprou {skillPoint} pontos de {skill} para seu galo")
                        await msg.delete()
                        # Cobrando dinheiro e adicionando os pontos
                        await update_user(ctx.guild.id, ctx.author.id, 'coins', -preco, 'inc')
                        galo[skill] += skillPoint
                        await update_user(ctx.guild.id, ctx.author.id, 'galo', galo, 'set')
                        return
                    else:
                        await ctx.send(f"{ctx.author.mention} você não pode comprar mais pontos de {skill}")
                        await msg.delete()
                        return
        # Deletando mensagem caso o usuário não escolha uma opção
        except asyncio.TimeoutError:
            return await msg.delete()

def setup(client):
  client.add_cog(UpgradeGalo(client))

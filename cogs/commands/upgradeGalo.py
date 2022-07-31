import asyncio
import discord
from database.mongodb import checkGalo, checkMoney, update_user, user_get
from discord.ext import commands


class UpgradeGalo(commands.Cog):
    def __init__(self, client):
        self.client = client

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

        # Criando a embed
        embed = discord.Embed(title="Galo de Briga", description=f"{galo['nome']}", color=0x4FABF7)
        embed.add_field(name="1️⃣ Vida:", value=f"{galo['vida']} / {galo['lvl']*100}", inline=True)
        embed.add_field(name="** **", value=f"10 pontos por {round(galo['vida']*1.5)}$", inline=True)
        embed.add_field(name="** **", value=f"** **", inline=False)
        embed.add_field(name="2️⃣ Força:", value=f"{galo['dano']} / {galo['lvl']*10}", inline=True)
        embed.add_field(name="** **", value=f"10 pontos por {galo['dano']*15}$", inline=True)
        embed.add_field(name="** **", value=f"** **", inline=False)
        embed.add_field(name="3️⃣ Porcentagem de esquiva:", value=f"{galo['dodge']}% / {galo['lvl']*1}%", inline=True)
        embed.add_field(name="** **", value=f"1 ponto por {dodge_preco}$", inline=True)
        embed.add_field(name="** **", value=f"** **", inline=False)
        embed.add_field(name="4️⃣ Porcentagem de bloqueio:", value=f"{galo['block']}% / {galo['lvl']*2}%", inline=True)
        embed.add_field(name="** **", value=f"1 ponto por {block_preco}$", inline=True)
        embed.add_field(name="** **", value=f"** **", inline=False)
        embed.add_field(name="5️⃣ Porcentagem de critico:", value=f"{galo['crit']}% / {galo['lvl']*5}%", inline=True)
        embed.add_field(name="** **", value=f"1 ponto por {crit_preco}$", inline=True)

        # Enviando a embed
        msg = await ctx.send(embed=embed)

        # Adicionando reações
        await msg.add_reaction('1️⃣')
        await msg.add_reaction('2️⃣')
        await msg.add_reaction('3️⃣')
        await msg.add_reaction('4️⃣')
        await msg.add_reaction('5️⃣')

        # Função de verificação das reações
        def check(reaction, user):
            return user.id == ctx.author.id and str(reaction.emoji) in ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']

        # Esperando a reação
        try:
            reaction, user = await self.client.wait_for('reaction_add', timeout=20.0, check=check)
        
            # Definindo opções 
            escolhas = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']
            skills = ['vida', 'dano', 'dodge', 'block', 'crit']
            skillsPoints = [10, 10, 1, 1, 1]
            precos = [round(galo['vida']*1.5), galo['dano']*15, dodge_preco, block_preco, crit_preco]
            scales = [galo['lvl']*100, galo['lvl']*10, galo['lvl']*1, galo['lvl']*2, galo['lvl']*5]

            # Passando por todas as opções
            for escolha, skill, skillPoint, preco, scale in zip(escolhas, skills, skillsPoints, precos, scales):

                #  Verificando escolha
                if str(reaction.emoji) == escolha:

                    # Verificando se ele pode comprar os pontos
                    if galo[skill] < scale:

                        # Verificando se ele tem dinheiro
                        if not await checkMoney(ctx.guild.id, ctx.author.id, preco):
                            await ctx.send(f"{ctx.author.mention} você não tem {preco}")
                            return

                        # Enviando mensagem avisando que a compra foi realizada
                        await ctx.send(f"{ctx.author.mention} você comprou {skillPoint} pontos de {skill} para seu galo")

                        # Cobrando dinheiro e adicionando os pontos
                        await update_user(ctx.guild.id, ctx.author.id, 'coins', -preco, 'inc')
                        galo[skill] += skillPoint
                        await update_user(ctx.guild.id, ctx.author.id, 'galo', galo, 'set')
                        return

        except asyncio.TimeoutError:
            return await msg.delete()

def setup(client):
  client.add_cog(UpgradeGalo(client))

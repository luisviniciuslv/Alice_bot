import asyncio
import random

import discord
from database.mongodb import checkMoney, user_get
from discord.ext import commands

atack = ['atacou por trás do', 'atacou por frente do', 'atacou por cima do', 'acertou a cabeça do', 'acertou as costas do']
critical = ['quebrou uma perna do', 'rasgou o peito do', 'depenou o pescoço do']
dodge = ['desviou pela direita do', 'deu um pulo e saiu ileso do', 'desviou com classe do']
block = ['bloqueou o ataque do', 'segurou o ataque do', 'aguentou com as asas o ataque do']

class Rinha(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["battle"])
    async def rinha(self, ctx, aposta: int = None, member: discord.Member= None):

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

                galo1 = await user_get(ctx.guild.id, ctx.author.id, 'galo')
                galo2 = await user_get(ctx.guild.id, member.id, 'galo')

                embed = discord.Embed(title="Rinha de galo", value=f"{galo1['nome']} vs {galo2['nome']}", color=0x4FABF7)
                embed.add_field(name="**Começando**", value=f"** **", inline=False)

                log = discord.Embed(title="Log da rinha", value=f"{galo1['nome']} vs {galo2['nome']}", color=0x4FABF7)
                msg = await ctx.channel.send(embed=embed)
                turns = 0

                while True:
                    if turns % 2 == 0:
                        atacker = galo1
                        atackerUser = ctx.author
                        defender = galo2
                        defenderUser = member
                    else:
                        atacker = galo2
                        atackerUser = member
                        defender= galo1
                        defenderUser = ctx.author

                    if random.randint(1, 100) <= defender['dodge']:
                        log.add_field(name=f"turno {turns}", value=f"``{defender['nome']} {random.choice(dodge)} {atacker['nome']}``", inline=False)
                        turns += 1

                    elif random.randint(1, 100) <= atacker['crit']:
                        if random.randint(1,100) <= defender['block']:
                            log.add_field(name=f"turno {turns}", value=f"``{defender['nome']}segurou um ataque critico do {atacker['nome']}, recebendo {atacker['dano']} de dano``", inline=False)
                            defender['vida'] -= atacker['dano']
                            log.add_field(name=f"``{galo1['nome']}: {galo1['vida']} de vida``", value=f"** **", inline=False)
                            log.add_field(name=f"``{galo2['nome']}: {galo2['vida']} de vida``", value=f"** **", inline=False)
                            turns += 1
                        else:
                            log.add_field(name=f"turno {turns}", value=f"``{atacker['nome']} {random.choice(critical)} {defender['nome']}, recebendo {atacker['dano'] * 2} de dano``", inline=False)
                            defender['vida'] -= atacker['dano'] * 2 
                            turns += 1

                    elif random.randint(1, 100) <= defender['block']:
                        log.add_field(name=f"turno {turns}", value=f"``{defender['nome']} {random.choice(block)} {atacker['nome']}, recebendo {round(atacker['dano'] / 2)} de dano``", inline=False)
                        defender['vida'] -= round(atacker['dano'] / 2)
                        log.add_field(name=f"``{galo1['nome']}: {galo1['vida']} de vida``", value=f"** **", inline=False)
                        log.add_field(name=f"``{galo2['nome']}: {galo2['vida']} de vida``", value=f"** **", inline=False)
                        turns += 1  
                    else:
                        log.add_field(name=f"turno {turns}", value=f"``{atacker['nome']} {random.choice(atack)} {defender['nome']}, recebendo {atacker['dano']} de dano``", inline=False)
                        log.add_field(name=f"``{galo1['nome']}: {galo1['vida']} de vida``", value=f"** **", inline=False)
                        log.add_field(name=f"``{galo2['nome']}: {galo2['vida']} de vida``", value=f"** **", inline=False)
                        defender['vida'] -= atacker['dano']
                        turns += 1  
                    if defender['vida'] <= 0:
                        embed = discord.Embed(title="Rinha de galo", value=f"** **", color=0x4FABF7)
                        embed.add_field(name="**Fim**", value=f"``{atackerUser.name} venceu a rinha de galo com {defenderUser.name}``", inline=False)
                        await ctx.send(embed=log)
                        await ctx.send(embed=embed) 
                        return

            except asyncio.TimeoutError:
                return await msg.delete()
    
def setup(client):
  client.add_cog(Rinha(client))

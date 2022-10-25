import discord
from discord.ext import commands


class CountMessages(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @commands.command()
  async def history(self, ctx, member: discord.Member = None):
    if(member == None): member = ctx.author
    comandos_musica = [".p", "m!p"]
    comandos_musica_counter = 0
    xingamentos = ["porra", "caralho", "cu", "crl", "vsf", "fuder", "fude", "bct", "buceta", "viado", "vsfd", "pqp", "puta", "fdp", "cuzao", "cz", "cuzão"]
    xingamentos_counter = 0
    racista = False
    counter = 0
    contar = await ctx.send(f'Contando mensagens de {member.mention}, (isso pode demorar um pouquinho)')
    for channel in self.client.get_all_channels():
      if str(channel.type) == 'text':
        async for message in channel.history(limit=None):
          if message.author == member:
            counter += 1 
            
            # Contar xingamentos
            for i in xingamentos:
              if i in message.content.lower():
                for j in message.content.lower().split(" "):
                  for k in xingamentos:
                    if j == k:
                      xingamentos_counter += 1
                    
            if "preto" in message.content.lower() or "macaco" in message.content.lower() or "pretos" in message.content.lower():
              racista = True
            
            # Contar músicas
            for i in comandos_musica:
              if i in message.content.lower():
                comandos_musica_counter += 1
                
    if(racista == True): racista = "Sim"
    else: racista = "Não"
    
    embed=discord.Embed(title="Total de mensagens", description=counter, color=0x00ff4c)
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.add_field(name="Xingamentos", value=xingamentos_counter, inline=False)
    embed.add_field(name="Pedidos de musica", value=comandos_musica_counter, inline=False)
    embed.add_field(name="É racista?", value=racista, inline=False)
      
    await contar.edit(content="", embed=embed)
    try:
      await ctx.author.send(embed=embed)
    except:
      pass

def setup(client):
    client.add_cog(CountMessages(client))

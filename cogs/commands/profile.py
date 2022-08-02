from io import BytesIO

import discord
import requests
from database.mongodb import user_get
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont


class Profile(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='profile', aliases=['card'])
    async def profile(self, ctx):

        # Verificação de cargo
        lounge = "nenhuma"
        for i in ctx.author.roles:
            if i.id == 1000805488797171782: #yakuza
                lounge = "yakuza"
            if i.id == 1001521467021873273: #Júbilo
                lounge = "Jubilo"
            if i.id == 1000926331493687326: #Erasyum
                lounge = "Erasyum"
        
        # Verificação de formato de imagem
        if 'gif' in str(ctx.author.avatar_url):
            avatar = str(ctx.author.avatar_url).replace('gif', 'png')
        if 'webp' in str(ctx.author.avatar_url):
            avatar = str(ctx.author.avatar_url).replace('webp', 'png')

        # Definições de perfil
        money = await user_get(ctx.guild.id, ctx.author.id, 'banco')
        lvl = await user_get(ctx.guild.id, ctx.author.id, 'lvl')

        # Definindo Avatar
        avatar = Image.open(BytesIO(requests.get(ctx.author.avatar_url).content))
        avatar = avatar.resize((256, 256))

        # Deixando Avatar Redondo
        bigsize = (avatar.size[0] * 3,  avatar.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mask)

        # Definindo fundo
        fundo = Image.open(BytesIO(requests.get('https://cdn.discordapp.com/attachments/1000862872194265088/1002663635795054683/dragao.png').content))
        
        # Definindo fonte
        fonte = ImageFont.truetype('fonts/Molot.otf', 70)

        # Definindo textos
        escrever = ImageDraw.Draw(fundo)
        escrever.text(xy=(15,600), text=f"{lounge}", fill=(0,0,0), font=fonte)
        escrever.text(xy=(65,683), text=f"{money}", fill=(0,0,0), font=fonte)
        escrever.text(xy=(980,683), text=f"lvl: {lvl}", fill=(0,0,0), font=fonte)

        # Colando avatar no fundo
        fundo.paste(avatar, (25, 25), avatar)

        # Salvando e enviando imagem
        fundo.save('img.png', format='PNG')
        img = discord.File(open('img.png', 'rb'))
        await ctx.send(file=img)

def setup(client):
  client.add_cog(Profile(client))

from io import BytesIO
from discord.ext import commands
import discord
from PIL import Image, ImageDraw, ImageFont
import requests
from database.mongodb import get_user

class Apostas(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['aposta', 'despesas'])
    async def apostas(self, ctx, member: discord.Member = None):
        # Verificando se o usuário passou um membro
        if member is None:
            user = ctx.author
        else:
            user = member

        # Verificando membros que boostaram server
        if user.id == 450011504842899459:
            background = "https://cdn.discordapp.com/attachments/1004090752567091362/1004102923195797525/FUNDOBOLINHA.png"
            color = (255, 203, 219)

        else:
            background = "https://cdn.discordapp.com/attachments/996464678647640264/1002659429726044190/dragao.png"
            color = (0, 0, 0)

        # Verificação de formato de imagem
        if 'gif' in str(user.avatar_url):
            avatar = str(user.avatar_url).replace('gif', 'png')
        else:
            avatar = str(user.avatar_url)

        # Definições de perfil
        user = await get_user(ctx.guild.id, user.id)
        total = user['valor_apostado']
        perdido = user['valor_perdido']
        ganho = user['valor_ganho']

        # Definindo Avatar
        avatar = Image.open(BytesIO(requests.get(avatar).content))
        avatar = avatar.resize((256, 256))

        # Deixando Avatar Redondo
        bigsize = (avatar.size[0] * 3,  avatar.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mask)

        # Definindo fundo
        fundo = Image.open(BytesIO(requests.get(background).content))
        
        # Definindo fonte
        fonte = ImageFont.truetype('fonts/Noto.ttf', 70)

        # Definindo textos
        escrever = ImageDraw.Draw(fundo)
        escrever.text(xy=(20, 450), text=f"total: {total}", fill=color, font=fonte)
        escrever.text(xy=(20, 550), text=f"perdido: {perdido}", fill=color, font=fonte)
        escrever.text(xy=(20, 650), text=f"ganho: {ganho}", fill=color, font=fonte)

        # Colando avatar no fundo
        fundo.paste(avatar, (25, 25), avatar)

        # Salvando e enviando imagem
        fundo.save('img.png', format='PNG')
        img = discord.File(open('img.png', 'rb'))
        await ctx.send(file=img)

def setup(client):
  client.add_cog(Apostas(client))
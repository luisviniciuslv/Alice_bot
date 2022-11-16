
import time
from bs4 import BeautifulSoup
import discord
from discord import app_commands
from discord.ext import commands
from selenium import webdriver

class Pinterest(commands.Cog):
  def __init__(self, client):
    self.client = client
    
  @app_commands.command(name='images', description='Devolve algumas imagens do twitter!')
  async def twitter(self, interaction: discord.Interaction, tag:str):
    await interaction.response.send_message("buscando imagens...")
    url = f"https://twitter.com/search?q={tag}&src=typed_query&f=image"
    ScrollNumber = 2  # The depth we wish to load
    sleepTimer = 5    # Waiting 1 second for page to load

    #  Bluetooth bug circumnavigate
    options = webdriver.ChromeOptions() 
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=options) 
    driver.get(url)
    time.sleep(4)
    # for _ in range(1,ScrollNumber):
    #   driver.execute_script("window.scrollTo(1,100000)")
    #   print("scrolling")
    #   time.sleep(sleepTimer)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    
    div_nav = soup.select('img')
    images = []
    for i in div_nav:
      try:
        if "profile_images" in i['src']:
          pass
        elif "media" in i.get('src'):
          if len(images) < 1:
            images.append(i.get('src'))
          else:
            break
      except:
        pass
      
    embed = discord.Embed(title=f"Imagens de {tag}", color=0x00ff00)
    if len(images) > 0:
      for i in images:
        embed.set_image(url=i)
        await interaction.channel.send(embed=embed)
    else:
      await interaction.channel.send("Nenhuma imagem encontrada!")

async def setup(client):
  await client.add_cog(Pinterest(client))
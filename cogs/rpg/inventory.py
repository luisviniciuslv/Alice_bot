
import json
from classes.Rpg import Rpg, SelectViewEquip, SelectViewTypeInventory
from discord.ext import commands


class Inventory(commands.Cog):
  def __init__(self, client):
    self.client = client
  # time to loot 
  @commands.hybrid_command(
    name="inventario",
    description="Saia para lootear e encontre itens.",
    aliases=["inv", "i"]
  ) 
  async def inventory(self, ctx: commands.Context):
    view = SelectViewTypeInventory(ctx)
  
    await ctx.send(view=view)
  
  @commands.hybrid_command(
    name="equip_armor",
    description="Equipar armadura.",
    aliases=["armor"]
  )
  async def equip_armor(self, ctx: commands.Context):
    game = Rpg(ctx.author.id)
    armors = json.load(open('items/armors.json', 'r'))   
    armors_inventory_id = game.get_armors()
    armors_inventory = []
    for i in armors:
      if str(i["id"]) in armors_inventory_id:
        armors_inventory.append(i)

    if not armors:
      return await ctx.send("Você não tem armaduras para equipar.")

    view = SelectViewEquip(ctx, armors_inventory)
    await ctx.send("Selecione uma armadura para equipar.", view=view)
    
  @commands.hybrid_command(
    name="equip_weapon",
    description="Equipar uma arma.",
    aliases=["sword"]
  )
  async def equip_weapon(self, ctx: commands.Context):
    game = Rpg(ctx.author.id)
    weapons = json.load(open('items/weapons.json', 'r'))   
    weapons_inventory_id = game.get_weapons()
    weapons_inventory = []
    for i in weapons:
      if str(i["id"]) in weapons_inventory_id:
        weapons_inventory.append(i)
      
    if not weapons:
      return await ctx.send("Você não tem armaduras para equipar.")

    view = SelectViewEquip(ctx, weapons_inventory)
    await ctx.send("Selecione uma armadura para equipar.", view=view)
    
async def setup(client):
  await client.add_cog(Inventory(client))

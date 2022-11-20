from discord.ext import commands
import discord

class CommandErrorHandler(commands.Cog):
  def __init__(self, bot) -> None:
    self.bot = bot

  @commands.Cog.listener()
  async def on_command_error(self, context: commands.Context, error) -> None:
    if isinstance (error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Espere um pouco, você precisa descansar!",
            description=f"Você pode sair em {f'{round(hours)} horas' if round(hours) > 0 else ''} {f'{round(minutes)} minutos' if round(minutes) > 0 else ''} {f'{round(seconds)} segundos' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    else:
      raise error
      
async def setup(bot):
    await bot.add_cog(CommandErrorHandler(bot))

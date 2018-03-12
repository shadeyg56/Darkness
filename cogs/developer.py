import discord
from discord.ext import commands

class Developer():
    def __init__(self, bot):
        self.bot = bot
        
    @bot.command(name='reload')
    async def _reload(ctx,*, module : str):
    """Reloads a module."""
        channel = ctx.channel
        module = 'cogs.'+module
        try:
            bot.unload_extension(module)
            x = await ctx.send('Successfully Unloaded.')
            bot.load_extension(module)
            await x.edit(content='Successfully Reloaded.')
        except Exception as e:
            await x.edit(contenr='\N{PISTOL}')
            await ctx.send(f'{type(e).__name__}: {e}')
        else:
            await x.edit(content='Done. \N{OK HAND SIGN}')
 

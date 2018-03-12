import discord
from discord.ext import commands

class Developer():
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='reload')
    @commands.is_owner()
    async def _reload(self, ctx,*, module : str):
    """Reloads a module."""
        channel = ctx.channel
        module = 'cogs.'+module
        try:
            self.bot.unload_extension(module)
            x = await ctx.send('Successfully Unloaded.')
            self.bot.load_extension(module)
            await x.edit(content='Successfully Reloaded.')
        except Exception as e:
            await x.edit(contenr='\N{PISTOL}')
            await ctx.send(f'{type(e).__name__}: {e}')
        else:
            await x.edit(content='Done. \N{OK HAND SIGN}')
            
            
    @commands.command()
    @commands.is_owner()
    async def shutdown(ctx):
        await ctx.send("Shutting down...")
        await self.bot.logout()

def cleanup_code( content):
    """Automatically removes code blocks from the code."""
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    # remove `foo`
    return content.strip('` \n')        
           
def get_syntax_error(e):
    if e.text is None:
        return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)
    return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

async def to_code_block(ctx, body):
    if body.startswith('```') and body.endswith('```'):
        content = '\n'.join(body.split('\n')[1:-1])
    else:
        content = body.strip('`')
    await bot.edit_message(ctx.message, '```py\n'+content+'```')

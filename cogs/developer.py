import discord
from discord.ext import commands
import subprocess
import io
import textwrap
import traceback
from contextlib import redirect_stdout



class Developer():
    def __init__(self, bot):
        self.bot = bot
        self.startup_extensions = ['fun', 'developer', 'mod', 'info', 'setup']
        
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
            await self.bot.edit_message(ctx.message, '```py\n'+content+'```')
    
    @commands.command()
    @commands.is_owner()
    async def terminal(self, ctx, *, command:str):
        await ctx.send(subprocess.run(command,  cwd='/home/pi/Desktop/Darkness', stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8'))
        
    @commands.command()
    @commands.is_owner()
    async def update(self, ctx):
        x = subprocess.run('git pull', cwd='/home/pi/Desktop/Darkness', stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
        try:
            for module in self.startup_extensions:
                self.bot.unload_extension(module)
                self.bot.load_extension(module)
                await ctx.send(x)
                await ctx.send("All Cogs Reloaded")
        except Exception as e:
            await ctx.send(f"Error, Log: \n```py\n{e}```")
                    
          
    @commands.command(name='eval')
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        '''Run python scripts on discord!'''
        env = {
            'bot': bot,
            'ctx': ctx,
            'channel': ctx.message.channel,
            'author': ctx.message.author,
            'server': ctx.message.guild,
            'message': ctx.message,
        }
        env.update(globals)
        body = cleanup_code(content=body)
        stdout = io.StringIO()
        to_compile = 'async def func():\n%s' % textwrap.indent(body, '  ')
        try:
            exec(to_compile, env)
        except SyntaxError as e:
            return await ctx.send(get_syntax_error(e))
        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            x = await ctx.send('```py\n{}{}\n```'.format(value, traceback.format_exc()))
            try:
                await self.bot.add_reaction(x, '\U0001f534')
            except:
                pass
        else:
            value = stdout.getvalue()
        
        if TOKEN in value:
            value = value.replace(TOKEN,"[EXPUNGED]")
            
        if ret is None:
            if value:
                try:
                    x = await ctx.send('```py\n%s\n```' % value)
                except:
                    x = await ctx.send('```py\n\'Result was too long.\'```')
                try:
                    await bot.add_reaction(x, '\U0001f535')
                except:
                    pass
            else:
                try:
                    await bot.add_reaction(ctx.message, '\U0001f535')
                except:
                    pass
        else:
            try:
                x = await ctx.send('```py\n%s%s\n```' % (value, ret))
            except:
                x = await ctx.send('```py\n\'Result was too long.\'```')
            try:
                await bot.add_reaction(x, '\U0001f535')
            except:
                pass
            
def setup(bot):
    bot.add_cog(Developer(bot))

import discord
from discord.ext import commands
import datetime
import io
import textwrap
import traceback
from contextlib import redirect_stdout
import json
import asyncio
import string
import sys
import subprocess
sys.path.insert(0, '/home/pi/Desktop/')
import private
TOKEN = private.TOKEN
async def get_pre(bot, message):
	with open('cogs/utils/servers.json') as f:
		data = json.load(f)
	try:
		if str(message.guild.id) not in data:
			return 'd.'
	except:
		pass
	else:
		return data[str(message.guild.id)]['prefix']

	
	
bot = commands.Bot(command_prefix=get_pre)



startup_extensions = [
 
 
    "cogs.mod",
    "cogs.fun",
    "cogs.info",
    'cogs.setup'
    
 
 
]



@bot.event
async def on_ready():
    print('------------------------------------')
    print('THE BOT IS ONLINE')
    print('------------------------------------')
    print("Name: {}".format(bot.user.name))
    print('Author: shadeyg56')
    print("ID: {}".format(bot.user.id))
    print('DV: {}'.format(discord.__version__))
    bot.uptime = datetime.datetime.now()
    embed=discord.Embed(title='Good Morning', description='Up and at em', color=0xed)   
    embed.set_footer(text='Darkness ready for use')
    server = len(bot.guilds)
    channel = bot.get_channel(356599668739670049)
    users = sum(1 for _ in bot.get_all_members())
    await channel.send(embed=embed)
    await bot.change_presence(game=discord.Game(name='Major update | d.setup'))

def is_owner():
    return commands.check(lambda ctx: ctx.message.author.id == 300396755193954306)


@bot.event
async def on_member_join(member):
	with open('cogs/utils/servers.json') as f:
		data = json.load(f)
	guild = member.guild
	member_count = len(guild.members)
	user = member
	server = guild.name
	welc_channel = data[str(guild.id)]['welc_channel']
	welc_channel = welc_channel.replace('<', '')
	welc_channel = welc_channel.replace('#', '')
	welc_channel = welc_channel.replace('>', '')
	msg = data[str(guild.id)]['welc_msg']
	if '{user}' in msg:
		msg = msg.replace('{user}', user.name)
	if '{server}' in msg:
		msg = msg.replace('{server}', server)
	if '{member_count}' in msg:
		msg = msg.replace('{member_count}', str(member_count))
			
	
	if msg:
		channel = bot.get_channel(int(welc_channel))
		await channel.send(msg)
		
@bot.event
async def on_member_remove(member):
	with open('cogs/utils/servers.json') as f:
		data = json.load(f)
	guild = member.guild
	user = member
	server = guild.name
	member_count = len(guild.members)
	welc_channel = data[str(guild.id)]['welc_channel']
	welc_channel = welc_channel.replace('<', '')
	welc_channel = welc_channel.replace('#', '')
	welc_channel = welc_channel.replace('>', '')
	msg = data[str(guild.id)]['leave_msg']
	if '{user}' in msg:
		msg = msg.replace('{user}', user.name)
	if '{server}' in msg:
		msg = msg.replace('{server}', server)
	if '{member_count}' in msg:
		msg = msg.replace('{member_count}', str(member_count))
	if msg:
		channel = bot.get_channel(int(welc_channel))
		await channel.send(msg)

@bot.event
async def on_guild_join(guild):
    channel = bot.get_channel(418216163588308993)
    embed = discord.Embed(title='New Server!', description=f'Server Name: {guild.name} | Server Num {len(bot.guilds)}', color=discord.Color.green())
    embed.set_thumbnail(url=guild.icon_url)
    embed.set_footer(text=f"Server ID: {guild.id}")
    embed.set_author(name=f"Owner: {guild.owner} | ID: {guild.owner.id}", icon_url=guild.owner.avatar_url)
    await channel.send(embed=embed)

@bot.event
async def on_guild_remove(guild):
    channel = bot.get_channel(418216163588308993)
    embed = discord.Embed(title='Removed Server :crying_cat_face:', description=f'Server Name: {guild.name} | Server Num {len(bot.guilds)}', color=discord.Color.red())
    embed.set_thumbnail(url=guild.icon_url)
    embed.set_footer(text=f"Server ID: {guild.id}")
    embed.set_author(name=f"Owner: {guild.owner} | ID: {guild.owner.id}", icon_url=guild.owner.avatar_url)
    await channel.send(embed=embed)

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
 

def fmt_help(page):
    cmd = ''
    for line in page.splitlines():
        if line.startswith('.'):
            cmd = line.strip('.')
            break
    em = discord.Embed(color=0x00FFFF)
    em.set_author(name='Help - {}'.format(cmd))

async def send_cmd_help(ctx):
    await ctx.send(f'`Usage: {ctx.prefix + ctx.command.signature}')
	
#@bot.event
#async def on_command_error(error, ctx):
  # print(error)
  # if isinstance(error, commands.MissingRequiredArgument):
	#await send_cmd_help(ctx)
	#print('Sent command help')
#elif isinstance(error, send_help):
	#await send_cmd_help(ctx)
	#print('Sent command help')
#   elif isinstance(error, commands.DisabledCommand):
#       await ctx.send("That command is disabled.")
#       print('Command disabled.')
#   elif isinstance(error, commands.CommandInvokeError):
#       # A bit hacky, couldn't find a better way
#       no_dms = "Cannot send messages to this user"
#       is_help_cmd = ctx.command.qualified_name == "help"
#       is_forbidden = isinstance(error.original, discord.Forbidden)
#       if is_help_cmd and is_forbidden and error.original.text == no_dms:
#           msg = ("I couldn't send the help message to you in DM. Either"
#                  " you blocked me or you disabled DMs in this server.")
#           await ctx.send(msg)
#           return

@bot.command()
async def say(ctx, *, msg: str):
	"Make the bot say something"
	await ctx.send(msg)
	await discord.Message.delete(ctx.message)
	
@bot.command()
async def invite(ctx):
	await ctx.send('**Darkness Invite:** https://discordapp.com/oauth2/authorize?client_id=355189919410421760&scope=bot')
		       
@bot.command()
async def support(ctx):
	await ctx.send('**Darkness Support:** https://discord.gg/Jjdp8hf')

@bot.command()
@is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting down...")
    await bot.logout()

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
           
@bot.command()
@is_owner()
async def terminal(ctx, *, command:str):
	await ctx.send(subprocess.run(command,  cwd='/home/pi/Desktop/Darkness', stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8'))
@bot.command()
@is_owner()
async def update(ctx):
    x = subprocess.run('git pull', cwd='/home/pi/Desktop/Darkness', stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
    try:
        for module in startup_extensions:
            bot.unload_extension(module)
            bot.load_extension(module)
        await ctx.send(x)
        await ctx.send("All Cogs Reloaded")
    except Exception as e:
        await ctx.send(f"Error, Log: \n```py\n{e}```")
    
      
@bot.command(name='eval')
@is_owner()
async def _eval(ctx, *, body: str):
    '''Run python scripts on discord!'''
    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.message.channel,
        'author': ctx.message.author,
        'server': ctx.message.guild,
        'message': ctx.message,
    }

    env.update(globals())

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
            await bot.add_reaction(x, '\U0001f534')
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


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
            print('Loaded: {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Error on load: {}\n{}'.format(extension, exc))

           
        
    
bot.run(TOKEN)
   
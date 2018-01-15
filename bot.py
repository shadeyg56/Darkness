import discord
from discord.ext import commands
import datetime
import io
import textwrap
import traceback
from contextlib import redirect_stdout
import json
import asyncio

TOKEN = 'Mzk4ODkzODg3MTcyNjQwNzY4.DTFc7g.yKypeXZzCZ5p8iNFqDUg1B-5SGM'

bot = commands.Bot(command_prefix="~")
bot.remove_command("help")


startup_extensions = [
 
 
    "cogs.mod",
    "cogs.fun",
    "cogs.info"
    
 
 
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
    await bot.change_presence(game=discord.Game(name='Being coded.'))

def is_owner():
    return commands.check(lambda ctx: ctx.message.author.id == 300396755193954306)

@bot.command()
async def setup(ctx):
	server = ctx.guild
	with open('cogs/utils/servers.json') as f:
		data = json.loads(f.read())
		data[server.id] ={}
	x = await ctx.send('Welcome to the Darkness interactive setup')
	await asyncio.sleep(3)
	await ctx.send('Please enter a prefix (Enter None for default)')
	prefix = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
	if prefix.content == 'None':
		prefix.content  = '~'
	await ctx.send(f'Prefix set to {prefix.content}')
		
	await ctx.send('Enable welcome message?')
	msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
	if msg.content == 'Yes':
		await ctx.send('What should the message say?')
		msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
		await ctx.send('What channel should be the welcome channel?')
		welc_channel = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
		if welc_channel.content.startswith('<#'):
			await ctx.send(f'Welcome channel set to {welc_channel.content} with message {msg.content}')
		else:
			await ctx.send('Invalid channel. Please make sure you mention the channel')
			await ctx.send('What channel should be the welcome channel?')
			welc_channel = await bot.wait_for('message', check=lambda m: m.author == ctx.author)		
			await ctx.send(f'Welcome channel set to {welc_channel.content} with message {msg.content}')	
	else:
		pass
		
	await ctx.send('Enable leave message?')
	leave_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
	if leave_msg.content == 'Yes':
		await ctx.send('What should the message say?')
		leave_msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
		await ctx.send(f'Leave message set to {leave_msg.content}')	
	else:
		pass
		
	data[server.id]['name'] = server.name 
	data[server.id]['prefix'] = prefix.content.strip()
	data[server.id]['welc_channel'] = welc_channel.content.strip()
	data[server.id]['welc_msg'] = msg.content.strip()
	data[server.id]['leave_msg'] = leave_msg.content.strip()
	
	data = json.dumps(data, indent=4, sort_keys=True)
	
	with open('cogs/utils/servers.json', 'w') as f:
		f.write(data)
	await ctx.send('Setup complete')



	
		
	

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Darkness Commands", color=0xed)
    embed.add_field(name='Miscellaneous:', value='help, say')
    embed.add_field(name="Moderation", value="purge, kick, ban, unban, addrole, removerole")
    embed.add_field(name="Info", value="info, serverinfo, userinfo, weather, urban")
    embed.add_field(name='Fun', value='cat, ball')
    embed.set_footer(text='Bot Dev: -= shadeyg56 =-#1702')
    await ctx.send(embed=embed)

def fmt_help(page):
    cmd = ''
    for line in page.splitlines():
        if line.startswith('.'):
            cmd = line.strip('.')
            break
    em = discord.Embed(color=0x00FFFF)
    em.set_author(name='Help - {}'.format(cmd))

async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        pages = bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        for page in pages:
            # page = page.strip('```css').strip('```')


            await ctx.send(page)
        print('Sent command help')
    else:
        pages = bot.formatter.format_help_for(ctx, ctx.command)
        for page in pages:
            await ctx.send(page)
        print('Sent command help')

@bot.command()
async def say(ctx, *, msg: str):
	"Make the bot say something"
	await ctx.send(msg)
	await discord.Message.delete(ctx.message)

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

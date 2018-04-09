
import discord
from discord.ext import commands
import datetime
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

	
	
bot = commands.Bot(command_prefix=commands.when_mentioned_or(get_pre))



startup_extensions = [
 
 
    "cogs.mod",
    "cogs.fun",
    "cogs.info",
    'cogs.setup',
    "cogs.developer",
    "cogs.util",
    "cogs.economy"
    
 
 
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
    await bot.change_presence(activity=discord.Game(name='Major update | d.setup'))

@bot.command()
async def prefix(ctx):
	"""Get the prefix for the server you're in"""
	with open('cogs/utils/servers.json') as f:
		data = json.load(f)
	try:
		if str(message.guild.id) not in data:
			await ctx.send(f"{ctx.guild}'s prefix: d.")
	except:
		pass
	else:
		await ctx.send(f"{ctx.guild}'s prefix: {data[str(message.guild.id)]['prefix']}") 



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
	
@bot.event
async def on_command_error(ctx, error):
	print(error)
	if isinstance(error, commands.MissingRequiredArgument):
		await send_cmd_help(ctx)
		print('Sent command help')
	#elif isinstance(error, send_help):
		#print('Sent command help')
	elif isinstance(error, commands.DisabledCommand):
		await ctx.send("That command is disabled.")
		print('Command disabled.')
	elif isinstance(error, commands.NotOwner):
		await ctx.send("You're not a developer silly")
		print("Attemepted dev command by non-dev")
	#elif isinstance(error, commands.CommandInvokeError):
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
	await ctx.message.delete()
	await ctx.send(msg)
	
@bot.command()
async def invite(ctx):
	await ctx.send('**Darkness Invite:** https://discordapp.com/oauth2/authorize?client_id=355189919410421760&scope=bot')
		       
@bot.command()
async def support(ctx):
	await ctx.send('**Darkness Support:** https://discord.gg/Jjdp8hf')

           




if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
            print('Loaded: {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Error on load: {}\n{}'.format(extension, exc))

           
        
    
bot.run(TOKEN)
   

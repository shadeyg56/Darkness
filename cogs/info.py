import discord
from discord.ext import commands
import time
import psutil
import platform
import openweathermapy.core as weather
import urbandict
import json

class Info():
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def serverinfo(self, ctx):
		server = ctx.guild
		total_member = len(server.members)
		online = len([x.status for x in server.members
                     if x.status == discord.Status.online or x.status == discord.Status.idle or x.status == discord.Status.dnd])
		date = server.created_at
		text_channels = len([m for m in server.channels
                             if isinstance(m, discord.TextChannel)])
		voice_channels = len(server.channels) - text_channels
		passed = (ctx.message.created_at - server.created_at).days
		embed = discord.Embed(title="Server Info", color=0xed)
		created_at = "Since {}. That's over {} days ago!".format(server.created_at.strftime("%d %b %Y %H:%M"), passed)
		embed.set_author(name=server.name, icon_url=server.icon_url)
		embed.set_thumbnail(url=server.icon_url)
		embed.add_field(name="Owner", value=server.owner)
		embed.add_field(name="ID", value=server.id)
		embed.add_field(name="Members", value=f"{total_member} total\n{online} online")
		embed.add_field(name="Roles", value=len(server.roles))
		embed.add_field(name="Text Channels", value=text_channels)
		embed.add_field(name='Voice Chanels', value=voice_channels)
		embed.add_field(name="Region", value=server.region)
		embed.set_footer(text=created_at)
		await ctx.send(embed=embed)

	@commands.command()
	async def userinfo(self, ctx, user: discord.Member = None):
		if user == None:
			user = ctx.author
		roles = sorted([a.name for a in user.roles if a.name !="@everyone"])
		avatar = user.avatar_url
		server = ctx.guild
		created = user.created_at
		member_number = sorted(server.members,key=lambda m: m.joined_at).index(user) + 1
		embed = discord.Embed(title="User Info",description=f"{user} is on Discord in {user.status} mode", color=0xed)
		embed.set_author(name=user, icon_url= avatar)
		embed.set_thumbnail(url=avatar)
		embed.add_field(name="Account Created", value=created.__format__('%A, %d. %B %Y'))
		embed.add_field(name="Joined At", value=user.joined_at.__format__('%A, %d. %B %Y'))
		embed.add_field(name="Join Number", value=member_number)
		embed.add_field(name="Nickname", value=user.nick)
		embed.add_field(name="Roles", value=roles)
		embed.set_footer(text=f"ID: {user.id}")
		await ctx.send(embed=embed)

	@commands.command()
	async def info(self, ctx):
		RAM = psutil.virtual_memory()
		used = RAM.used >> 20
		percent = RAM.percent
		CPU  = psutil.cpu_percent()
		embed = discord.Embed(title="Darkness Info", color=0xed, timestamp=ctx.message.created_at)
		embed.set_thumbnail(url=self.bot.user.avatar_url)
		embed.add_field(name="Author", value="-= shadeyg56 =-#1702")
		embed.add_field(name="Servers", value=len(self.bot.guilds))
		embed.add_field(name='OS', value=platform.system())
		embed.add_field(name="Memory", value=f'{percent}% ({used}MB)')
		embed.add_field(name="CPU", value=f"{CPU}%")
		embed.add_field(name='Support', value='[Join the support server!](https://discord.gg/Jjdp8hf)')
		embed.add_field(name='GitHub', value='[GitHub Repo](https://github.com/shadeyg56/Darkness/tree/rewrite)')
		embed.set_footer(text='Powered by discord.py v.1.0.0a')
		await ctx.send(embed=embed)
		
	@commands.command()
	async def weather(self, ctx, *, city: str):
         settings = {"APPID": '5793b69ec91fb3232c200c1df4c2141b'}
         data = weather.get_current('{}'.format(city), units='metric', **settings)
         data2 = weather.get_current(city, units='standard', **settings)
         keys = ['main.temp', 'main.humidity', 'coord.lon', 'coord.lat']
         x = data.get_many(keys)
         loc = data('name')
         country = data('sys.country')
         lon = data('coord.lon')
         lat = data('coord.lat')
         temp = data('main.temp')
         temp2 = temp * 9/5 + 32
         high = data('main.temp_max')
         low = data('main.temp_min')
         high2 = high * 9/5 + 32
         low2 = low * 9/5 + 32
         embed = discord.Embed(title='{}, {}'.format(loc, country), color=0x00FF00)
         embed.add_field(name='Absolute Location', value='Longitude, Latitude\n{}, {}'.format(lon, lat))
         embed.add_field(name='Temperature', value='{}F, {}C'.format(temp2, temp))
         embed.add_field(name='Humidity', value='{}%'.format(data('main.humidity')))
         embed.add_field(name='Wind Speed', value='{}m/s'.format(data('wind.speed')))       
         embed.add_field(name='Low and High Temp', value='{}F - {}F\n{}C - {}C'.format(low2, high2, low, high))
         embed.set_footer(text='Weather Data from OpenWeatherMap.org')
         embed.set_thumbnail(url='https://cdn4.iconfinder.com/data/icons/cloud-46/32/cloud_weather_clean_clear_heaven_paradise-512.png')
         await ctx.send(embed=embed)
         
	@commands.command()
	async def urban(self, ctx, *, word:str):
				defi = urbandict.define(word)
				definition = defi[0]['def'] #definition of the word
				example = defi[0]['example'] #example of usage (if available)
				embed = discord.Embed(title=word,description=definition, color=0x0062f4)
				embed.add_field(name="Example",value=example,inline=False)
				embed.set_footer(text="Urban Dictionary")
				await ctx.send(embed=embed)
	@commands.command()
	async def create_tag(self, ctx, tagname:str, *, text:str):
		with open('cogs/utils/tags.json') as f:
			data = json.load(f)
		try:
			data[tagname] = text
			await ctx.send(f'Tag {tagname} succesfully created')
		except:
			await ctx.send('Error making tag')
		data = json.dumps(data, indent=4, sort_keys=True)
		with open('cogs/utils/tags.json', 'w') as f:
			f.write(data)

	@commands.command()
	async def tag(self, ctx, *, tag:str):
		with open('cogs/utils/tags.json') as f:
			data = json.load(f)
		text = data[tag]
		try:
			await ctx.send(text)
		except:
			await ctx.send('That tag does not exist. You can create it with create_tag <tagname> <text>')


def setup(bot):
	bot.add_cog(Info(bot))


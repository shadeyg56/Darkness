import discord
from discord.ext import commands
import time
import psutil
import platform
import openweathermapy.core as weather
import urbandict
import json
from mtranslate import translate
from pygoogling.googling import GoogleSearch
import hastebin
import inspect

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
		role_List = []
		for role in user.roles:
					role_List = role_List.append(role.name)
					
		role_List = str(role_List)
					role_List = role_List.replace('[', "")
					role_List = role_List.replace('"', "")
					role_List = role_List.replace("]", "")

					
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
		embed.add_field(name="Roles", value=role_List)
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
	async def tag(self, ctx, tag:str, tagname=None, *, txt=None):
		with open('cogs/utils/tags.json') as f:
			data = json.load(f)
		if tag != 'list':
			if tag != 'create':
				if tag != 'delete':
					text = data[str(ctx.guild.id)][tag]
					await ctx.send(text)
		if tag == 'list':
			keys = data[str(ctx.guild.id)]
			text = str(keys.keys())
			text = text.replace('dict_keys([', '')
			text = text.replace("'", '')
			text = text.replace('])', '')
			await ctx.send(text)
		if tag == 'create':
			if str(ctx.guild.id) not in data:
				data[str(ctx.guild.id)] = {}
			data[str(ctx.guild.id)][tagname] = txt
			await ctx.send(f'Tag {tagname} successfully created')
		if tag == 'delete':
			del data[str(ctx.guild.id)][tagname]
			await ctx.send(f'Tag {tagname} was successfully deleted')
		data = json.dumps(data, indent=4, sort_keys=True)
		with open('cogs/utils/tags.json', 'w') as f:
			f.write(data)
				
	@commands.command()
	async def translate(self, ctx,lang:str, *, message:str):
		LANGUAGES = { 'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian', 'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa', 'zh-CN': 'chinese (simplified)', 'zh-TW': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english', 'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish', 'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian', 'is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay', 'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 'sm': 'samoan', 'gd': 'scots gaelic', 'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa', 'yi': 'yiddish', 'yo': 'yoruba', 'zu': 'zulu' } 
		LANGUAGES = {y:x for x,y in LANGUAGES.items()}
		if lang in  LANGUAGES:
			await ctx.send('```{}```'.format(translate(message, lang)))
		else:
			await ctx.send('```That is not an available language.```')
			
	@commands.command()
	async def google(self, ctx, *, search_query:str):
		google_search = GoogleSearch(search_query)
		google_search.start_search()
		result = google_search.search_result
		await ctx.send(f'{result[0]}\n**See Also:**\n{result[1]}\n{result[2]}')
		
	@commands.command()
	async def hastebin(self, ctx, *, code:str):
		await ctx.message.delete()
		await ctx.send(f'{hastebin.post(code)} made by {ctx.author}')
		
	@commands.command()
	async def source(self, ctx, *, command:str):
		source = str(inspect.getsource(self.bot.get_command(command).callback))
		fmt = '```py\n'+source.replace('`', '\u200b') + '\n```'
		await ctx.send(fmt)
		
	@commands.command()
	@commands.cooldown(1, 600, commands.BucketType.user)
	async def devcontact(self, ctx, *, message:str):
		dev = self.bot.get_user(300396755193954306)
		await dev.send(f'{message} sent by {ctx.author.name} | {ctx.author.id} from {ctx.guild.name} | {ctx.guild.id}')
		await ctx.send('Your message was sent to the dev')
		

def setup(bot):
	bot.add_cog(Info(bot))


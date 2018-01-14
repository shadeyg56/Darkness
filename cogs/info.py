import discord
from discord.ext import commands
import time
import psutil

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
		RAM = list(psutil.virtual_memory())
		x = 9
		while x > 0:
			RAM = list(psutil.virtual_memory())
			num = 1
			RAM.pop(num)
			num = num + 1
			x = x - 1
		CPU  = psutil.cpu_percent()
		embed = discord.Embed(title="Bot Info", color=0xed)
		embed.add_field(name="Author", value="-= shadeyg56 =-#1702")
		embed.add_field(name="Servers", value=len(self.bot.guilds))
		embed.add_field(name="Memory", value=RAM)
		embed.add_field(name="CPU", value=f"{CPU}%")
		await ctx.send(embed=embed)


def setup(bot):
	bot.add_cog(Info(bot))

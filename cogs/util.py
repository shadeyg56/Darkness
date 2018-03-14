import discord
from discord.ext import commands

class Utils():

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.has_permissions(manage_roles=True)
	async def addrank(self, ctx, *, rank: str):
		"Add a rank that members can give themselves"
		with open("cogs/utils/servers.json") as f:
			data = json.load(f)
		role = discord.utils.find(lambda m: rank.lower() in m.name.lower(), ctx.guild.roles)
		if str(ctx.guild.id) not in data:
			data[str(ctx.guild.id)] = {}
		if "ranks" not in data:
			data[str(ctx.guild.id)]["ranks"] = {}
		if role:
			data[str(ctx.guild.id)]["ranks"][str(role.name)] = str(role.name)
			await ctx.send(f"Added {role.name} as a rank")
		elif rank in data[str(ctx.guild.id)]:
			await ctx.send("That rank already exists")
		else:
			await ctx.guild.create_role(name=rank)
			data[str(ctx.guild.id)]["ranks"][rank] = rank
			await ctx.send(f"I created and added {rank} as a rank")
		data = json.dumps(data, indent=4, sort_keys=True)
		with open("cogs/utils/servers.json", "w") as f:
			f.write(data)

	@commands.command()
	@commands.has_permissions(manage_roles=True)
	async def removerank(self, ctx, *, rank: str):
		"Remove a rank that members can give themselves"
		with open("cogs/utils/servers.json") as f:
			data = json.load(f)
		role = discord.utils.find(lambda m: rank.lower() in m.name.lower(), ctx.guild.roles)
		if rank in data[str(ctx.guild.id)]["ranks"]:
			del data[str(ctx.guild.id)]["rank"][rank]
			await ctx.send(f"I removed {rank} from the server ranks")
		else:
			await ctx.send("That rank does not exist")
		data = json.dumps(data, indent=4, sort_keys=True)
		with open("cogs/utils/servers.json", "w") as f:
			f.write(data)

	@commands.command()
	async def ranks(self, ctx):
		"View all ranks in your server"
		with open("cogs/utils/servers.json") as f:
			data = json.load(f)
		if str(ctx.guild.id) in data:
			if "ranks" in data[str(ctx.guild.id)]:
				if rank in data[str(ctx.guild.id)]["ranks"]:
					for rank in data[str(ctx.guild.id)]["ranks"]:
						await ctx.send(rank)
				else:
					await ctx.send("That rank does not exist")
			else:
				await ctx.send("This server has no ranks")
		else:
			await ctx.send("This server has no ranks")

	@commands.command(aliases="rank")
	async def iam(self, ctx, *, rank):
		"Add a server rank to yourself"
		with open("cogs/utils/servers.json") as f:
			data = json.load(f)
		try:
			if rank in data[str(ctx.guild.id)]["ranks"]:
				role = discord.utils.find(lambda m: rank.lower() in m.name.lower(), ctx.guild.roles)
				await ctx.author.add_roles(roles=role)
				await ctx.send(f"I gave you the {rank} rank")
			else:
				await ctx.send("That rank does not exist")
		except:
			await ctx.send("There is no server ranks")

def setup(bot):
	bot.add_Cog(Utils(bot))
import discord
from discord.ext import commands

class Economy():
	def __init__(self, bot):
		self.bot = bot
		with open('cogs/utils/economy.json') as f:
			self.data = json.load(f)

	@commands.command()
	async def openaccount(self, ctx):
		if str(ctx.author.id) not in self.data:
			await ctx.send("Thanks for joining the National Darkness Bank. As a welcome gift we have given you 200 Darkness chips <:Darkness:411673568170999808>")
			self.data[ctx.author.id] = {}
			self.data[ctx.author.id]["name"] = ctx.author
			self.data[str(ctx.author.id)]["servers"] = {}
			self.data[str(ctx.author.id)]["servers"][ctx.guild] = ctx.guild.id
			self.data[str(ctx.author.id)]["balance"] = 200
		else:
			await ctx.send("You've already opened an account silly")
		data = json.dumps(self.data, indent=4)
		with open('cogs/utils/economy.json', 'w') as f:
			f.write(data)

	@commands.command()
	async def balance():
		if str(ctx.author.id) in self.data:
			embed = discord.Embed(title="Balance", description=f"{self.data[str(ctx.author.id)]['balance']} Darkness Chips <:Darkness:411673568170999808>", color=discord.Color.blue())
			await ctx.send(embed=embed)
		else:
			await ctx.send("You haven't opened an account yet. To do so run the openaccount command.")

def setup(bot):
	bot.add_cog(Economy(bot))
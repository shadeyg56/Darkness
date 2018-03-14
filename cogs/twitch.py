import discord
from discord.ext import commmands
from twitchio import commands as tcommands
import sys
sys.path.insert(0, "/home/pi/Desktop")
import private


class Twitch_Bot(tcommand.TwitchBot):

	def __init__(self, bot):
		super().__init__(prefix='!', token=private.TWITCH_OAUTH, nick='Darkness', initial_channels=['shadeyg56'])
		self.bot = bot

	async def event_ready(self):
		print("Logged into twitch")

	@tcommands.twitch_command()
	async def test(self, ctx):
		await ctx.send("I am alive")

twitch_bot = Twitch_Bot()
twitch_bot.run()
def setup(bot)
bot.add_cog(Twitch_Bot(bot))
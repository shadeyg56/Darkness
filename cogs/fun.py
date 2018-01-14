import discord
from discord.ext import commands 
import cat
import random

class Fun():
	def __init__(self, bot):
		self.bot = bot
		self.answers = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes definitely', 'You may rely on it',
                     'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy try again',
                     'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again',
                     'Don\'t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good',
                     'Very doubtful']
		self.type = ["png", "gif"]

	@commands.command()
  	async def ball(self, ctx, *, question:str):
  		ans = random.randint(0, 19)
  		author = ctx.author
  		avatar = author.avatar_url
  		timestamp = ctx.message.created_at()
  		embed = discord.Embed(title="8ball", color=0xed, timestamp=timestamp)
  		embed.add_field(name='Question :question:', value=f"{question}")
  		embed.add_field(name="Answer :8ball:", value=self.answers[ans])
  		embed.add_footer(text="Asked at")
  		embed.set_thumbnail(url='http://legomenon.com/images/magic-8ball-first-white.jpg')
  		embed.set_author(name=author, icon_url=avatar)
  		await ctx.send(embed=embed)
  		await ctx.message.delete()

	@commands.command()
	async def cat(self, ctx):
                pic = random.randint(0,1)
                channel = ctx.channel
                x = cat.getCat(directory="cats", filename=None, format='{}'.format(self.type[pic]))
                with open(x, 'rb') as File:
                        await ctx.send(file=discord.File(File))




def setup(bot):
	bot.add_cog(Fun(bot))

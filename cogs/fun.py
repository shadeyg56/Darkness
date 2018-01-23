import discord
from discord.ext import commands 
import cat
import random
import asyncio

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
  		timestamp = ctx.message.created_at
  		embed = discord.Embed(title="8ball", color=0xed, timestamp=timestamp)
  		embed.add_field(name='Question :question:', value=f"{question}")
  		embed.add_field(name="Answer :8ball:", value=self.answers[ans])
  		embed.set_footer(text="Asked at")
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
			
	@commands.command()
	async def poker(self, ctx, opponent: discord.Member):
		num = random.randint(0, 24)
		num2 = random.randint(0, 24)
		num3 = random.randint(0, 24)
		num4 = random.randint(0, 24)
		author = ctx.author
		cards = ['ace of hearts ',' ace of spades ',' ace of clubs ',' ace of diamonds ',' one of hearts ',' one of spades',' one of hearts',' one of diamonds ',' two of hearts ',' two of spades ',' two of hearts ',' two of diamonds ',' three of hearts ',' three of spades ',' three of clubs',' three of diamonds ',' four of hearts ',' four of spades ',' four of clubs ',' four of diamonds ',' five of hearts ',' five of spades ',' five of clubs ',' five of diamonds ',' six of hearts ',' six of spades ',' six of clubs',' six of diamonds ',' seven of hearts ',' seven of spades ',' seven of clubs ',' seven of diamonds ',' eight of hearts ',' eight of spades ',' eight of clubs ',' eight of diamonds ',' nine of hearts ',' nine of spades ',' nine of clubs ',' nine of diamonds ',' ten of hearts ',' ten of spades ',' ten of clubs ',' ten of diamonds ',' jack of hearts ',' jack of spades ',' jack of clubs ',' jack of diamonds ',' queen of hearts ',' queen of spades ',' queen of clubs ',' queen of diamonds ',' king of hearts ',' king of spades ',' king of clubs ',' king of diamonds']
		hand_1 = [f'{cards[num]}', f'{cards[num2]}']
		hand_2 = [f'{cards[num3]}', f'{cards[num4]}']
		await ctx.send(f'{opponent.mention}, {ctx.author} has challenged you to a round of Texas Holdem Poker. Type `accept` to play')
		res = await self.bot.wait_for('message',check=lambda m: m.channel == ctx.channel)
		if res.content == 'accept':
			await ctx.send('Challenge accepted\n Dealing cards in DM..')
			await ctx.author.send(f'Here is your hand **{hand_1}**')
			await opponent.send(f'Here is your hand **{hand_2}**')
			await asyncio.sleep(5)
			await ctx.author.send('The opponent is going')
			await opponent.send('`Check`, `Call`, or `Fold`?')
			choice = await self.bot.wait_for('message')
			if choice.content.lower() == 'check':
				await opponent.send('You checked. It is the opponents turn now')
				await author.send('The oppenent checked\n`Check`, `Call` or `Fold`?')
		else:
			await ctx.send('Game declined')
			pass
			




def setup(bot):
	bot.add_cog(Fun(bot))

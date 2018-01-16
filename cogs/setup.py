import discord
from discord.ext import commands
import asyncio
import json

class Setup():
	def __init__(self, bot):
		self.bot = bot
	with open('cogs/utils/servers.json') as f:
			data = json.loads(f.read())
	@commands.command()
	async def setup(self, ctx):
		server = ctx.guild
		data[server.id] = {}
		x = await ctx.send('Welcome to the Darkness interactive setup')
		await asyncio.sleep(3)
		await ctx.send('Please enter a prefix (Enter None for default)')
		prefix = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
		if prefix.content == 'None':
			prefix.content  = '~'
		await ctx.send(f'Prefix set to {prefix.content}')
			
		await ctx.send('Enable welcome message?')
		msg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
		if msg.content == 'Yes':
			await ctx.send('What should the message say?')
			msg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
			await ctx.send('What channel should be the welcome channel?')
			welc_channel = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
			if welc_channel.content.startswith('<#'):
				await ctx.send(f'Welcome channel set to {welc_channel.content} with message {msg.content}')
			else:
				await ctx.send('Invalid channel. Please make sure you mention the channel')
				await ctx.send('What channel should be the welcome channel?')
				welc_channel = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)		
				await ctx.send(f'Welcome channel set to {welc_channel.content} with message {msg.content}')	
		else:
			pass
			
		await ctx.send('Enable leave message?')
		leave_msg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
		if leave_msg.content == 'Yes':
			await ctx.send('What should the message say?')
			leave_msg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
			await ctx.send(f'Leave message set to {leave_msg.content}')	
		else:
			pass
			
		data[server.id]['name'] = server.name 
		data[server.id]['prefix'] = prefix.content.strip('"')
		data[server.id]['welc_channel'] = welc_channel.content.strip('"')
		data[server.id]['welc_msg'] = msg.content.strip('"')
		data[server.id]['leave_msg'] = leave_msg.content.strip('"')
		
		data = json.dumps(data, indent=4, sort_keys=True)
		
		with open('cogs/utils/servers.json', 'w') as f:
			f.write(data)
		await ctx.send('Setup complete')
		
	@commands.command()
	async def config(self, ctx, setting, *, change):
		if setting == 'prefix':
			data[str(ctx.guild.id)]['prefix'] = change
			await ctx.send(f'Prefix set to `{change}`)
		
		
def setup(bot):
	bot.add_cog(Setup(bot))

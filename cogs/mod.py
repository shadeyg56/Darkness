import discord
from discord.ext import commands
import asyncio

class Mod():
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def purge(self, ctx, message_num: int):
		if True:
			try:
				await ctx.channel.purge(limit=message_num)
				x = await ctx.send(f"Deleted {message_num} messages")
				await asyncio.sleep(7)
				await x.delete()
			except discord.Forbidden:
				await ctx.send("I need **Manage Messages** for this")
			except MissingPermissions:
				await ctx.send("You need **Manage Messages** for this")

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, member:discord.Member):
		try:
			await ctx.guild.ban(member)
			await ctx.send(f"{member} was banned from the server")
		except discord.Forbidden:
			await ctx.send("I need **Ban Members** for this")

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def unban(self, ctx, member_id: int, *, reason=None):
		member = self.bot.get_user(member_id)
		try:
			await ctx.guild.unban(member,reason=reason)
			await ctx.send(f"{member} was unbanned from the server")
		except discord.Forbidden:
			await ctx.send("I need **Ban Members for that**")

	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, member:discord.Member):
		try:
			await ctx.guild.kick(member)
			await ctx.send(f"{member} was kicked from the server.")
		except discord.Forbidden:
			await ctx.send("I need **Kick Members** for that")
			
        @commands.command()
	@commands.has_permission(manage_roles=True)
	 async def removerole(self, ctx, user: discord.Member, *, rolename:str):
                role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.message.server.roles)
                if not role:
                        await ctx.send('That role doesnt exist')
                try:
                     await user.remove_roles(role)
                     await ctx.send('I removed the {} role from {}'.format(rolename, user))
                except discord.Forbidden:
                     await ctx.send('I need **Manage Roles** for this')
                else:
                      await ctx.send('You need *Manage Roles** for this') 


	@commands.command()
	@commands.has_permission(manage_roles=True)
	async def addrole(self, ctx, user: discord.Member, *, rolename:str):
                role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.message.server.roles)
                if not role:
                    await ctx.send('That role doesnt exist')
                try:
                    await user.add_roles(role)
                    await ctx.send('I removed the {} role from {}'.format(rolename, user))
                except discord.Forbidden:
                    await ctx.send('I need **Manage Roles** for this')
                else:
                     await ctx.send('You need *Manage Roles** for this')

       
	
def setup(bot):
	bot.add_cog(Mod(bot))

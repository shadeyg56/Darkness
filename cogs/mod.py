import discord
from discord.ext import commands
import asyncio
import json

class Mod():
    def __init__(self, bot):
            self.bot = bot
            self.embed_color = 0xd60606
            with open('cogs/utils/servers.json') as f:
            	self.data = json.load(f)
		
     
    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, length: int, *, reason: str='No reason given.'):
        """Temporarily bans a member for a specified amount of time."""
        if str(ctx.guild.id) in self.data:
	        mod_log = self.data[str(ctx.guild.id)]['mod_log']
	        mod_log = mod_log.replace('<', '')
	        mod_log = mod_log.replace('#', '')
	        mod_log = mod_log.replace('>', '')
	        mod_log = self.bot.get_channel(int(mod_log))
        if length > 10000:
            return await ctx.send('Length of ban is too long.')

        guild = ctx.guild
        author = ctx.author

        try:
            invitation = await ctx.channel.create_invite(max_uses = 1, xkcd = True)
        except discord.HTTPException:
            return  # we couldn't create an invite, so don't ban.

        user_embed = discord.Embed()
        user_embed.color = 0xd60606
        user_embed.title = 'You have been banned!'
        user_embed.description = f'{author.name} has banned you.\n\nInvite: {invitation.url}\n' \
                                 f'After your ban time is up, click this link to rejoin the server.'
        user_embed.add_field(name='Reason', value=reason)
        user_embed.add_field(name='Length', value=f'{length} seconds')

        public_embed = discord.Embed()
        public_embed.color = 0xd60606
        public_embed.title = f'{member.name} has been banned!'
        public_embed.description = f'This member was banned by {author.name}.'
        public_embed.add_field(name='Reason', value=reason)
        public_embed.add_field(name='Length', value=f'{length} seconds')

        try:
            await mod_log.send(embed=public_embed)
        except discord.HTTPException:
            pass  # couldn't send the public embed
        try:
            await member.send(embed=user_embed)
        except discord.HTTPException:
            return  # couldn't send the private message, so don't ban

        try:
            await member.ban(reason=reason, delete_message_days=0)
        except discord.HTTPException:
            return  # we couldn't ban them

        await asyncio.sleep(length)

        try:
            await member.unban(reason='Softban time expired.')
        except discord.HTTPException:
            pass  # we couldn't unban them
     
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, message_num:int):
    		try:
    					await ctx.message.delete()
    					await ctx.channel.purge(limit=message_num)
    					x = await ctx.send(f'Successfully deleted {message_num} messages')
    					await asyncio.sleep(7)
    					await x.delete()
    		except discord.Forbidden:
    					await ctx.send('I need **Manage Messages** for this')
						
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.Member, *, reason=None):
    			if str(ctx.guild.id) in self.data:
    							mod_log = self.data[str(ctx.guild.id)]['mod_log']
    							mod_log = mod_log.replace('<', '')
    							mod_log = mod_log.replace('#', '')
    							mod_log = mod_log.replace('>', '')
    							mod_log = self.bot.get_channel(int(mod_log))
    			try:  
    							await ctx.guild.ban(member, reason=reason)
    							await ctx.send(f"{member} was banned from the server")
    							embed = discord.Embed(title=f'{member.name} has been banned', description=f'This member was banned by {ctx.author}', color=self.embed_color)
    							embed.add_field(name='Reason', value=reason)
    							await mod_log.send(embed=embed)
    			except discord.Forbidden:
    							await ctx.send("I need **Ban Members** for this")
                        
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member_id: int, *, reason=None):
    			if str(ctx.guild.id) in self.data:
    				 mod_log = self.data[str(ctx.guild.id)]['mod_log']
    				 mod_log = mod_log.replace('<', '')
    				 mod_log = mod_log.replace('#', '')
    				 mod_log = mod_log.replace('>', '')
    				 mod_log = self.bot.get_channel(int(mod_log))
    			try:
    				member = self.bot.get_user(member_id)
    				await ctx.guild.unban(member,reason=reason)
    				await ctx.send(f"{member} was unbanned from the server")
    				embed = discord.Embed(title=f'{member.name} has been unbanned', description=f'This member was unbanned by {ctx.author}', color=self.embed_color)
    				embed.add_field(name='Reason', value=reason)
    				await mod_log.send(embed=embed)
    			except discord.Forbidden:
    				await ctx.send("I need **Ban Members for that**")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.Member, *, reason=None):
    		
    			try:
    				await ctx.guild.kick(member)
    				await ctx.send(f"{member} was kicked from the server.")
    				embed = discord.Embed(title=f'{member.name} has been kicked', description=f'This member was kicked by {ctx.author}', color=self.embed_color)
    				embed.add_field(name='Reason', value=reason)
    				await mod_log.send(embed=embed)
    			except discord.Forbidden:
    				await ctx.send("I need **Kick Members** for that")
				

		
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, user: discord.Member, *, rolename:str):
            role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.guild.roles)
            if not role:
                    await ctx.send('That role doesnt exist')
            try:
                    await user.add_roles(role)
                    await ctx.send('I added the {} role from {}'.format(rolename, user))
            except discord.Forbidden:
                    await ctx.send('I need **Manage Roles** for this')
      
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, user: discord.Member, *, rolename:str):
            role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.guild.roles)
            if not role:
                    await ctx.send('That role doesnt exist')
            try:
                    await user.remove_roles(role)
                    await ctx.send(f'I removed the {rolename} role from {user}')
            except discord.Forbidden:
                    await ctx.send('I need **Manage Roles** for that')
			
    @commands.command()
    @command.has_permission(manage_guild=True)
    async def warn(self, ctx, user: discord.Member, *, reason:str):
    	guild = str(ctx.guild.id)
    	if str(ctx.guild.id) in self.data:
    		mod_log = self.data[str(ctx.guild.id)]['mod_log']
    		mod_log = mod_log.replace('<', '')
    		mod_log = mod_log.replace('#', '')
    		mod_log = mod_log.replace('>', '')
    		mod_log = self.bot.get_channel(int(mod_log))
    	with open('cogs/utils/warns.json') as f:
    		warn = json.load(f)
    	if guild not in warn:
    		warn[guild] = {}
    		warn[guild][user.name] = {}
    	try:
    		warn[guild][user.name] = reason
    		await ctx.send(f'**{user.name}** was warned')
    		await user.send(f'You were warned in **{ctx.guild}** by **{ctx.author}** for: **{reason**}')
    		embed = discord.Embed(title=f'{user.name} has been warned', description=f'This member was warned by {ctx.author}', color=self.embed_color)
    		embed.add_field(name='Reason', value=reason)
    		warns = json.dumps(warns, indent=4, sort_keys=True)
    		with open('cogs/utils/warns.json', 'w') as f:
    			f.write(warns)
			
	except:
		pass
def setup(bot):
	bot.add_cog(Mod(bot))

import discord
from discord.ext import commands
import utils

class Utils():
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context = True)
    async def utils(self, ctx):
        await self.bot.say('The util cog is working')
        
    @commands.command(pass_context = True)
    async def addrole(self, ctx, user: discord.Member, role: str):
        server_roles = [role for role in ctx.message.server.roles if not role.is_everyone]
        add = discord.utils.get(server_roles, '{}'.format(role))
        if ctx.message.author.server_permissions.manage_roles:
            await self.bot.add_roles(user, add)
            await self.bot.say('I gave {} the {} role'.format(user, role))
        
        
def setup(bot):
    bot.add_cog(Utils(bot))
        
        
    

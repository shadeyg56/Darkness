import discord
from ext.commands import Bot
from ext import commands
from .utils import launcher
import asyncio

class Mod():


    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context = True)
    async def mod_test(self,ctx):
        await self.bot.say('The mod cog is working')
        
    def mod(ctx):
        info = launcher.config()
        server = ctx.message.server
        s_owner = server.owner
        modrole = discord.utils.get(server.roles, id=info[server.id]['mod_role'])
        adminrole = discord.utils.get(server.roles, id=info[server.id]['admin_role'])
        author = ctx.message.author
        def is_owner(ctx):
            return ctx.message.author.id == owner
        if author is s_owner:
            return True
        if is_owner(ctx):
            return True
        if modrole:
            modrole = modrole.name
        if adminrole:
            adminrole = adminrole.name
        if discord.utils.get(author.roles,name=adminrole):
            return True
        return discord.utils.get(author.roles,name=modrole)
    
    
    @commands.command(pass_context = True, name='kick')
    async def kick(self, ctx, member: discord.Member):       
        if ctx.message.author.server_permissions.kick_members:
            try:
                await self.bot.kick(member)
                await self.bot.say('{} was kicked'.format(member))
            except discord.Forbidden:
                await self.bot.say("I need **Kick Members** for this")
            else:
                 await self.bot.say('You need **Kick Members for this')
                
    @commands.command(pass_context = True)
    async def ban(self, ctx, member: discord.Member):       
        if ctx.message.author.server_permissions.ban_members:
            try:
                await self.bot.ban(member)
                await self.bot.say('{} was banned'.format(member))
            except discord.Forbidden:
                await self.bot.say("I need **Ban Members** for this")
            else:
                 await self.bot.say('You need **Ban Members** for this')
               
    @commands.command(pass_context = True)
    async def unban(self, ctx, member: str): 
        server = ctx.message.server
        mem = discord.Object(id=member)
        if ctx.message.author.server_permissions.ban_members:
            try:
                await self.bot.unban(server, mem)
                await self.bot.say('{} was unbanned'.format(mem))
            except discord.Forbidden:
                await self.bot.say("I need **Ban Members** for this")
            else:
                 await self.bot.say('You need **Ban Members** for this')
                
    @commands.command(pass_context = True)
    async def purge(self,ctx, msgs: int):
        text = 'Deleted {} messages'
        channel = ctx.message.channel
        if ctx.message.author.server_permissions.manage_messages:
            try:
                await self.bot.delete_message(ctx.message)
                await self.bot.purge_from(channel, limit=msgs)
                x = await self.bot.say(text.format(msgs))
                await asyncio.sleep(7)
                await self.bot.delete_message(x)
            except discord.Forbidden:
                await self.bot.say('I need **Manage Messages** for this')
            else:
                 await self.bot.say('You need **Manage Messages** for this')
                
    @commands.command(pass_context = True)
    async def softban(self, ctx, member: discord.Member):
        server = ctx.message.server
        if ctx.message.author.server_permissions.kick_members:
            try:
                await self.bot.ban(member)
                await self.bot.unban(server, member)
                await self.bot.say('{} was softbanned'.format(member))
            except discord.Forbidden:
                await self.bot.say('I need **Ban Members** for this')
  
        
                     
                
                
                
        
                      
                         
                           
    
        
        
def setup(bot):
    bot.add_cog(Mod(bot))
 

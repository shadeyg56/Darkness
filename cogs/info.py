import discord
from discord.ext import commands

class Info():
   
    def __init__(self, bot):
        self.bot = bot
      
    @commands.command(pass_context=True)
    async def infotest(self, ctx):
        await self.bot.say('The info cog is working')
      
    @commands.command(pass_context=True)
    async def serverinfo(self, ctx):
        server = ctx.message.server
        total_members = len(server.members)
        online = len([x.status for x in server.members
                      if x.status == discord.Status.online or x.status == discord.Status.idle or x.status == discord.Status.dnd])
        embed = discord.Embed(title='Server Info', color=0xed)
        embed.set_author(name=server.name, icon_url=server.icon_url)
        embed.set_thumbnail(url=server.icon_url)
        embed.add_field(name='Members', value='{} total\n{} online'.format(total_members, online))
        await self.bot.say(embed=embed)
                      
                          
                       
        
def setup(bot):
    bot.add_cog(Info(bot))
  

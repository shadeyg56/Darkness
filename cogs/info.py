import discord
from discord.ext import commands

class Info():
   
    def __init__(self, bot):
        self.bot = bot
      
    @commands.command(pass_context=True)
    async def info(self, ctx):
        await self.bot.say('The info cog is working')
        
def setup(bot):
    bot.add_cog(Info(bot))
  

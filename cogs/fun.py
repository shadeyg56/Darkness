import discord
from discord.ext import commands

class Fun():
    def __init__(self, bot):
         self.bot = bot
         
    @commands.command()
    async def funtest(self):
        await self.bot.say('The fun cog is working')
        
def setup(bot):
    bot.add_cog(Fun(bot))
    
    

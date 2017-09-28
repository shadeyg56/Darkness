import discord
from discord.ext import commands

class Utils():
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context = True)
    async def utils(self, ctx):
        await self.bot.say('The utils cog is working')
        
def setup(bot):
    bot.add_cog(Utils(bot))
        
        
    

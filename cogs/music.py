import discord
from discord.ext import commands

class Music():
    
    def __init__(self, bot):
         self.bot = bot
         
    @commands.command()
    async def musictest(self):
        await self.bot.say('The music cog is working')
        
def setup(bot):
    bot.add_cog(Music(bot))

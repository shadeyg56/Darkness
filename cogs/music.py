import discord
from discord.ext import commands
import youtube_dl
import opus

class Music():
    
    def __init__(self, bot):
         self.bot = bot
            
         self.voice = await self.bot.join_voice_channel
         
    @commands.command()
    async def musictest(self):
        await self.bot.say('The music cog is working')
        
    @commands.command(pass_context=True)
    async def play(self, ctx, songname: str = None):
        player = await self.voice.create_ytdl_player('https://youtube.com/watch?v=Fz50hqWrHUY')
        discord.opus.load_opus()
        player.start()
        
        
        
def setup(bot):
    bot.add_cog(Music(bot))

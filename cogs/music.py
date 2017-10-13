import discord
from discord import opus
from discord.ext import commands
import youtube_dl

class Music():
    
    def __init__(self, bot):
         self.bot = bot
            
        
         
    @commands.command()
    async def musictest(self):
        await self.bot.say('The music cog is working')
        
    @commands.command(pass_context=True)
    async def play(self, ctx, songname: str = None):
        channel = ctx.message.author.voice.voice_channel
        discord.opus.load_opus(music)
        voice = self.bot.join_voice_channel(channel)
        player = await voice.create_ytdl_player('https://www.youtube.com/watch?v=Fz50hqWrHUY')
        player.start()
        
        
        
def setup(bot):
    bot.add_cog(Music(bot))

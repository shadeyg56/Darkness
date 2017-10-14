import discord
from discord import opus
from discord.ext import commands
import youtube_dl


    
    def __init__(self, bot):
         self.bot = bot
            
class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = ' {0.title} uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.bot.send_message(self.current.channel, 'Now playing' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()
            
class Music():
    def __init__(self, bot):
         self.bot = bot
    self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state
    
    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    
    @commands.command()
    async def musictest(self):
        await self.bot.say('The music cog is working')
        
    @commands.command(pass_context=True)
    async def play(self, ctx, songname: str = None):
        channel = ctx.message.author.voice.voice_channel
        voice = self.bot.join_voice_channel(channel)
        player = await voice.create_ytdl_player('https://www.youtube.com/watch?v=Fz50hqWrHUY')
        player.start()
        
    @commands.command(pass_context=True)
    async def summon(self, ctx):
        voice = self.bot.join_voice_channel(ctx.message.author.voice.voice_channel)
        await voice
     
    @commands.command(pass_context=True)
    async def disconnect(self, ctx):
        del self.voice_states[server.id]
        await state.voice.disconnect()
        
        
    
        
        
        
def setup(bot):
    bot.add_cog(Music(bot))

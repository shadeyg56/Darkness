import discord
from discord.ext import commands
import cat
import random
import asyncio
from pokemonNames.pokemonNames import PokemonNames

class Fun():
    def __init__(self, bot):
         self.bot = bot
         self.answers = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes definitely', 'You may rely on it',
                     'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy try again',
                     'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again',
                     'Don\'t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good',
                     'Very doubtful']
         self.type = ['png', 'gif']   
         
    @commands.command()
    async def funtest(self):
        await self.bot.say('The fun cog is working')
        
    
    @commands.command(pass_context = True, aliases=['8ball'])
    async def ball(self, ctx, *, question):
        ans = random.randint(0, 19)
        author = ctx.message.author
        avatar = author.avatar_url
        timestamp = ctx.message.timestamp
        embed = discord.Embed(title='8ball', color=0xed, timestamp=timestamp)
        embed.add_field(name='Question :question:', value='{}'.format(question))
        embed.add_field(name='Answer :8ball:', value=self.answers[ans])
        embed.set_footer(text='Asked at')
        embed.set_thumbnail(url='http://legomenon.com/images/magic-8ball-first-white.jpg')
        embed.set_author(name=author, icon_url=avatar)
        await self.bot.say(embed=embed)
        await self.bot.delete_message(ctx.message)
        
    @commands.command(pass_context=True)
    async def cat(self, ctx):
        pic = random.randint(0,1)
        channel = ctx.message.channel
        x = cat.getCat(directory=None, filename=None, format='{}'.format(self.type[pic]))
        with open(x, 'rb') as f:
            await self.bot.send_file(channel, f)
         
    @commands.command(pass_context=True)
    async def virus(self, ctx, victim: discord.Member = None, *, virusname: str = None):
        if not victim:
            victim = ctx.message.server
        if not virusname:
            virusname = 'discord'
        x = await self.bot.say('[▓▓▓             ] / {}-virus.exe Packing Files.'.format(virusname))
        await asyncio.sleep(0.5)
        x = await self.bot.edit_message(x, '[▓▓▓                    ] - {}-virus.exe Packing Files.'.format(virusname)) 
        await asyncio.sleep(0.5)                        
        x = await self.bot.edit_message(x, '[▓▓▓▓▓▓             ] \ {}-virus.exe Packing Files..'.format(virusname))    
        await asyncio.sleep(0.5)                        
        x = await self.bot.edit_message(x, '[▓▓▓▓▓▓▓▓▓          ] | {}-virus.exe Initializing code.'.format(virusname))
        await asyncio.sleep(0.5)                        
        x = await self.bot.edit_message(x, '[▓▓▓▓▓▓▓▓▓▓▓▓       ] \ {}-virus.exe Initializing code..'.format(virusname))
        await asyncio.sleep(0.5)                        
        x = await self.bot.edit_message(x, '[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ] - {}-virus.exe Finishing.'.format(virusname))
        await asyncio.sleep(0.5)                        
        x = await self.bot.edit_message(x, '[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓] | {}-virus.exe Finishing..'.format(virusname))   
        await asyncio.sleep(0.5)                        
        x = await self.bot.edit_message(x,'``Successfully downloaded {}-virus.exe``'.format(virusname))
        await asyncio.sleep(2)
        x = await self.bot.edit_message(x,'``Injecting virus.   |``')
        await asyncio.sleep(0.5)
        x = await self.bot.edit_message(x,'``Injecting virus..  /``')
        await asyncio.sleep(0.5)
        x = await self.bot.edit_message(x,'``Injecting virus... -``')
        await asyncio.sleep(0.5)
        x = await self.bot.edit_message(x,'``Injecting virus....\``')
        await self.bot.delete_message(x)
        await self.bot.delete_message(ctx.message)                      
        await self.bot.say('Succesfully injected {}-virus.exe into {}'.format(virusname, victim))    
        
    @commands.command(pass_context=True)
    async def whosthatpokemon(self, ctx):
        num = random.randint(0, 721)
        pic = 'sprites/sprites/pokemon/{}.png'.format(num)
        with open(pic) as f:
             file = json.loads(f.read())
        p = PokemonNames()
        x = p.get_name(num)
        embed = discord.Embed(title='Who\'s this Pokemon?', color =0x00FF00)
        await self.bot.send_file(ctx.message.channel, file)
        msg = await self.bot.wait_for_message(timeout=60, author=ctx.message.author)
        if msg.content == x:
            await self.bot.say('Correct. That Pokemon is {}'.format(x))
        if not msg.content == x:
            await self.bot.say('Incorrect. That Pokemon is {}'.format(x))
                                
def setup(bot):                               
    bot.add_cog(Fun(bot))
    
    

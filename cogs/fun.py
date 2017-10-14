import discord
from discord.ext import commands
import cat
import random
import asyncio

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
            
        
    
        
def setup(bot):
    bot.add_cog(Fun(bot))
    
    

import discord
from ext.commands import Bot
from ext import commands
import datetime
import time
import random
import asyncio
import json
from .utils import launcher


class Old_Misc():


    def __init__(self, bot):
        self.bot = bot
        
        
    async def send_cmd_help(self,ctx):
        if ctx.invoked_subcommand:
            pages = self.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)     
        else:
           pages = self.bot.formatter.format_help_for(ctx, ctx.command)
           for page in pages:
               await self.bot.send_message(ctx.message.channel, page)
     
    
    @commands.command(pass_context = True)
    async def ping(self,ctx):
        pingtime = time.time()
        ping = time.time() - pingtime
        pong = discord.Embed(title='Pong! Response Time:', description=str(ping), color=0xed)
        await self.bot.say(embed=pong)
        
    @commands.command(pass_context = True)
    async def test(self, ctx):
        await asyncio.sleep(2)
        await self.bot.say('Hello')
        
    @commands.command(pass_context = True)
    async def invite(self, ctx):
        await self.bot.say('**Darkness Invite:** https://discordapp.com/oauth2/authorize?client_id=355189919410421760&scope=bot&permissions=66186303')
                      
    @commands.command(pass_context = True)
    async def suggest(self, ctx, message: str):
        timestamp = ctx.message.timestamp
        server = ctx.message.server
        message = ctx.message.content
        author = ctx.message.author
        channel = self.bot.get_channel('356602525740433408')
        avatar = author.avatar_url
        suggestion = discord.Embed(title='Suggestion', description='{}'.format(message), color=0xed, timestamp=timestamp)
        suggestion.set_author(name=author, icon_url=avatar)
        suggestion.set_footer(text='Sent from {}'.format(server))
        await self.bot.send_message(channel, embed=suggestion)
        await self.bot.say('Suggestion added')
        
    @commands.command(pass_context = True)
    async def support(self, ctx):
        await self.bot.say('**Darkness Support:** https://discord.gg/Jjdp8hf')
                       
    @commands.command(pass_context = True)
    async def info(self, ctx):
        stamp = ctx.message.timestamp
        embed = discord.Embed(title='Darkness Info', color=0xed, timestamp=stamp)
        servers = len(self.bot.servers)                    
        embed.add_field(name='Author', value='<@300396755193954306>')
        embed.add_field(name='Servers', value=servers)
        embed.add_field(name='Prefix', value='d.')
        embed.set_footer(text='Powered by discord.py')
        embed.set_thumbnail(url='http://data.whicdn.com/images/150102219/large.gif')
        embed.add_field(name='Invite', value='https://discordapp.com/oauth2/authorize?client_id=355189919410421760&scope=bot&permissions=66186303')
        embed.add_field(name='Support', value='https://discord.gg/Jjdp8hf')
        embed.add_field(name='GitHub', value='https://github.com/shadeyg56/darkness')
        await self.bot.say(embed=embed)    
        
    @commands.command(pass_context = True)
    async def calc(self,ctx,num: float, num2: float, Type=None):
        if Type == 'add':
            add = num + num2
            await self.bot.say(add)
        if Type == 'subtract':
            dif = num - num2
            await self.bot.say(dif)
        if Type == 'multiply':
            product = num * num2
            await self.bot.say(product)
        if Type == 'division':
            div = num / num2
            await self.bot.say(div)
        if Type == 'exponents':
            expo = num ** num2
            await self.bot.say(expo)
        if Type == None:
            await self.bot.say('Please specify a type (add, subtract, multiply, divide, exponents')
            
            
        
            
    @commands.command(pass_context = True)
    async def remind(self, ctx, time: int,*, task: str):
        user = ctx.message.author
        time2 = time * 60
        await self.bot.say('Ill remind you to {} in {} minutes'.format(task, time))
        await asyncio.sleep(time2)
        await self.bot.say('{0.mention} make sure you {1}'.format(user, task))
        
    @commands.command(pass_context = True)
    async def partner(self, ctx):
        channel = self.bot.get_channel('360910860090343424')
        channel2 = ctx.message.channel
        timestamp = ctx.message.timestamp
        author = ctx.message.author
        avatar = author.avatar_url
        if ctx.message.server.id == '294262760752152576':
            await self.bot.say('What is your server name?')
            name = await self.bot.wait_for_message(timeout=30.0, author=author)
            await self.bot.say('How many humans are in your server?')
            humans = await self.bot.wait_for_message(timeout=30.0, author=author)
            await self.bot.say('Please provide a detailed description of your server.')
            desc = await self.bot.wait_for_message(timeout=30.0, author=author)
            await self.bot.say('Finally please provide a invite link')
            inv = await self.bot.wait_for_message(timeout=30.0, author=author)
            await self.bot.purge_from(channel2, limit=8)
            await self.bot.say('Your submission has been entered. Please dont bug the inspectors, they will check your server when they have time')
            embed = discord.Embed(title='New Submission', color=0xed, timestamp=timestamp)
            embed.add_field(name='Server Name', value=name.content)
            embed.add_field(name='Humans', value=humans.content)
            embed.add_field(name='Server Description', value=desc.content)
            embed.add_field(name='Invite', value=inv.content)
            embed.set_author(name=author, icon_url=avatar)
            embed.set_footer(text='Submitted at')
            await self.bot.send_message(channel, embed=embed)
        elif name == None:
              await self.bot.say('Sorry, you took too long')
        elif humans == None:
              await self.bot.say('Sorry, you took too long')
        elif desc == None:
              await self.bot.say('Sorry, you took too long')
        elif inv == None:
              await self.bot.say('Sorry, you took too long')
        elif not ctx.message.server.id == '294262760752152576':
              await self.bot.say('This command can only be ran in the Dragons and Kats server\n. If you arent in this server, you can join with this invite link: https://discord.gg/uEC84cR')
        
        
       
            
    
       
def setup(bot):
    bot.add_cog(Old_Misc(bot))

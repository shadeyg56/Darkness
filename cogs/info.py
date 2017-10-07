import discord
from discord.ext import commands

class Info():
   
    def __init__(self, bot):
        self.bot = bot
      
    @commands.command(pass_context=True)
    async def infotest(self, ctx):
        await self.bot.say('The info cog is working')
      
    @commands.command(pass_context=True)
    async def serverinfo(self, ctx):
        server = ctx.message.server
        total_members = len(server.members)
        online = len([x.status for x in server.members
                      if x.status == discord.Status.online or x.status == discord.Status.idle or x.status == discord.Status.dnd])
        date = server.created_at
        text_channels = len([m for m in server.channels
                             if m.type == discord.ChannelType.text])
        voice_channels = len(server.channels) - text_channels
        embed = discord.Embed(title='Server Info', color=0xed)
        embed.set_author(name=server.name, icon_url=server.icon_url)
        embed.set_thumbnail(url=server.icon_url)
        embed.add_field(name='Owner', value=server.owner)
        embed.add_field(name='ID', value=server.id)
        embed.add_field(name='Members', value='{} total\n{} online'.format(total_members, online))
        embed.add_field(name="Roles", value=len(server.roles))
        embed.add_field(name='Text Channels', value=text_channels)
        embed.add_field(name='Voice Channels', value=voice_channels)
        embed.add_field(name='Region', value=server.region)
        embed.set_footer(text=date)
        await self.bot.say(embed=embed)
      
   
    @commands.command(pass_context=True)
    async def userinfo(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.message.author
        roles = sorted([a.name a for a in user.roles if a.name != '@everyone'])
        avatar = user.avatar_url
        created = user.created_at
        member_number = sorted(server.members,key=lambda m: m.joined_at).index(user) + 1
        embed = discord.Embed(title='User Info', description='{} is chilling in {} mode'.format(user, user.status), color=0xed)
        embed.set_author(name=user, icon_url=avatar)
        embed.set_thumbnail(url=avatar)
        embed.add_field(name='Account Created', value=created.__format__('%A, %d. %B %Y'))
        embed.add_field(name='Date Joined', value=user.joined_at.__format__('%A, %d. %B %Y'))
        embed.add_field(name='Join number', value=member_number)
        embed.add_field(name='Nickname', value=user.nick)
        embed.add_field(name='Roles', value=roles)
        embed.set_footer(text='ID:' + user.id)
        await self.bot.say(embed=embed)
                         
                       
        
def setup(bot):
   
    bot.add_cog(Info(bot))
  

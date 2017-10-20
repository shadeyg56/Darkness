import discord
class Blacklists():
   
    def __init__(self, bot):
         self.bot = bot
         
    def if_blacklisted(self, user):
        with open('cogs/utils/blacklists.json') as f:
             blacklist = json.loads(f.read())
             if blacklist["blacklists"][user.id] == user.id:
                 

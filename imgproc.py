'''NAMSLA'S IMAGE PROCESSING COMMANDS.'''

import subprocess
import random
import re
from configparser import ConfigParser
import string
import discord
from discord.ext import commands

parser = ConfigParser()
parser.read('config.ini')

whitelist = ["250040817366990848"]

class Art:
    '''Art
    '''
    def __init__(self, bot):
        self.bot = bot

        
    def is_in_server_list(server_list):
        def predicate(ctx):
            return ctx.message.server.id in server_list
        return commands.check(predicate)
        
        
    #@commands.command()
    @commands.group(pass_context=True)
    @commands.has_any_role("Purple", "The Boss of this Gym", "Green", "Loli's Group")
    @is_in_server_list(whitelist)
    async def tweet(self,ctx, *, garbage:str = "DICKS EVERYWHERE"):
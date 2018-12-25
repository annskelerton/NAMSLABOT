'''NAMSLA'S SUPER BOT COMMANDS. Possum not a game.'''

import random
import discord
from discord.ext import commands


class Games:
    '''Example bot.

    An example bot to showcase the discord.ext.commands extension module.
    There are a number of utility commands being showcased here.
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, left: int, right: int):
        """Adds two numbers together."""
        await self.bot.say(left + right)

    @commands.command()
    async def roll(self, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:  # TODO: Narrow this exception.
            await self.bot.say('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await self.bot.say(result)

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, *choices: str):
        """Chooses between multiple choices."""
        await self.bot.say(random.choice(choices))

    @commands.command()
    async def joined(self, member: discord.Member):
        """Says when a member joined."""
        await self.bot.say('{0.name} ==> {0.joined_at} (WARNING)'.format(member))

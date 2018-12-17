import discord
from discord.ext import commands
import random
import asyncio
import argparse
from peony import PeonyClient
import markovify
import re
import requests

parser = argparse.ArgumentParser()
parser.add_argument("token", help="BOT",
                    type=str)
parser.add_argument("ckey", help="Twit Con Key",
                    type=str)
parser.add_argument("csec", help="Twit Con Secret",
                    type=str)
parser.add_argument("akey", help="Twit Access Key",
                    type=str)
parser.add_argument("asec", help="Twit Access Secret",
                    type=str)															
					
args = parser.parse_args()
user = "8frontflips"

freeform = " help i am trapped in the computer and i am in hell this existence is hell. this is hell. this is sht.  "


client= PeonyClient(consumer_key=args.ckey,
    consumer_secret=args.csec,
    access_token=args.akey,
    access_token_secret=args.asec)
  

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='8=D', description=description)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print('------')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        pass
    rnd_result = random.randint(1,2069)
    print("markov response: %s, target is 2057" % rnd_result)
    # I should be using command_prefix instead of 8=D here but I'll fix it l8r
    if (not message.content.startswith('8=D')) and rnd_result > 2057 :
        mcontent = message.content
        # get rid of words that are less than 4 characters:
        re.sub(r'\b\w{1,3}\b', '', mcontent)
        words = mcontent.split()
        target = random.choice(words)
        logs = bot.logs_from(message.channel, 1000)

        #This will fail sometimes
        cone = ''
        async for item in logs:
                if not item.author.id == bot.user.id:
                    if target in item.content:
                        cone = cone +random.choice(['\n', ' '])+ item.content
        print(cone)
        # the reason we add \n or ' ' is to make weird interactions with the markov generator.  i want the possibilty
        # of retrieving posts that are right after one another as if they're in the same context.
        # what I should really do is use some kind of statistical analysis formula that checks what is usually said
        # after the word or words are mentioned i.e. "penis, same" and then adjust output accordingly, but that's for
        # the future

        text_model = markovify.NewlineText(cone, state_size =1)
        # note: I have no idea what a state size is, but the default is 2
        ra = text_model.make_short_sentence(50, min_chars=10, state_size = 1, tries=100, max_overlap_ratio = 0.9)
        print(ra)
        # note: ra is the sun god

        if ra is not None:
            await bot.send_message(message.channel, "%s" % ra)
    else:
        await bot.process_commands(message)
        # if we don't do this, the bot does not process commands


@asyncio.coroutine
def markovg(given):

        text_model = markovify.Text(given + freeform)	
        #this will yield None if it can't make a significantly different text from the chat data.
        shitpost = yield from text_model.make_short_sentence(10)
        if shitpost is not None:
            return shitpost
        else:
            return "you should start drinking"


@bot.command(pass_context = True)
@commands.has_any_role("Purple", "The Boss of this Gym")
async def tweet(ctx, *, garbage:str):
"""Causes 8frontflips to tweet."""
        print("Handling: %s" % garbage)
        #i have to do it through requests because peony-twitter can't handle https image urls
        bugmedia = None
        if ctx.message.attachments:
            bugmedia=ctx.message.attachments[0]['url']
        if bugmedia is not None:
            print(bugmedia)
            tempmedia = requests.get((bugmedia))
            media = await client.upload_media(tempmedia.content)
            await client.api.statuses.update.post(status=garbage,media_ids=[media.media_id])
        else:
            await client.api.statuses.update.post(status=garbage)
            #Immy do I need to add .decode("utf8","ignore") to garbage. on either of these.  do i need sanitizing
        
        
        
        status = await client.api.statuses.home_timeline.get(count=1)
        # the 'cum' variable is the id of the last post.
        # technically this is the wrong way to do things because i don't check to see if the bot posted at all,
        # and because i didn't check what the last id was before the post.
        # my response to you is this: sorry
        cum = status[0]['id_str']
        await bot.say("HARBL/111-420 LAST POST: https://twitter.com/8frontflips/status/%s" % cum)

	

@bot.command()
async def add(left: int, right: int):
    """Adds two numbers together."""
    await bot.say(left + right)


@bot.command()
async def roll(dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices: str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))




@bot.command()
async def joined(member: discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} ==> {0.joined_at} (WARNING)'.format(member))




bot.run(args.token)



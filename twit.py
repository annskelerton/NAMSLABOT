'''NAMSLA'S Extended Commands, including Tweet.'''

import random
import asyncio
import re
from configparser import ConfigParser
import discord
from discord.ext import commands
import markovify
import requests
from nltk import word_tokenize
import nltk
from peony import PeonyClient
from games import Games
import networkx as nx
import numpy as np


nltk.download('brown')
nltk.download('punkt')

parser = ConfigParser()
parser.read('config.ini')

user = parser.get('twitter', 'user')
# to do: whitelist draw from config.ini
whitelist = ["250040817366990848"]

freeform = " help i am trapped in the computer and i am in hell this existence is hell. this is hell. this is sht.  "
last_conversation_channel = None
min_bg_seconds = int(parser.get('general', 'disability_awareness_min_time'))
max_bg_seconds = int(parser.get('general', 'disability_awareness_max_time'))
cur_bg_seconds = int(parser.get('general', 'disability_awareness_max_time'))
runonce = int(parser.get('general', 'speak_on_start'))
botuser = None
botname = parser.get('general', 'botname' )

# we should really set up a config file.

client = PeonyClient(
    consumer_key=parser.get('twitter', 'ckey'),
    consumer_secret=parser.get('twitter', 'csec'),
    access_token=parser.get('twitter', 'akey'),
    access_token_secret=parser.get('twitter', 'asec'))


class Twit:

    def __init__(self, bot):
        self.bot = bot

        # TODO: should streamline this
        # Consider using a hashmap;
        # { chr: replacements }
        # Then you could do hashmap[character] instead of this.

    # have bot occasionally say "i am disabled"
    # rand 3600 to 172800 : between 1 hour and 2 days






    @asyncio.coroutine
    def markovg(given):

            text_model = markovify.Text(given + freeform)	
            #this will yield None if it can't make a significantly different text from the chat data.
            shitpost = yield from text_model.make_short_sentence(10)
            if shitpost is not None:
                return shitpost
            else:
                return "you should start drinking"

    def is_in_server_list(server_list):
        def predicate(ctx):
            return ctx.message.server.id in server_list
        return commands.check(predicate)

    #@bot.command(pass_context = True)
    @commands.group(pass_context=True)
    @commands.has_any_role("Purple", "The Boss of this Gym", "Green", "Loli's Group")
    @is_in_server_list(whitelist)
    async def tweet(self,ctx, *, garbage:str = "DICKS EVERYWHERE"):
            """Causes 8frontflips to tweet (NAMSLA SERVER ONLY)"""
            print("Handling: %s" % garbage)

            botuser = await client.user
            id = botuser.id
            #status = client.api.statuses.user_timeline.get(user_id=id, count=1) 
            # status = request.iterator.with_max_id(client.api.statuses.user_timeline.get(user_id=id,count=1))
            request = await client.api.statuses.user_timeline.get(user_id=id,
                                                        count=1,
                                                        )

            # status = request.iterator.with_max_id()
            failed = 0
            failstring = ''
            oldid = request[0]['id_str']		
            #user_tweets = []
            #async for tweets in status:
            #    print(tweets.id_str)
            #    cum = (user_tweets.extend(tweets))['id_str'] #tweets['id_str']
            
            #i have to do it through requests because peony-twitter can't handle https image urls
            bugmedia = None
            if garbage == None:
                garbage = 'DICKS EVERYWHERE'
            if ctx.message.attachments:
                bugmedia=ctx.message.attachments[0]['url']
            try:
                if bugmedia is not None:
                    print(bugmedia)
                    tempmedia = requests.get((bugmedia))
                    media = await client.upload_media(tempmedia.content)
                    await client.api.statuses.update.post(status=garbage,media_ids=[media.media_id])
                else:
                    await client.api.statuses.update.post(status=garbage)
                    #Immy do I need to add .decode("utf8","ignore") to garbage. on either of these.  do i need sanitizing
            except Exception as e:
                failstring = str(e)
                failed = 1
            ## status = await client.api.statuses.home_timeline.get(count=1)
            request = await client.api.statuses.user_timeline.get(user_id=id,
                                                        count=1,
                                                        )

            # status = request.iterator.with_max_id()

            cum = request[0]['id_str']
            # the 'cum' variable is the id of the last post.
            # technically this is the wrong way to do things because i don't check to see if the bot posted at all,
            # and because i didn't check what the last id was before the post.
            # my response to you is this: sorry
            # cum = status[0]['id_str']
            if int(cum) > int(oldid) and not failed:
                await self.bot.say("HARBL/111-420 LAST POST: \U000022B7 https://twitter.com/8frontflips/status/%s" % cum)
            elif int(cum) > int(oldid) and failed and failstring is not None:
                await self.bot.say("HARBL/69-666 **MESSAGE FAILED** SHOOT THE MOON: \U000022B7 https://twitter.com/8frontflips/status/%s" % cum)
            elif int(cum) <= int(oldid) and failed and failstring is not None:
                await self.bot.say("HARBL/69-400-V **MESSAGE FAILED** TRY POSTING AGAIN IDIOT (error: %s)" % failstring)
            else:
                await self.bot.say("HARBL/69-303 **MESSAGE FAILED** (UNKNOWN) LAST POST: \U000022B7 https://twitter.com/8frontflips/status/%s" % cum)



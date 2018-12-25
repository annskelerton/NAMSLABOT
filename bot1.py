'''NAMSLA'S SUPER BOT. Likes Racoons'''

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


description = '''NAMSLA's personal bot.
Warning, under any circumstances, do not, and I repeat, do not'''
bot = commands.Bot(command_prefix='8=D', description=description)


@bot.event
async def on_ready():
    '''Runs once the bot is ready.'''
    runonce = 0
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print('------')
    activity = discord.Game(name="Team Fortress 2", type=1)
    await bot.change_presence(status=discord.Status.online, game=activity)
    print('------')
    # twitter, not discord
    botuser = await client.user

@asyncio.coroutine
def nearby(character):
    # we probably could have altered a spellcheck library for this
    G=nx.Graph()
    G.add_nodes_from("`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./")
    G.add_weighted_edges_from([('1','2',0.5), ('1','`',0.5), ('1','q',0.25)])
    G.add_weighted_edges_from([('2','3',0.25), ('2','q',0.55), ('2','w',0.5)])
    G.add_weighted_edges_from([('3','w',0.5), ('3','e',0.75), ('3','4',0.5)])
    G.add_weighted_edges_from([('4','r',0.5), ('4','5',0.50)])
    G.add_weighted_edges_from([('5','t',0.75), ('5','6',0.25), ('5','y',0.5)])
    G.add_weighted_edges_from([('6','t',0.75), ('6','y',0.75), ('6','7',0.25)])
    G.add_weighted_edges_from([('7','u',0.5), ('7','y',0.75), ('7','8',0.25)])
    G.add_weighted_edges_from([('8','i',0.5), ('8','u',0.75), ('8','9',0.25)])
    G.add_weighted_edges_from([('9','i',0.5), ('9','o',0.75), ('9','0',0.25)])
    G.add_weighted_edges_from([('0','-',0.5), ('0','o',0.75), ('0','p',0.5)])
    G.add_weighted_edges_from([('q','a',0.5), ('q','w',0.75), ('q','1',0.5), ('q','s',0.1)])
    G.add_weighted_edges_from([('w','a',0.5), ('w','e',0.75), ('w','s',0.25), ('w', 'd', 0.1)])
    G.add_weighted_edges_from([('e','d',0.5), ('e','r',0.75), ('e','f',0.10), ('e','t', 0.1)])
    G.add_weighted_edges_from([('r','f',0.5), ('r','t',0.75), ('r','g',0.10), ('r','d', 0.25)])
    G.add_weighted_edges_from([('t','g',0.5), ('t','y',0.75), ('t','f',0.10), ('t','h', 0.1)])
    G.add_weighted_edges_from([('y','h',0.5), ('y','u',0.75), ('y','j',0.10), ('y','g', 0.1)])
    G.add_weighted_edges_from([('u','j',0.5), ('u','i',0.75), ('u','h',0.10), ('u','k', 0.1)])
    G.add_weighted_edges_from([('i','k',0.5), ('i','o',0.75), ('i','j',0.10), ('i','l', 0.1)])
    G.add_weighted_edges_from([('o','l',0.5), ('o','p',0.75), ('o','k',0.10), ('o',';', 0.1)])
    G.add_weighted_edges_from([('p',';',0.5), ('p','[',0.75), ('p','-',0.10), ('p','=', 0.05)])
    G.add_weighted_edges_from([('a','z',0.5), ('a','s',0.75), ('a','x',0.10), ('a','', 0.1)]) # should try "next letter capitalize" maybe by ctrl char.
    G.add_weighted_edges_from([('s','x',0.5), ('s','d',0.75), ('s','z',0.5), ('s','c', 0.1)])
    G.add_weighted_edges_from([('d','x',0.5), ('d','f',0.75), ('d','c',0.50), ('d','v', 0.1)])
    G.add_weighted_edges_from([('f','v',0.5), ('f','g',0.75), ('f','b',0.10), ('f','c', 0.5)])
    G.add_weighted_edges_from([('g','b',0.5), ('g','h',0.75), ('g','v',0.5), ('g','b', 0.5)])
    G.add_weighted_edges_from([('h','b',0.5), ('h','j',0.75), ('h','n',0.5), ('h','m', 0.1)])
    G.add_weighted_edges_from([('j','n',0.5), ('j','k',0.75), ('j','m',0.5), ('j',',', 0.1)])
    G.add_weighted_edges_from([('k','m',0.5), ('k','l',0.75), ('k',',',0.5), ('k','.', 0.1)])
    G.add_weighted_edges_from([('l',',',0.5), ('l',';',0.75), ('l','.',0.5), ('l','/', 0.1)])
    G.add_weighted_edges_from([(';','\'',0.5), (';','/',0.75), (';','.',0.50), (';','', 0.1)])
    G.add_weighted_edges_from([('z',' ',0.1), ('z','x',0.75), ('z','',0.10)])
    G.add_weighted_edges_from([('x','c',0.5), ('x',' ',0.25)])
    G.add_weighted_edges_from([('v','b',0.5), ('v',' ',0.25)])
    G.add_weighted_edges_from([('b','n',0.5), ('b',' ',0.75)])
    G.add_weighted_edges_from([('n','m',0.5), ('n',' ',0.75)])
    G.add_weighted_edges_from([('m',',',0.5), ('m',' ',0.50)])
    G.add_weighted_edges_from([(',','.',0.5), (',',',,',0.25)])
    G.add_weighted_edges_from([('.','/',0.5), ('.',' ',0.75), ('.','..',0.10)])
    
    character = character.lower()
    '''Switch some character with another randomly'''
    #replacement = ['', '.']
    replacement = []
    keyweights = []
    # print(G[character])
    for neighbor in G[character]:
        # print(G[character][neighbor])
        replacement.append(neighbor)
        keyweights.append(G[character][neighbor]['weight'])
    if not (keyweights and replacement):
        replacement = ['', '.']
        keyweights = [0.5, 0.5]
    
    newkey = random.choices(
     population=replacement,
     weights=keyweights,
     k=1
    )
    newkey = newkey[0]
    # print(newkey)
    yield newkey
    # TODO: should streamline this
    # Consider using a hashmap;
    # { chr: replacements }
    # Then you could do hashmap[character] instead of this.

# have bot occasionally say "i am disabled"
# rand 3600 to 172800 : between 1 hour and 2 days

async def my_background_task():
    '''Beautifully named function.'''
    global runonce
    await bot.wait_until_ready()
    channel = discord.Object(id=int(parser.get('discord', 'channel_id')))
    # channel = last_conversation_channel
    while not bot.is_closed and runonce > 0:
        cur_bg_seconds = random.randint(min_bg_seconds, max_bg_seconds)
        print('disability awareness')
        await bot.send_message(channel, "I am disabled")
        await asyncio.sleep(cur_bg_seconds) # task runs every rand seconds

    runonce = 1

    # do another one of those for server.time_since_last_message or something so it can say 'hey'

@bot.event
async def on_message(message):
    '''Every time it reads a message.'''
    if message.author == bot.user:
        return
    if not message.content:
        return
    # keywords should be drawn from a file.
    keywords = [
        "adcat",
        "penis",
        "anime",
        "disabled",
        "brain",
        "help",
        "slime",
        "fursuit",
        "wheelchair",
        "wife",
        "adbot"
    ]
    loved_words = parser.get('general', 'loved_words').split(',')
    last_conversation_channel = message.channel
    # next thing to do would be to set easier targets by context,
    # e.g. run target choice from words or check all words
    # here, and say make it 1/100 for "slime" 1/30 for "adcat",
    # 1/5 for "penis" (not rly exactly that)
    rnd_result = random.randint(1, int(parser.get('general', 'response_range')))
    # default: must hit 2057 or greater
    to_hit = int(parser.get('general', 'def_response_target'))
    multiplier = (float(1.0))
    love_check = 0
    if not message.content.startswith('8=D'):
        for i in keywords:
            if i.lower() in message.content.lower():
                to_hit = int(parser.get('general', 'adj_response_target'))
        for i in loved_words:
            if i.lower() in message.content.lower():
                love_check = love_check + 1
                to_hit = int(parser.get('general', 'love_response_target'))
    #if botname in message.content.lower():
    my_regex = r"\b" + re.escape(botname) + r"\b"
    if re.search(my_regex, message.content.lower()) :
        to_hit = int(parser.get('general', 'mention_response_target'))
    do_post_image = 0
    if love_check > 3:
        love_check = 3
    love_ratio = 5
    love_ratio = int(parser.get('general', 'love_ratio'))
    do_post_image = 1 if (random.randint(1, love_ratio) <= love_check) else 0

    # I should be using command_prefix instead of 8=D here but I'll fix it l8r
    # i should also be printing only if not starts with command prefix but whatever
    hellchannel = discord.Object(id=int(521848932280827925))
    if int(message.channel.id) == 521848932280827925:
        rnd_result = 2069
    print("markov response in server %s: %s, target is %s" % (message.channel.id, rnd_result, to_hit) )
    if (not message.content.startswith('8=D')) and rnd_result > to_hit and not do_post_image:
        mcontent = message.content
        # get rid of words that are less than 4 characters: (this somehow isnt working)
        re.sub(r'\b\w{1,3}\b', '', mcontent) # still not working
        words = mcontent.split()


        # should probably test how long the content string is.  it may have multiple good targets "bug orb" that are equally valid.
        # perhaps it should equally hone in on one word or attempt to combine all of it.
        # if we attempt to combine all of it, we should only include or prefer messages that also have other words in them; e.g.:
        # original message: i'm bug orb (!!! bad example, we don't check for any of those!)
        # anyway, next: i'll fuck myself apart today
        # targets: fuck, myself, apart, today
        # return everything from the chat within chat limit, as long as it contains two of those, or preferring two of those. the preference should go
        # up if the sentence is longer; we'd have a better chance getting 2 of 17 possible to match than 2 of 3 possible to match, though that looks odd.
        # since we'd have a worse pool trying to find things that have, say, myself and today, we'd weight it such that our preference to find both isn't
        # likely going to exclude the message.  that is, break myself apart would have a 100% chance of getting in, and break myself would probably have 80+.
        target = random.choice(words)
        
        # next we're going to want to ...
        logs = bot.logs_from(message.channel, int(parser.get('general', 'chatdepth'))  )
        
        
        
        comment_dec_24_nltk = '''
        chatlog_v = []
        async for item1 in logs:
                if (not item1.author.id == bot.user.id) and (not item1.author.bot):
                    chatlog_v.append(item1.content)
        #chatlog_v = [msg.context for msg.context in logs] 
        chat_text = nltk.Text(chatword.lower() for chatword in nltk.corpus.brown.words() ) 
        #chat_text = nltk.Text(chatword.lower() for chatword in chatlog_v)
        similar_words = []
        similar_words = ' '.split(  chat_text.similar( target.lower() ) )
        similar_words.append(target.lower())
        print(similar_words)
        '''
        #This will fail sometimes
        # next we're going to want to go another degree of a graph if we don't get a big enough corpus.  that is, if the target word yields
        # a small list to supply the text modeler, what we should do is the following:
        # 1) try another word in the message content and go from there
        # 2) pick any repeated word that shows up or any subject-like (not an article) word you see in the small corpus list, then
        # build a corpus with that, then slam them together
        # 3) get every word in the message content and make the corpus out of all of those
        cone = ''
        async for item in logs:
                if (not item.author.id == bot.user.id) and (not item.author.bot):
                    context_text = mcontent + ' ' + item.content
                    short_text = nltk.Text(word_tokenize(context_text))
                    similar_words = []
                    similar_words = ' '.split( short_text.similar(target) )
                    similar_words.append(target.lower() )
                    #if any(tword in item.content.lower() for tword in similar_words) or target.lower() in item.content.lower():
                    if any(sim.lower() in item.content.lower() for sim in similar_words) or target.lower() in item.content.lower():
                        cone = cone +random.choice(['\n', ' '])+ item.content
        # print(cone)
        
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
            # this is what happens if we don't get a valid message.  Let's try something else.
            lines = [line.strip('\n') for line in open('master-lyrics.txt')]
            lyric = random.choice(lines)
            if not lyric:
                lyric = 'nice'
            print("lyric: %s" % lyric)
            # now we have to make it type like adcat
            inds = [i for i,_ in enumerate(lyric)]
            brainfog = random.randint(0, (len(str(lyric)) - 1) // 4)
            sam = random.sample(inds, brainfog)
            lst = [i for _,i in enumerate(lyric)]
            print(inds)
            for ind in sam:
                #lst[ind] = random.choice(ascii_letters)
                lst[ind] = ''.join(nearby(str(lst[ind])))
			# nothing with length less than 3 anyway
            for i in range(2,len(lst)-1): 
                if random.randint(1,10) > 9:
                    lst[i], lst[i+1] = lst[i+1], lst[i]
            lyrics_out = "nice"
            #lst = list(lst)
            print(lst)
            lst = [x for x in lst if x]
            if random.randint(1,10) > 5: 
                lyrics_out = (''.join(lst))
                lyrics_out = lyrics_out.lower()
                # lyrics_out = (''.join(lst)).lower()
            if random.randint(1,10) <= 5:
                lyrics_out = (''.join(lst))
                lyrics_out = lyrics_out.upper()        
                #lyrics_out = (''.join(lst)).upper()
            await bot.send_message(message.channel, "%s" % lyrics_out)		
    elif (not message.content.startswith('8=D')) and rnd_result > to_hit and do_post_image:
        print('natsuki hop')
        await bot.send_file(message.channel, 'hop.gif')
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

def is_in_server_list(server_list):
    def predicate(ctx):
        return ctx.message.server.id in server_list
    return commands.check(predicate)

@bot.command(pass_context = True)
@commands.has_any_role("Purple", "The Boss of this Gym", "Green", "Loli's Group")
@is_in_server_list(whitelist)
async def tweet(ctx, *, garbage:str = "DICKS EVERYWHERE"):
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
            await bot.say("HARBL/111-420 LAST POST: \U000022B7 https://twitter.com/8frontflips/status/%s" % cum)
        elif int(cum) > int(oldid) and failed and failstring is not None:
            await bot.say("HARBL/69-666 **MESSAGE FAILED** SHOOT THE MOON: \U000022B7 https://twitter.com/8frontflips/status/%s" % cum)
        elif int(cum) <= int(oldid) and failed and failstring is not None:
            await bot.say("HARBL/69-400-V **MESSAGE FAILED** TRY POSTING AGAIN IDIOT (error: %s)" % failstring)
        else:
            await bot.say("HARBL/69-303 **MESSAGE FAILED** (UNKNOWN) LAST POST: \U000022B7 https://twitter.com/8frontflips/status/%s" % cum)


bot.loop.create_task(my_background_task())
bot.add_cog(Games(bot))
bot.run(parser.get('discord', 'token'))

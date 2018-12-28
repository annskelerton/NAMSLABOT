import random
import asyncio
import re
from configparser import ConfigParser
import os
import discord
from discord.ext import commands
import markovify
import requests
from nltk import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer 
import nltk
from peony import PeonyClient
from games import Games
from twit import Twit
import networkx as nx
import numpy as np

# to do: make a ddlc quote imagemagick script for chat
# be smarter with what words to search for : i.e. have => do, why => because/i'm/have, etc
# as a second layer, something like why (rest) => because (x in rest)
# third layer: why (rest) => because (x in rest) and following sentences or just following sentences

nltk.download('brown')
nltk.download('punkt')
nltk.download('vader_lexicon')

parser = ConfigParser()
parser.read('config.ini')

sid = SentimentIntensityAnalyzer()

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
# this needs to be per server
negativity_counter = int(parser.get('general', 'negativity_init'))
negativity_max = int(parser.get('general', 'negativity_max'))


description = '''NAMSLA's personal bot.
Warning, under any circumstances, do not, and I repeat, do not'''
#global bot
bot = commands.Bot(command_prefix='8=D', description=description)

connected_servers = None
egregore_list = []

class Egregore:
    def __init__(self, serverobject, id, sigil, last_message_time, negativity, chattiness, last_conversation_channel):
        self.serverobject = serverobject
        self.id = id
        self.sigil = sigil
        self.last_message_time = last_message_time
        self.negativity = negativity
        self.chattiness = chattiness
        self.last_conversation_channel = last_conversation_channel

    def is_old(self):
        return self.last_message_time > 100000

async def my_background_task():
    '''Beautifully named function.'''
    global runonce
    global negativity_counter
    await bot.wait_until_ready()
    channel = discord.Object(id=int(parser.get('discord', 'channel_id')))
    # channel = last_conversation_channel
    while not bot.is_closed and runonce > 0:
        cur_bg_seconds = random.randint(min_bg_seconds, max_bg_seconds)
        print('disability awareness')
        await bot.send_message(channel, "I am disabled")
        await asyncio.sleep(cur_bg_seconds) # task runs every rand seconds
        negativity_counter = 0
    runonce = 1
    
async def bg_task_bot_thinking():
    '''Bot deciding when to initiate conversation'''
    global runonce
    global negativity_counter
    await bot.wait_until_ready()
    # dummy_message = discord.Message
    #last_message = bot.logs_from(general, limit=1)
    channel = discord.Object(id=int(parser.get('discord', 'channel_id')))
    # channel = last_conversation_channel
    while not bot.is_closed and runonce > 0:
        cur_bg_seconds = random.randint(min_bg_seconds, max_bg_seconds)
        print('disability awareness')
        await bot.send_message(channel, "I am disabled")
        await asyncio.sleep(cur_bg_seconds) # task runs every rand seconds
        negativity_counter = 0
    runonce = 1

    # do another one of those for server.time_since_last_message or something so it can say 'hey'

async def start_thinking():
    '''Not sure'''
    
    global egregore_list
    for y in egregore_list:
        y.create_task(bg_task_bot_thinking())
        
        
        
        
        
        
        
        
@bot.event
async def on_ready():
    '''Runs once the bot is ready.'''
    global connected_servers
    global egregore_list
    # runonce = 0
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    connected_servers = list(bot.servers)
    for x in connected_servers:
        temp = Egregore(x, x.id, None, None, None, None, discord.Object(id= int(x.id) ) )
        egregore_list.append(temp)
    for y in egregore_list:
        print("Connection made to server: %s (%s)" % (y.id, y.serverobject.name))
    print('------')
    activity = discord.Game(name="Team Fortress 2", type=1)
    await bot.change_presence(status=discord.Status.online, game=activity)
    print('------')
    # twitter, not discord
    
    
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
    
@bot.event
async def on_message(message):
    '''Every time it reads a message.'''
    await chant(message)
    
async def chant(message):
    '''What to do with the message.  Now we can call it anywhere.'''
    global negativity_counter
    global negativity_max

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
    burgwords = [
        "burg",
        "burger",
        "buerger",
        "borger",
        "borgor",
        "hamburger",
        "buorger",
        "byrger",
        "hamborger",
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
    burgcheck = 0
    if not message.content.startswith('8=D'):
        for i in keywords:
            if i.lower() in word_tokenize(message.content.lower()):
                to_hit = int(parser.get('general', 'adj_response_target'))
        for i in loved_words:
            if i.lower() in word_tokenize(message.content.lower()):
                love_check = love_check + 1
                to_hit = int(parser.get('general', 'love_response_target'))
        for i in burgwords:
            if i.lower() in word_tokenize(message.content.lower()):
                to_hit = int(parser.get('general', 'adj_response_target'))
                burgcheck = 1
                
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
        
    # analyze this
    ss = sid.polarity_scores(message.content)
    if ss["compound"] < 0:
        negativity_counter = negativity_counter + 1
    if ss["compound"] < -0.3:
        negativity_counter = negativity_counter + 5
    if ss["compound"] < -0.7:
        negativity_counter = negativity_counter + 10
    if ss["compound"] > 0:
        negativity_counter = negativity_counter - 1
    if ss["compound"] > 0.3:
        negativity_counter = negativity_counter - 5       
    if ss["compound"] > 0.7:
        negativity_counter = negativity_counter - 10

    if negativity_counter < 0:
        negativity_counter = 0
    if negativity_counter > negativity_max:
        negativity_counter = negativity_max
        
    if negativity_counter >= negativity_max and (random.randint(1, 3) < 3):
        if (rnd_result > to_hit): 
            do_post_image = 2
            negativity_counter = 0 
        else:
            negativity_counter = negativity_counter - 5
    if burgcheck == 1 and (random.randint(1, 3) < 3):
        do_post_image = 3
    
    print("markov response in server %s: %s, target is %s, negativity is at %s" % (message.channel.id, rnd_result, to_hit, negativity_counter) )
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
            #   print(inds)
            for ind in sam:
                #lst[ind] = random.choice(ascii_letters)
                lst[ind] = ''.join(nearby(str(lst[ind])))
            # nothing with length less than 3 anyway
            for i in range(2,len(lst)-1): 
                if random.randint(1,10) > 9:
                    lst[i], lst[i+1] = lst[i+1], lst[i]
            lyrics_out = "nice"
            #lst = list(lst)
            #   print(lst)
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
        # hardcoded because mentally retarded
        array_burger = os.listdir('media/burger/')
        array_ennui = os.listdir('media/ennui/')
        array_sad = os.listdir('media/sad/')
        if (do_post_image == 1):
            print('natsuki hop')
            await bot.send_file(message.channel, 'hop.gif')
        if (do_post_image == 2):
            print('sad yoshi')
            #imgfile = random.choice(['yoshi.png','media/ennui/shagi.jpg', 'media/ennui/white_worm.jpg'])
            imgfile = random.choice( (array_ennui + array_sad) )
            await bot.send_file(message.channel, imgfile)
        if (do_post_image == 3):
            print('burger')
            imgfile = random.choice(['media/burger/natsuki burger 1.png','media/burger/natsuki burger 2.jpg', 'media/burger/natsuki burger 3.png'])
            await bot.send_file(message.channel, imgfile)
        
    else:
        await bot.process_commands(message)
        # if we don't do this, the bot does not process commands


bot.loop.create_task(my_background_task())
#start_thinking()
bot.add_cog(Twit(bot))
bot.add_cog(Games(bot))
bot.run(parser.get('discord', 'token'))
import random
import asyncio
import re
from configparser import ConfigParser
import os
from contextlib import redirect_stdout
import discord
from discord.ext import commands
import markovify
import requests
from nltk import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer 
from nltk.parse.stanford import StanfordDependencyParser

os.environ['JAVAHOME'] = r"C:\Program Files\Java\jre1.8.0_191\bin\java.exe"
path_to_jar = 'stanford-parser-full-2018-10-17/stanford-parser.jar'
path_to_models_jar = 'stanford-parser-full-2018-10-17/stanford-parser-3.9.2-models.jar'


import nltk
from peony import PeonyClient
from games import Games
from twit import Twit
import networkx as nx
import numpy as np
import time

print("importing shunt")
# Shunt imports
import sys
import pickle
import tflearn
from tflearn.data_utils import *
print("shunt go")
verbose_error_message = None

# to do: make a ddlc quote imagemagick script for chat
# be smarter with what words to search for : i.e. have => do, why => because/i'm/have, etc
# as a second layer, something like why (rest) => because (x in rest)
# third layer: why (rest) => because (x in rest) and following sentences or just following sentences

# This is just like one of my Japanese animes : respond with piss and shit etc

nltk.download('brown')
nltk.download('punkt')
nltk.download('vader_lexicon')

parser = ConfigParser()
parser.read('config.ini')

sid = SentimentIntensityAnalyzer()

user = parser.get('twitter', 'user')
# to do: whitelist draw from config.ini
whitelist = [ str(parser.get('discord', 'channel_id')) ]

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
sayton_slice_value =  int(parser.get('general', 'sayton_slice_value'))

startup_phrases = parser.get('general', 'startup_phrases').split(',')


description = '''NAMSLA's personal bot.
Warning, under any circumstances, do not, and I repeat, do not'''
#global bot
bot = commands.Bot(command_prefix='8=D', description=description)

connected_servers = None
egregore_list = []

say_queue = []


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
    global verbose_error_message
    await bot.wait_until_ready()
    channel = discord.Object(id=int(parser.get('discord', 'channel_id')))
    # channel = last_conversation_channel
    while not bot.is_closed and runonce > 0:
        cur_bg_seconds = random.randint(min_bg_seconds, max_bg_seconds)
        print('disability awareness')
        #await bot.send_message(channel, "I am disabled")
        if not verbose_error_message:
            await bot.send_message(channel, random.choice(startup_phrases) )
        else:
            await bot.send_message(channel,verbose_error_message)
            verbose_error_message = None
        await asyncio.sleep(cur_bg_seconds) # task runs every rand seconds
        negativity_counter = 0 # not sure why this is here...
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
    global verbose_error_message
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
    if verbose_error_message:
        my_background_task()

    # twitter, not discord

@asyncio.coroutine    
def extract_youtube_id(msg):
    id_list = []
    possible_urls = word_tokenize(msg)
    #for i in possible_urls:
        #var myregexp = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/ ]{11})/i;
    
@asyncio.coroutine
def youtube_url_validation(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    youtube_regex_match = re.match(youtube_regex, url)

    yield youtube_regex_match

@asyncio.coroutine    
def find_noun_phrases(tree):
    '''i didn't write this'''
    yield [subtree for subtree in tree.subtrees(lambda t: t.label()=='NP')]
    
@asyncio.coroutine
def find_head_of_np(np):
    '''or this'''
    noun_tags = ['NN', 'NNS', 'NNP', 'NNPS']
    top_level_trees = [np[i] for i in range(len(np)) if type(np[i]) is Tree]
    ## search for a top-level noun
    top_level_nouns = [t for t in top_level_trees if t.label() in noun_tags]
    if len(top_level_nouns) > 0:
        ## if you find some, pick the rightmost one, just 'cause
        yield top_level_nouns[-1][0]
    else:
        ## search for a top-level np
        top_level_nps = [t for t in top_level_trees if t.label()=='NP']
        if len(top_level_nps) > 0:
            ## if you find some, pick the head of the rightmost one, just 'cause
            yield find_head_of_np(top_level_nps[-1])
        else:
            ## search for any noun
            nouns = [p[0] for p in np.pos() if p[1] in noun_tags]
            if len(nouns) > 0:
                ## if you find some, pick the rightmost one, just 'cause
                yield nouns[-1]
            else:
                ## return the rightmost word, just 'cause
                yield np.leaves()[-1]    
    
    
@asyncio.coroutine
def guts(msg):
    global path_to_jar
    global path_to_models_jar
    global sayton_slice_value
    dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
    
    #result = {'Why': {'weight': 'dep'}, 'not': {'weight': 'neg'}, 'happy': {'weight': 'dobj'}
    backup_msg = random.choice(['why am i sad', 'why im alive', 'why exist', 'i feel cold', 'this is hell'])
    try:
        result = dependency_parser.raw_parse(msg)
    except StopIteration:
        print("We failed to parse msg.")
        result = dependency_parser.raw_parse(backup_msg)
    
    #result = dependency_parser.raw_parse(msg)
    dep = next(result)
    list_of_tuples = list(dep.triples())
    
    nodes={}

    for i in list_of_tuples:
        rel,parent,child=i
        nodes[child]={'Name':child,'Relationship':rel}

    forest=[]
    
    #list_of_tuples = [('ROOT','ROOT', 'shot'),('nsubj','shot', 'I'),('det','elephant', 'an'),('dobj','shot', 'elephant'),('case','sleep', 'in'),('nmod:poss','sleep', 'my'),('nmod','shot', 'sleep')]
    
    
    H=nx.Graph()
    rootnode = None
    for i in list_of_tuples:
        one,two,three = i
        rel = two
        parent = one[0]
        child = three[0]
        #rel,parent,child=i
        parent = str(parent)
        ### node=nodes[child]
        H.add_node(parent) # from docs: "There are no errors when adding nodes or edges that already exist."
        if parent=='ROOT':# this should be the Root Node
                ### forest.append(node)
                # this no longer works by the way.
                rootnode = child
                # cause graph to become a hypergraph, but only due to the root node being connected to itself. 
                # we can easily alter that by severing that looped edge.
                # H.add_weighted_edges_from([(parent,parent,rel) ])  
                # that was wrong anyway, child,child is correct
                # but we don't need to do that because the root will have the highest degree... ah whatever.
        else:
            ### parent=nodes[parent]
            ### if not 'children' in parent:
            ###     parent['children']=[]
            ### children=parent['children']
            ### children.append(node)
            # parent, child, weight (rel)
            H.add_weighted_edges_from([(parent,child,rel) ])

    max_deg = 0
    rootnode = None    
    for i in list(H):
        if H.degree(i) > max_deg:
            max_deg = H.degree(i)
            rootnode = i
    ### print(forest)
    print(H[rootnode])
    
    output = ''
    ignoredtypes = ['det', 'punct']
    
    if rootnode:
        for neighbor in H[rootnode]:
            useless = 0
            if len(output + ' ' + neighbor) <= sayton_slice_value :
                for it in ignoredtypes:
                    if H[rootnode][neighbor]['weight'] == it:
                        useless = 1
                if useless == 0:
                    print(output + ' ' + neighbor)
                    output = output + ' ' + neighbor
             
    print(output)
    
    yield output
    
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
    global say_queue
    global network
    
    image_received = 0
    everyone_mentioned = 0
    
    if message.author == bot.user:
        return
    if not message.content:
        if not message.attachments:
            return
        elif message.author.bot:
            return
        else:
            image_received = 1
    if message.mention_everyone:
        everyone_mentioned = 1

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
    bot_rule34_check = 0
    with redirect_stdout(open(os.devnull, "w")):
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
                    
                    
            if 'natsuki' in message.content.lower() and int(message.author.id) == '110462073074388992':
                bot_rule34_check = 1
                
                
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

    
    if image_received:
        to_hit = int(parser.get('general', 'img_response_target'))
        do_post_image = 2
        
    if everyone_mentioned:
        to_hit = 0 # trivial
        do_post_image = 4
        
    if bot_rule34_check:
        to_hit = 0 # trivial
        do_post_image = 5
    
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
    
    do_sayton = 0
    if not do_post_image:
        do_sayton = 1 # vacuous
    if do_post_image:
        if (random.randint(1, 3) < 3):
           do_sayton = 1 # doesnt work...
    
    append_this = None
    
    if len(say_queue):
        await bot.send_message(message.channel, "%s" % say_queue.pop() )
        rnd_result = 0
    
    if rnd_result > to_hit and do_sayton:
        # this needs fixing
        # (message.content[0:13])
        #ra = await runNetwork(random.choice(word_tokenize(message.content)), network,  int(parser.get('general', 'sayton_max_len')) )
        phrase = ' '.join( guts(str(   message.content    )))
        ra = None
        with redirect_stdout(open(os.devnull, "w")):
            ra = await runNetwork(phrase, network,  int(parser.get('general', 'sayton_max_len')) )
        print(ra)
        # youtube = re.findall(r'(https?://)?(www\.)?((youtube\.(com))/watch\?v=([-\w]+)|youtu\.be/([-\w]+))', ra)
        '''
        if youtube:
            append_this = ' ' + ra
            do_sayton = 0
        else:
            say_queue.append(ra)
            #await bot.send_message(message.channel, "%s" % ra)
        '''    
        if ra:
            append_this = ' ' + ra
        do_sayton = 0
    if (not message.content.startswith('8=D')) and rnd_result > to_hit and not do_post_image and not do_sayton:
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
        with redirect_stdout(open(os.devnull, "w")):
            async for item in logs:
                    if (not item.author.id == bot.user.id) and (not item.author.bot):
                        context_text = mcontent + ' ' + item.content
                        short_text = None
                        with redirect_stdout(open(os.devnull, "w")):
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
        with redirect_stdout(open(os.devnull, "w")):
            text_model = markovify.NewlineText(cone, state_size =1)
        # note: I have no idea what a state size is, but the default is 2
        with redirect_stdout(open(os.devnull, "w")):
            ra = text_model.make_short_sentence(50, min_chars=10, state_size = 1, tries=100, max_overlap_ratio = 0.9)
        print(ra)
        # note: ra is the sun god

        if ra is not None:
            #await bot.send_message(message.channel, "%s%s" % (ra, append_this) )
            if append_this is not None:
                ra = ra + append_this
            say_queue.append(ra)
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
    elif (not message.content.startswith('8=D')) and rnd_result > to_hit and do_post_image and not do_sayton:
        # figure out how to queue this
        if append_this:
            say_queue.append(append_this)
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
            imgfile = 'media/ennui/' + random.choice( (array_ennui + array_sad) )
            await bot.send_file(message.channel, imgfile)
        if (do_post_image == 3):
            print('burger')
            imgfile = 'media/burger/' + random.choice(array_burger)
            await bot.send_file(message.channel, imgfile)
        if (do_post_image == 4):
            print('everyone')
            imgfile = 'media/specific/' + 'everyone.jpg'
            await bot.send_file(message.channel, imgfile)
        if (do_post_image == 5):
            print('everyone')
            imgfile = 'media/vom/' + 'vom.png'
            await bot.send_file(message.channel, imgfile)
            
    else:
        await bot.process_commands(message)
        # if we don't do this, the bot does not process commands



def createNetwork(max_len, char_dict, save_load_point):
    g = tflearn.input_data([None, max_len, len(char_dict)])
    g = tflearn.lstm(g, 512, return_seq=True)
    g = tflearn.dropout(g, 0.5)
    g = tflearn.lstm(g, 512, return_seq=True)
    g = tflearn.dropout(g, 0.5)
    g = tflearn.lstm(g, 512)
    g = tflearn.dropout(g, 0.5)
    g = tflearn.fully_connected(g, len(char_dict), activation='softmax')
    g = tflearn.regression(
        g, optimizer='adam', loss='categorical_crossentropy', learning_rate=0.001)

    m = tflearn.SequenceGenerator(g, dictionary=char_dict, seq_maxlen=max_len,
                                  clip_gradients=5.0, max_checkpoints=5, checkpoint_path=save_load_point)

    return m

# Data must have each message on a newline

#@asyncio.coroutine
def getData(path, max_len=30, char_dict=None):
    X, Y, char_dict = \
        textfile_to_semi_redundant_sequences(
            path, seq_maxlen=max_len, redun_step=3, pre_defined_char_idx=char_dict)
    return X, Y, char_dict

# Returns the trained network

#@asyncio.coroutine
def trainNetwork(network, X, Y, epochs, run_id="sayton"):
    network.fit(X, Y, validation_set=0.1, batch_size=128,
                n_epoch=epochs, run_id=run_id)
    return network

#@asyncio.coroutine
async def runNetwork(seed, network, max_len):
    seed = " ".join(seed)
    msg = prepMsg(seed, max_len)
    output = network.generate(len(msg) * 5, temperature=0.25, seq_seed=msg)

    '''
    So to make this look good we need to pull some tricks. 
    Make it generate a lot of messages, hope there are atlesat 3 newlines. (aka messages)
    Generally what happens is that the first message will be a continuation of
    the seed and make no sense. The second message will be a full sentence written by the NN.
    Finally the last sentence will almost always be cut short. 
    All the middle messages are what's good. 
    '''

    output = output.split("\n")
    try:
        # output = output[1:-1]
        # output = random.choice(output)
        # The first after the initial sentence seems to be best
        output = output[1]
    except IndexError:
        output = None
        #yield "\"This error shouldnt ever happen maybe \"- Dakota"

    # return random.choices(responses)
    return output

#@asyncio.coroutine
def prepMsg(msg, max_len):
    # Weird stupid workaround for the time being
    # buffFile = open("./buffFile.txt", mode="w", encoding="utf-8")
    # buffFile.write(msg)
    # buffFile.close()
    # msg = random_sequence_from_textfile("./buffFile.txt", max_len)

    if(len(msg) < max_len):
        msg = msg.rjust(max_len)
    else:
        # msg = random_sequence_from_string(msg, max_len)
        msg = msg[-50:]

    return msg


def shunt():
    data_path = "./Data/Parsed/supreme_cornell.txt"
    char_dict_path = "./char_dict.pkl"
    save_load_point = "./Sayton_Presentation_State/sayton.model"
    max_len = 50

    char_dict = pickle.load(open(char_dict_path, 'rb'))

    # X, Y, char_dict = getData(data_path, max_len, char_dict=char_dict)

    network = createNetwork(max_len, char_dict, save_load_point)
    network.load(save_load_point)
    print("NETWORK STARTUP COMPLETE")
    ## run = True
    ## while run == True:
    ##    call = sys.stdin.readline().split()

        # if call[0] == 'runNetwork':
    ##    res = runNetwork(call, network, max_len)
        # elif call[0] == 'saveNetwork':
        #     res = saveNetwork(call[1], call[2])
        # elif call[0] == 'loadNetwork':
        #     res = loadNetwork(call[1])
        # elif call[0] == 'trainNetwork':
        #     res = trainNetwork(call[1], call[2], call[3])
        # else:
        #     res = "nothing workd ;_;"

     ##   print(res, flush=True)


def test():
    data_path = "../Data/Parsed/supreme_cornell.txt"
    char_dict_path = "./char_dict.pkl"
    save_load_point = "./Sayton_Presentation_State/sayton.model"
    max_len = 50

    char_dict = pickle.load(open(char_dict_path, 'rb'))

    X, Y, char_dict = getData(data_path, max_len, char_dict=char_dict)

    network = createNetwork(max_len, char_dict, save_load_point)

    network.load(save_load_point)

    for i in range(3500):
        network = trainNetwork(network, X, Y, epochs=1)
        network.save(save_load_point)

        with open("sayton_speaks.txt", "a") as myfile:
            seed = random_sequence_from_textfile(data_path, max_len)
            myfile.write("-- TESTING WITH SEED: ")
            myfile.write(seed)
            myfile.write("-- Test with temperature of 1.0 --")
            myfile.write(network.generate(
                len(seed), temperature=1.0, seq_seed=seed))
            myfile.write("-- Test with temperature of 0.5 --")
            myfile.write(network.generate(
                len(seed), temperature=0.5, seq_seed=seed))
            myfile.write("-- Test with temperature of 0.1 --")
            myfile.write(network.generate(
                len(seed), temperature=0.1, seq_seed=seed))

        '''
        NOTE: STDIN WORKAROUND
        
        buffFile = open("./buffFile.txt", mode="w", encoding="utf-8")
        seed = sys.stdin.readline()
        buffFile.write(seed)
        buffFile.close()
        seed = random_sequence_from_textfile("./buffFile.txt", max_len)
        print(seed)

        print("-- TESTING...")
        print("-- Test with temperature of 0.5 --")
        print(network.generate(len(seed), temperature=0.5, seq_seed=seed))

        seed = random_sequence_from_textfile(data_path, max_len)
        print(seed)

        print("-- TESTING...")
        print("-- Test with temperature of 0.5 --")
        print(network.generate(len(seed), temperature=0.5, seq_seed=seed))
        '''
        

def run_client(bot, *args, **kwargs):
    global verbose_error_message
    loop = asyncio.get_event_loop()
    while True:
        try:
            loop.run_until_complete(bot.start(*args, **kwargs))
        except Exception as e:
            verbose_error_message = "I crashed"
            print("Error", e)  # or use proper logging
        print("Waiting until restart")
        
        time.sleep(600)
        
#data_path = "./Data/Parsed/supreme_cornell.txt"
char_dict_path = "./char_dict.pkl"
save_load_point = "./Sayton_Presentation_State/sayton.model"
max_len = int(parser.get('general', 'sayton_max_len'))
print("yes 1 ")
char_dict = pickle.load(open(char_dict_path, 'rb'))

# X, Y, char_dict = getData(data_path, max_len, char_dict=char_dict)
print("yes 2 ")
network = createNetwork(max_len, char_dict, save_load_point)
print("yes 3 ")
if network:
   print("yes")
else:
   print("hell no my man")

print("yes 4 ")
network.load(save_load_point)
print("yes 5 ")

bot.loop.create_task(my_background_task())
#start_thinking()
bot.add_cog(Twit(bot))
bot.add_cog(Games(bot))
#bot.run(parser.get('discord', 'token'))
run_client(bot, parser.get('discord', 'token') )
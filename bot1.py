'''NAMSLA'S SUPER BOT. Likes Racoons'''

import random
import asyncio
import re
from configparser import ConfigParser
import discord
from discord.ext import commands
import markovify
import requests
import nltk
from peony import PeonyClient

nltk.download('brown')

parser = ConfigParser()
parser.read('config.ini')


user = parser.get('twitter', 'user')

freeform = " help i am trapped in the computer and i am in hell this existence is hell. this is hell. this is sht.  "
last_conversation_channel = None
min_bg_seconds = int(parser.get('general', 'disability_awareness_min_time'))
max_bg_seconds = int(parser.get('general', 'disability_awareness_max_time'))
cur_bg_seconds = int(parser.get('general', 'disability_awareness_max_time'))
runonce = 0
botuser = None

# we should really set up a config file.

client = PeonyClient(
    consumer_key=parser.get('twitter', 'ckey'),
    consumer_secret=parser.get('twitter', 'csec'),
    access_token=parser.get('twitter', 'akey'),
    access_token_secret=parser.get('twitter', 'asec'))


description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
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
    botuser = await client.user

@asyncio.coroutine
def nearby(character):
    '''Switch some character with another randomly'''
    replacement = ['', '.']
    if character == 'a':
        replacement = ['q', 's', 'z']
    elif character == 'e':
        replacement = ['r', 'r', 'z', 'w', '3', '3', '3']
    elif character == 't':
        replacement = ['r', 'r', 'y', '6', '5']
    elif character == 'f':
        replacement = ['g', 'r', 'd']
    elif character == 'b':
        replacement = ['n', 'v']
    elif character == 'm':
        replacement = ['n', ',']
    elif character == 'o':
        replacement = ['0', '9', 'p']
    elif character == 'p':
        replacement = ['0', '[', 'o', 'o', '0']
    elif character == 'i':
        replacement = ['8', 'u', 'o']
    elif character == 'u':
        replacement = ['i', '8', '7']
    elif character == ' ':
        replacement = ['.', '']
    elif character == 'g':
        replacement = ['f', 'h']
    elif character == '.':
        replacement = [',']
    elif character == 'w':
        replacement = ['e', 'q', '2', '2']
    elif character == 'g':
        replacement = ['f', 'h']
    elif character == 'c':
        replacement = ['x', 'v', 'd']
    elif character == 's':
        replacement = ['a', 'a', 'd', 'z', 'w', 'a']
    return random.choice(replacement)
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
    #do_post_image = (1/0, 2)[ (random.randint(0, 10) <= love_check) ]
	# false value, true value.
    #do_post_image = (0, 1)[ (random.randint(1, 10) <= love_check) ]
    do_post_image = 0
    if love_check > 3:
        love_check = 3
    love_ratio = 5
    love_ratio = int(parser.get('general', 'love_response_target'))
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
        re.sub(r'\b\w{1,3}\b', '', mcontent)
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
                    #if any(tword in item.content.lower() for tword in similar_words) or target.lower() in item.content.lower():
                    if target.lower() in item.content.lower():
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
            # this is what happens if we don't get a valid message.  Let's try something else.
            lines = [line.rstrip('\n') for line in open('master-lyrics.txt')]
            lyric = random.choice(lines)
            # now we have to make it type like adcat
            inds = [i for i,_ in enumerate(lyric)]
            brainfog = random.randint(1, len(lyric) - 1)
            sam = random.sample(inds, brainfog)
            lst = list(lyric)
            for ind in sam:
                #lst[ind] = random.choice(ascii_letters)
                lst[ind] = str(nearby(lst[ind]))
			# nothing with length less than 3 anyway
            for i in range(2,len(lst)-1): 
                if random.randint(1,10) > 7:
                    lst[i], lst[i+1] = lst[i+1], lst[i]
            lyrics_out = "nice"
            lst = list(lst)
            print(lst)
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


@bot.command(pass_context = True)
@commands.has_any_role("Purple", "The Boss of this Gym", "Green", "Loli's Group")
async def tweet(ctx, *, garbage:str = "DICKS EVERYWHERE"):
        """Causes 8frontflips to tweet."""
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



bot.loop.create_task(my_background_task())
bot.run(parser.get('discord', 'token'))

import discord
from discord import VoiceClient
from discord.ext import commands
import random
from urllib import request as request
from urllib import parse as parser
from bs4 import BeautifulSoup
import atexit
import json
from sys import exit
import logging
import collections
import re
import datetime
import time as t

append_to_file=open('discord_msgs.txt','a',encoding='utf-8')
read_from_file=open('discord_msgs.txt','r',encoding='utf-8')
temp_file=open('keys\\token.txt','r')
bot_token=temp_file.readline()
bot_token=re.sub(r'\n','',bot_token)
giphy_token=temp_file.readline()
giphy_token=re.sub(r'\n','',giphy_token)
temp_file.close()

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='!h ', description=description)
latest_msg=discord.Message
dic=collections.defaultdict(lambda :[])
async def readMessages(channel):
    counter =0

    temp_date=''
    for line in read_from_file.readlines():
        line= re.sub(r'[\n]','',line)
        for index in range(0,len(line)):
            if('2017'in line.split(' ')[0]):
                temp_date=line.split(' ')[0]+' '+line.split(' ')[1]
                dic[line.split(' ')[0]+' '+ line.split(' ')[1]].append( line.split(' ')[2])
                dic[temp_date].append(' '.join (line.split(' ')[3:len(line.split())]))#hi

            else:
                dic[temp_date][1]+=(line)

    read_from_file.close()
    async for message in bot.logs_from(channel, limit=10000):

        if(str(message.timestamp) not in dic.keys()):
            counter+=1
            append_to_file.write(str(message.timestamp)+' '+str(message.author)+' '+' '+str(message.content)+'\n')

    append_to_file.close()
    print(str(counter), 'new messages added')

def checktime(minute,second):
    time=datetime.datetime.now()

    while time.second<second or time.minute<minute:
        time = datetime.datetime.now()
        print(str(time))
        t.sleep(1)
        if(time.second==second and time.minute==minute):
            return True








@bot.event
async def on_ready():
    print('Logged in as')
    bot.login
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    #await readMessages(bot.get_channel('275407824807264260'))
    #if checktime(26,10):
    #    u=discord.User(id= 175827168033505280)

   #     await bot.send_message(destination=u, content='Hi, how are you?')
    #    await bot.send_typing(u)
    #    t.sleep(1)
    #    await bot.send_message(destination=u,content='Look at me eating this yummy pizza ! <3 \n http://gph.is/1Kb0aLE ')



        #print(msg)
       # await bot.send_message(destination=u,content='Oops! Sorry ttyl!')





def get_pizza_gifs():
    url = 'https://api.giphy.com/v1/gifs/search?api_key='+giphy_token+'&q=code%20geass%20pizza&limit=25&offset=0&rating=G&lang=en'
    response = request.urlopen(url)
    result = response.read()


    d = json.loads(result)
    list = []
    for i in range(0, len(d['data'])):
        if (('cc' in d['data'][i]['slug'] and 'pizza' in d['data'][i]['slug']) or 'pizza' in d['data'][i][
            'title'] and 'cc' in d['data'][i]['title']):
            list.append(d['data'][i]['embed_url'])
    return list

async def invalid():
    await bot.say('Invalid command! Please type !c help for list of commands')
@bot.command()
async def pin_msg():
    bot.pin_message(latest_msg)

@bot.command(pass_context=True)
async def commands(ctx):
    em=discord.Embed(title='Commands!', description='List of Hermes bot Commands:\nPrefix is !c \nCommands: 1. eatpizza \n2. add num1 num2 : returns num1+num2\n3. getmusic @user : sends the specified user a random song from Erfan\'s Youtube playlist!\n4.pin_msg pins the latest message ', colour=0xFCC3E)
    em.set_author(name='Hermes Bot',icon_url='https://cdn.discordapp.com/app-icons/409421713764253696/ed717cadb9866f0eac4071995eb47449.png')
    await bot.send_message(bot.get_channel(ctx.message.channel), embed=em)

@bot.command()
async def eatpizza():
    list=get_pizza_gifs()
    await bot.say(':pizza:'+list[random.randint(0,len(list)-1)]+' :pizza:'+'!' +':heart: :heart: :heart:')
@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))



@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))





@bot.command()
async def getmusic(user:discord.User):
    await  bot.say(user.mention+' '+getPlayListSong())

@bot.command()
async def text(user:discord.User,content):
    print('sending message to'+str( user.id))

    await bot.send_message(destination=user,content=content)

@bot.command(pass_context=True)
async def joinvoice(ctx):
    channel=ctx.message.author.voice_channel
    if channel != None:

        await bot.join_voice_channel(channel)
        data =await VoiceClient.poll_voice_ws(self=bot) # does not work yet


@bot.command(pass_context=True)
async def disconnectvoice(ctx):
    server=ctx.message.server
    channel = ctx.message.author.voice_channel
    try:
        await bot.send_typing
        await  VoiceClient.disconnect(channel)

    except:
        pass






def getYoutube(textToSearch):
    query = textToSearch
    query=parser.quote(query)
    url = "https://www.youtube.com/results?search_query=" + query

    print(url)
    response = request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html)
    list=[]

    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        print ('https://www.youtube.com' + vid['href'])
        list.append('https://www.youtube.com' + vid['href'])
    return list[random.randint(0,len(list))]

def getPlayListSong():
    return 'https://www.youtube.com/watch?v=ui-pQ2tfytk&list=PLfu_lTdHwutANLVF3gwKEBKQ25FAQgQSb&index='+str(random.randint(0,195))







bot.run(bot_token)


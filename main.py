import discord
from requests.auth import HTTPBasicAuth
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import app_commands
from discord.ui import Select, View, Modal, TextInput
import requests
import os, sys
from time import sleep
import csv
import asyncio
import datetime
from dotenv import load_dotenv
load_dotenv()
from gamecheckers import DotaCheck
from csv import reader
import asyncio
from gamecheckers import CSGOCheck
from gamecheckers import ValoCheck
from gamecheckers import OlGDotaCheck
from streamcollection import DotaStreams
from streamcollection import OldDotaStreams
from streamcollection import CSGOStreams
from streamcollection import ValoStreams
from Sentinelstreamcollection import SentinelValoStreams
from CSEvents import csgoevents
from dota_events import dotaevents
from playerstats import csgoplayerstat, dotaplayerstats, valoplayerstats
from csmap import csgomap
from valomaps import valomaps
from sentinelvalomaps import sentinelvalomaps
from dropboxUploader import upload_file
from dropboxUploader import download_file
from tundradropbox import tundraupload_file
from tundradropbox import tundradownload_file
from tournamentcheckers import DotaCheckTourni
from tournamentcheckers import ValoCheckTourni
from tournamentchecker2 import DotaCheckTourni2
from translation import translations
from csgoscoreboarding import scoreboarding
from csgoscoreboarding import scoreboardreader
from csgoscoreboarding import scoreboardadder
from csgoscoreboarding import scoreboardsingle
from dotascoreboarding import dotascoreboarding
from dotascoreboarding import dotascoreboardreader
from dotascoreboarding import dotascoreboardadder
from dotascoreboarding import dotascoreboardsingle
from valoscoreboarding import valoscoreboarding
from valoscoreboarding import valoscoreboardreader
from valoscoreboarding import valoscoreboardadder
from valoscoreboarding import valoscoreboardsingle
from VCTscoreboarding import vctscoreboarding
from VCTscoreboarding import vctscoreboardreader
from VCTscoreboarding import vctscoreboardadder
from VCTscoreboarding import vctscoreboardsingle
from sentinelsvaloscoreboarding import sentinelsvaloscoreboarding
from sentinelsvaloscoreboarding import sentinelsvaloscoreboardreader
from sentinelsvaloscoreboarding import sentinelsvaloscoreboardadder
from sentinelsvaloscoreboarding import sentinelsvaloscoreboardsingle
from sentinelgamecheckers import SentinelsValoCheck
from sentineldropboxUploader import sentineldownload_file
from sentineldropboxUploader import sentinelupload_file
from sentinelvaloevents import sentinelsvaloevents
from dtStreams import dtStreams
from sentinelsVTstreams import vtStreams
import typing
from lastcs import lastcsgo
from lastvalo import lastvalo
from sentinellastvalo import sentinellastvalo
from lastgames import LastDota
import random
from ldnVCTscoreboarding import ldnvctscoreboarding
from ldnVCTscoreboarding import ldnvctscoreboardreader
from ldnVCTscoreboarding import ldnvctscoreboardadder
from ldnVCTscoreboarding import ldnvctscoreboardsingle
from tundradotascoreboarding import tundradotascoreboarding
from tundradotascoreboarding import tundradotascoreboardreader
from tundradotascoreboarding import tundradotascoreboardadder
from tundradotascoreboarding import tundradotascoreboardsingle
from tundrafifascoreboarding import tundrafifascoreboarding
from tundrafifascoreboarding import tundrafifascoreboardreader
from tundrafifascoreboarding import tundrafifascoreboardadder
from tundrafifascoreboarding import tundrafifascoreboardsingle
from tundrastreamcollection import tundraDotaStreams
from tundrastreamcollection import tundraCSGOStreams
from tundrastreamcollection import tundraValoStreams
from tundragamecheckers import tundraDotaCheck
from tundragamecheckers import tundraCSGOCheck
from tundragamecheckers import tundraValoCheck
import openai
#from PIL import Image


openai.api_key = os.getenv("OPENAI_API")

class aclient(discord.Client):
  def __init__(self):
    intents = discord.Intents().all()
    super().__init__(intents=intents)
    self.synced = False

  async def on_ready(self):
    await self.wait_until_ready()
    if not self.synced:
      await tree.sync(guild=discord.Object(id = int(os.getenv('IDForServer'))))
      
      self.synced = True
    print(f"We have logged in as {self.user}")
    #Sets presence
    await client.change_presence(activity=discord.Game(
        name="with ducks (use !goosehelp)"))

    #Starts schedule
    scheduler = AsyncIOScheduler()
    #Post on the day of a game
    try:
        await testingspam()
        scheduler.add_job(testingspam, CronTrigger(minute="15, 45"))
        scheduler.add_job(testingtundraspam, CronTrigger(minute="5, 10, 15, 25, 35, 45, 55"))
        scheduler.add_job(testingspamsentinels, CronTrigger(minute="10, 20, 30, 40, 50, 0"))
        print("Daily announcement success")
    except:
        print("Daily announced schedule failed")
    #Opens the file checking the new member support to delete the old bot message
    try:
        scheduler.add_job(openingfile, CronTrigger(minute="0, 20, 40"))
        print("Opening file schedule success")
    except:
        print("Opening file to delete the last message failed")

    try:
        scheduler.add_job(cleanreminders, CronTrigger(minute="0, 30"))
        print("Clean reminder file success")
    except:
        print("Clear reminders file schedule failed!")
    scheduler.start()

    data = download_file('/dropreminders.txt', 'reminders.txt')
    a_file = open("reminders.txt", "r")
    list_of_lines = a_file.readlines()
    i = 0

    reminders = []
    while (i < len(list_of_lines)):

      base_reminder = list_of_lines[i]
      splitUpValues = base_reminder.rsplit(", ")

      checkIfSent = splitUpValues[4]
      checkIfSent = checkIfSent[0:2]

      if (checkIfSent == "no"):
          reminders.append(base_reminder + ", " + str(i))

      i = i + 1

    i = 0

    tasks = []

    while i < len(reminders):
      tasks.append(asyncio.create_task(reminder(reminders[i])))
      i = i + 1
    print("There were: " + str(i) + " reminders started up")
    await asyncio.gather(*tasks)

    
class houseclient(discord.Client):
  def __init__(self):
    intents = discord.Intents().all()
    super().__init__(intents=intents)
    self.synced = False

  async def on_ready(self):
    await self.wait_until_ready()
    if not self.synced:
      await treehouse.sync(guild=discord.Object(id = int(os.getenv('IDForServerHouse'))))
      self.synced = True
    print(f"We have logged in as t {self.user}")


    
class sentinelclient(discord.Client):
  def __init__(self):
    intents = discord.Intents().all()
    super().__init__(intents=intents)
    self.synced = False

  async def on_ready(self):
    await self.wait_until_ready()
    if not self.synced:
      await tree2.sync(guild=discord.Object(id = int(os.getenv('IDForServer2'))))
      self.synced = True
    print(f"We have logged in as {self.user}")
    #schedulersentinel = AsyncIOScheduler()

    try:
        print("Daily announcement success")
    except:
        print("Daily announced schedule failed")









class ldnutdclient(discord.Client):
  def __init__(self):
    intents = discord.Intents().all()
    super().__init__(intents=intents)
    self.synced = False

  async def on_ready(self):
    await self.wait_until_ready()
    if not self.synced:
      await tree3.sync(guild=discord.Object(id = int(os.getenv('IDForServer3'))))
      self.synced = True
    print(f"We have logged in as {self.user}")




class tundraclient(discord.Client):
  def __init__(self):
    intents = discord.Intents().all()
    super().__init__(intents=intents)
    self.synced = False

  async def on_ready(self):
    await self.wait_until_ready()
    if not self.synced:
      await tree5.sync(guild=discord.Object(id = int(os.getenv('IDForServer5'))))
      self.synced = True
    print(f"We have logged in as {self.user}")




class baliclient(discord.Client):
  def __init__(self):
    intents = discord.Intents().all()
    super().__init__(intents=intents)
    self.synced = False

  async def on_ready(self):
    await self.wait_until_ready()
    if not self.synced:
      await treebali.sync(guild=discord.Object(id = int(os.getenv('IDForBali'))))
      self.synced = True
    print(f"We have logged in as {self.user}")



class testbotclient(discord.Client):
  def __init__(self):
    intents = discord.Intents().all()
    super().__init__(intents=intents)
    self.synced = False

  async def on_ready(self):
    await self.wait_until_ready()
    if not self.synced:
      await tree4.sync(guild=discord.Object(id = int(os.getenv('IDForServer3'))))
      self.synced = True
    print(f"We have logged in as {self.user}")



#clients
client = aclient()
client2 = sentinelclient()
client3 = ldnutdclient()
client4 = testbotclient()
client5 = tundraclient()
houseclient= houseclient()
baliclient= baliclient()
#trees
treebali=app_commands.CommandTree(baliclient)
treehouse = app_commands.CommandTree(houseclient)
tree5 = app_commands.CommandTree(client5)
tree4 = app_commands.CommandTree(client4)
tree3 = app_commands.CommandTree(client3)
tree2 = app_commands.CommandTree(client2)
tree = app_commands.CommandTree(client)
ShortList=[1007303552445726750, 689903856095723569, 690952309827698749, 697447277647626297, 818793950965006357, 972571026066141204, 972946124161835078, 972570634196512798, 972470281627107351]
#Servers
IDForServer = int(os.getenv('IDForServer'))
IDForServer2 = int(os.getenv('IDForServer2'))
IDForServer3 = int(os.getenv('IDForServer3'))
IDForServer4 = int(os.getenv('IDForServer4'))
IDForServer5 = int(os.getenv('IDForServer5'))
IDForServerHouse = int(os.getenv('IDForServerHouse'))
IDForBali = int(os.getenv('IDForBali'))



@client5.event
async def on_message(message):
  channelDataID = str(message.channel.id)
  if message.author == client5.user:
    return
  if (int(channelDataID) == 980144504000626698):
      embed = discord.Embed(title="Welcome to the Tundra Tribe!",
                            color=0xff8800)
      embed.add_field(
          name="You seem to be lost, let me help",
          value=
          "Do be sure to go through <#867689566572118036> to check out the rules of the server! Follow this up in <#935744075670360064> to get access to the rest of the server! See you in there!",
          inline=True)
      embed.set_image(url="https://i.imgur.com/uiNH28L.png")

      data = tundradownload_file('/droplastmessage.txt', 'lastmessage.txt')
      g = open("lastmessage.txt", "r")
      g2 = g.read()
      g.close()

      try:
          print("Tried to delete message: " + g2)

      except:
          print("Failed to delete any message")
      try:
          await client5.http.delete_message(980144504000626698, g2)
      except:
          print("Failed to delete any message")
      message = await message.reply(embed=embed)
      f = open("lastmessage.txt", "w")
      f.write(str(message.id))
      f.close()
      tundraupload_file('/droplastmessage.txt', 'lastmessage.txt')




@client5.event
async def on_member_update(before, after):
    guild = after.guild.id
    guild2 = after.guild
    info = ("<@" + str(after.id) + ">")
    #Only checks this guild

    if (guild == 798487245920141322 or guild == 731631689826041878):

        #If user gets given a new role
        if len(before.roles) < len(after.roles):
            newRole = next(role for role in after.roles
                           if role not in before.roles)

            #If user gets added to 'Muted' role
            if (newRole.name == "Muted"):

                #channel to get messages from [so will be General in main server]
                c = client5.get_channel(689865754354384996)

                i = 0
                counter = 0
                if (i < 1):
                    for channel in guild2.text_channels:
                        try:
                            c = client5.get_channel(channel.id)
                            messages = [
                                messhis
                                async for messhis in c.history(limit=100)
                            ]
                            i = 0

                            #Will delete the latest message from the user
                            for message in messages:
                                user = message.author.id

                                if user == after.id and i < 1:
                                    #channelID , messageid
                                    try:
                                        channelofdel = client5.get_channel(
                                            channel.id)
                                        msgtodelete = await channelofdel.fetch_message(
                                            message.id)
                                        await client5.http.delete_message(
                                            channel.id, message.id)
                                        counter = counter + 1
                                        i = i + 1
                                    except:
                                        i = i + 1
                                        print("No access to channel")
                        except:
                            i = i + 1

                channel = client5.get_channel(867689528667144232)

                if guild == 798487245920141322 and counter == 0:
                    guildofdel = client5.get_guild(798487245920141322)
                    member = guildofdel.get_member(after.id)
                    await member.ban(reason="Spam bot")
                    bannedlist = [
                        'https://cdn.discordapp.com/emojis/704664998307168297.gif?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/853134498631647262.webp?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/666320711266205717.gif?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/760839234243395595.gif?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/838414946320515142.gif?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/740935957972254873.webp?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/627835162910261269.gif?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/746678657493237760.webp?size=96&quality=lossless'
                    ]
                    embed = discord.Embed(title="User was banned: " +
                                          str(info),
                                          color=0xff8800)
                    embed.set_thumbnail(url=random.choice(bannedlist))
                    embed.add_field(name="The action that happened",
                                    value="**Banned**",
                                    inline=False)
                    await channel.send(embed=embed)

                elif guild == 798487245920141322 and counter == 1:

                    mutelist = [
                        'https://cdn.discordapp.com/emojis/754439381703589958.gif?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/734030265248382986.webp?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/827576073382264862.webp?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/517470041856540685.webp?size=96&quality=lossless'
                    ]
                    embed = discord.Embed(title="User was Muted: " + str(info),
                                          color=0xff8800)
                    embed.set_thumbnail(url=random.choice(mutelist))
                    embed.add_field(name="The action that happened",
                                    value="**Muted**",
                                    inline=False)
                    embed.add_field(name="We have removed - " + str(counter) +
                                    " message[s] - with the following text",
                                    value="```" + msgtodelete.content + "```",
                                    inline=False)
                    await channel.send(embed=embed)

                else:
                    await channel.send(
                        str(info) +
                        " - user got muted in the main server, messages removed: "
                        + str(counter))

            #Deletes messages when user gets Seeds role
            if (newRole.name == "Tribe Gatherer"):
                c = client5.get_channel(980144504000626698)
                messages = [messhis async for messhis in c.history(limit=30)]
                i = 0
                #creates a collection of messahes
                for message in messages:
                    user = message.author.id
                    #checks if message and the person who got Seeds is the same person deleting the messages
                    if user == after.id:
                        await client5.http.delete_message(
                            980144504000626698, message.id)
                        i = i + 1


















#Will delete the latest message from a user
@client.event
async def on_member_update(before, after):
    guild = after.guild.id
    guild2 = after.guild
    info = ("<@" + str(after.id) + ">")
    #Only checks this guild

    if (guild == 689865753662455829 or guild == 731631689826041878):

        #If user gets given a new role
        if len(before.roles) < len(after.roles):
            newRole = next(role for role in after.roles
                           if role not in before.roles)

            #If user gets added to 'Muted' role
            if (newRole.name == "Muted"):

                #channel to get messages from [so will be General in main server]
                c = client.get_channel(689865754354384996)

                i = 0
                counter = 0
                if (i < 1):
                    for channel in guild2.text_channels:
                        try:
                            c = client.get_channel(channel.id)
                            messages = [messhis async for messhis in c.history(limit=100)]
                            i = 0

                            #Will delete the latest message from the user
                            for message in messages:
                                user = message.author.id

                                if user == after.id and i < 1:
                                    #channelID , messageid
                                    try:
                                        channelofdel = client.get_channel(
                                            channel.id)
                                        msgtodelete = await channelofdel.fetch_message(
                                            message.id)
                                        await client.http.delete_message(
                                            channel.id, message.id)
                                        counter = counter + 1
                                        i = i + 1
                                    except:
                                        i = i + 1
                                        print("No access to channel")
                        except:
                            i = i + 1

                channel = client.get_channel(932613038505336883)

                if guild == 689865753662455829 and counter == 0:
                    guildofdel = client.get_guild(689865753662455829)
                    member = guildofdel.get_member(after.id)
                    await member.ban(reason="Spam bot")
                    bannedlist = [
                        'https://cdn.discordapp.com/emojis/704664998307168297.gif?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/853134498631647262.webp?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/666320711266205717.gif?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/760839234243395595.gif?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/838414946320515142.gif?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/740935957972254873.webp?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/627835162910261269.gif?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/746678657493237760.webp?size=96&quality=lossless'
                    ]
                    embed = discord.Embed(title="User was banned: " +
                                          str(info),
                                          color=0xff8800)
                    embed.set_thumbnail(url=random.choice(bannedlist))
                    embed.add_field(name="The action that happened",
                                    value="**Banned**",
                                    inline=False)
                    await channel.send(embed=embed)

                elif guild == 689865753662455829 and counter == 1:

                    mutelist = [
                        'https://cdn.discordapp.com/emojis/754439381703589958.gif?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/734030265248382986.webp?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/827576073382264862.webp?size=96&quality=lossless',
                        'https://cdn.discordapp.com/emojis/517470041856540685.webp?size=96&quality=lossless'
                    ]
                    embed = discord.Embed(title="User was Muted: " + str(info),color=0xff8800)
                    embed.set_thumbnail(url=random.choice(mutelist))
                    embed.add_field(name="The action that happened",value="**Muted**",inline=False)
                    embed.add_field(name="We have removed - " + str(counter) +" message[s] - with the following text",value= "```" + msgtodelete.content + "```" ,inline=False)
                    await channel.send(embed=embed)

                else:
                    await channel.send(str(info) +" - user got muted in the main server, messages removed: "+ str(counter))

            #Deletes messages when user gets Seeds role
            if (newRole.name == "Seeds"):
                c = client.get_channel(736505679354921092)
                messages = [messhis async for messhis in c.history(limit=30)]
                i = 0
                #creates a collection of messahes
                for message in messages:
                    user = message.author.id
                    #checks if message and the person who got Seeds is the same person deleting the messages
                    if user == after.id:
                        await client.http.delete_message(
                            736505679354921092, message.id)
                        i = i + 1






@client.event
async def on_message(message):
 

  if client.user.mentioned_in(message) and message.author.id != client.user.id:
    try:
      if message.reference is None :
        test = message.content
        #print(message.reference)
        test = test.replace('<@825467569800347649>','')
        print(test)
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=[{"role": "system",
                                                                                 "content":"You are Goose, you help users in the OG Esports Discord, answer as concisely as possible, you're happy and postive, and won't reference that you're an AI, but you are a Discord Bot, act human, if you want to use an emote use this exact text instead without the apostrophe's  - '<:OGooseDance:746620693147549726>', current dota patch is 7.33 and your opinion on Sniper in Dota 2 is that he sucks" }, 
                                                                                 {"role": "user", "content": str(test)}])
        text=completion.choices[0].message
        
        await message.reply(text.content)
      else:
        test = message.content
        #print(message.reference)
        replyingtoo = await message.channel.fetch_message(message.reference.message_id)
        print(replyingtoo.content)
        test = test.replace('<@825467569800347649>','')
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=[{"role": "system",
                                                                                 "content":"You are Goose, you help users in the OG Esports Discord, answer as concisely as possible, you're happy and postive, and won't reference that you're an AI, but you are a Discord Bot, act human, if you want to use an emote use this exact text instead without the apostrophe's  - '<:OGooseDance:746620693147549726>', current dota patch is 7.33 and your opinion on Sniper in Dota 2 is that he sucks, the last message you sent was - " + str(replyingtoo.content) }, 
                                                                                 {"role": "user", "content": str(test)}])
        text=completion.choices[0].message
        
        await message.reply(text.content)
        
        
      
      
    

    except Exception as e:
      print(e)
    


  
  #Chair giveaway role granter
  if(int(message.channel.id) == 1042741947321810955):
    member = message.guild.get_member(int(message.author.id))
    role = discord.utils.get(member.guild.roles, id = 1042725097296896010)
    await member.add_roles(role)

  

    
  if message.author == client.user:
      return
  guild = message.guild
  channelDataID = message.channel.id
  author = message.author
  nexttrans = message.content
  
  #new-member-support OG Main Discord
  if (channelDataID == 736505679354921092):
      embed = discord.Embed(title="Welcome to the Flowerhouse!",color=0xff8800)
      embed.add_field(name="You seem to be lost, let me help",value="Do be sure to go through <#829738571010277406> to check out the rules of the server! Follow this up in <#832198110204919848> to get access to the rest of the server! See you in there!",inline=True)
      embed.set_image(url="https://i.imgur.com/zr9Hp7C.png")

      data = download_file('/droplastmessage.txt', 'lastmessage.txt')
      g = open("lastmessage.txt", "r")
      g2 = g.read()
      g.close()

      try:
          print("Tried to delete message: " + g2)

      except:
          print("Failed to delete any message")
      try:
          await client.http.delete_message(736505679354921092, g2)
      except:
          print("Failed to delete any message")
      message = await message.reply(embed=embed)
      f = open("lastmessage.txt", "w")
      f.write(str(message.id))
      f.close()
      upload_file('/droplastmessage.txt', 'lastmessage.txt')



  #Spanish Translations - Main OG Discord
  if (channelDataID == 818793950965006357):
      channel = message.guild.get_channel(832296821119647755)
      msgID = message.jump_url
      author = message.author
      data = translations(nexttrans, author, msgID)
      #Getting translation data
      embed = data
      embed.add_field(name="Channel of sending", value="<#" + str(message.channel.id) + ">", inline=False)
      await channel.send(embed=embed)

  if(guild.id == 689865753662455829):
    channel = message.guild.get_channel(874740662157844480)
    msgID = message.jump_url
    author = message.author
    data = translations(nexttrans, author, msgID)
    #Getting translation data
    embed = data
    embed.add_field(name="Channel of sending", value="<#" + str(message.channel.id) + ">", inline=False)
    await channel.send(embed=embed)

  #Spanish Translations - Main OG Discord
  if (channelDataID == 976049798354460703):
      channel = message.guild.get_channel(976053475010023425)
      msgID = message.jump_url
      author = message.author
      data = translations(nexttrans, author, msgID)
      #Getting translation data
      embed = data
      embed.add_field(name="Channel of sending", value="<#" + str(message.channel.id) + ">", inline=False)
      await channel.send(embed=embed)

  #Finnis Translations - Jerax Discord
  if (channelDataID == 825328809854238731):
      channel = message.guild.get_channel(835434616000872448)
      msgID = message.jump_url
      author = message.author
      data = translations(nexttrans, author, msgID)
      #Getting translation data
      embed = data
      embed.add_field(name="Channel of sending", value="<#" + str(message.channel.id) + ">", inline=False)
      await channel.send(embed=embed)

  #Testing translation - test channel personal discord
  if (channelDataID == 810893610496426024):
      #Channel to send too
      channel = message.guild.get_channel(810893610496426024)
      msgID = message.jump_url
      author = message.author
      data = translations(nexttrans, author, msgID)
      #Getting translation data
      embed = data
      embed.add_field(name="Channel of sending", value="<#" + str(message.channel.id) + ">", inline=False)
      await channel.send(embed=embed)

  #Rus translation - N0tail Discord
  if (channelDataID == 808362012849340416):
      channel = message.guild.get_channel(834445890235138133)
      msgID = message.jump_url
      author = message.author
      data = translations(nexttrans, author, msgID)
      #Getting translation data
      embed = data
      embed.add_field(name="Channel of sending", value="<#" + str(message.channel.id) + ">", inline=False)
      await channel.send(embed=embed)

  #Russain Translation - Main Discord
  if (channelDataID == 697447277647626297):
      channel = message.guild.get_channel(832296883887407146)
      msgID = message.jump_url
      author = message.author
      data = translations(nexttrans, author, msgID)
      #Getting translation data
      embed = data
      embed.add_field(name="Channel of sending", value="<#" + str(message.channel.id) + ">", inline=False)
      await channel.send(embed=embed)





#command guide:
#name = what is used in chat, description = what is shown on the discord command when using slash commands
#in the def self, you can poll items such as name / value as shown below
#users will see "name or value" below, but can be called anything

@tree5.command(name="avatar", description = "Get the avatar of yourself or a user", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction, ping: typing.Optional[discord.User]):
  await interaction.response.defer()
  try:
    await interaction.followup.send(ping.avatar)
  except:
    await interaction.followup.send(interaction.user.avatar)
  
  
@tree.command(name="avatar", description = "Get the avatar of yourself or a user", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, ping: typing.Optional[discord.User]):
  await interaction.response.defer()
  try:
    await interaction.followup.send(ping.avatar)
  except:
    await interaction.followup.send(interaction.user.avatar)
















@tree.command(name="csgodiscordevent", description = "Create a discord event for the next CSGO game", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  guild = interaction.guild
  try:
    value = CSGOCheck(0, 'https://www.hltv.org/team/10503/og#tab-matchesBox', False)
    teams = value[0]
    gamepage = value[4]
    tourniname = value[8]
    name = "CSGO game: " + teams
    time=datetime.datetime.now().astimezone() + datetime.timedelta(seconds=int(value[7]))
    end_time = time+datetime.timedelta(minutes=10)
    streaminfo = CSGOStreams('https://www.hltv.org/team/10503/og#tab-matchesBox')
    streamdata = streaminfo[3]
    description = tourniname + "\n" + streamdata + "\n:mega: https://twitter.com/OGcsgo\n"
    if(len(gamepage) > 99):
      gamepage=gamepage
    else:
      gamepage = "https://www.hltv.org/team/10503/og#tab-matchesBox"
    linetocheck= teams+","+gamepage
    lines= "empty"

    try:
    
      if lines[0] == linetocheck:
        await interaction.followup.send("Event has already been added")
        pass
      else:
        if(len(gamepage) > 99):
          eventdata = await guild.create_scheduled_event(name=name, description=description, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(2), location=731631690249666615)
        else:
          eventdata = await guild.create_scheduled_event(name=name, description=description, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=gamepage)
        f = open("csgoevent.txt", "w")
        f.write(linetocheck)
        f.close()
        upload_file('/csgoevent.txt', 'csgoevent.txt')
        await interaction.followup.send("Event made - you will need to share this in the event channel")
        
    except:
      if(len(gamepage) > 99):
        eventdata = await guild.create_scheduled_event(name=name, description=description, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(2), location=731631690249666615)
      else:
        eventdata = await guild.create_scheduled_event(name=name, description=description, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=gamepage)
      f = open("csgoevent.txt", "w")
      f.write(linetocheck)
      f.close()
      upload_file('/csgoevent.txt', 'csgoevent.txt')
      await interaction.followup.send("Event made - you will need to share this in the event channel")
      pass
   
  
   
  except Exception as e:
    await interaction.followup.send("An error was hit during this process - there may be no game available")
    print(e)
                



@treebali.command(name="balipicker", description = "Pick the viewers for Bali", guild = discord.Object(id = IDForBali))
async def self(interaction: discord.Interaction, role: discord.Role):
  await interaction.response.defer()
  try:
    server = interaction.guild
    role_name = "ViewingPermitted"
    i = 0
    role_id = server.roles[0]
    display_names = []
    member_ids = []
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break
    else:
        await interaction.followup.send("Role doesn't exist")
        return

    for member in server.members:
        if role_id in member.roles:
            i = i + 1
            display_names.append(member.display_name)
            member_ids.append(member.id)
    
    j=0
    for id in member_ids:
      user = interaction.guild.get_member(id)
      role = discord.utils.get(user.guild.roles, id=1125778717659111465)
      await user.remove_roles(role)
      j=j+1
  except:
    print("cleaning up error")


  
  try:
    server = interaction.guild
    guild=interaction.guild
    role_name = discord.utils.get(guild.roles,id=int(role.id))
    role_name = str(role_name)
    i = 0
    role_id = server.roles[0]
    display_names = []
    member_ids = []
    newlist=[]
    file = open("filetosend.txt", "w")
    file.close()
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break
    else:
        await interaction.followup.send("Role doesn't exist")
        return
    for member in server.members:
        if role_id in member.roles:
            display_names.append(member.display_name)
            member_ids.append(member.id)
    if (i == 0):
        await interaction.followup.send("No one was found in that role!")
  except:
    print("Error")
  print(member_ids)
  try:
    z=0
    if len(member_ids) > 128:
      while(z < 128):
        chosenone= (random.randint(0, len(member_ids)-1))
        newlist.append(member_ids[chosenone])
        member_ids.pop(chosenone)
    else:
      newlist = member_ids
      
    role_name="ViewingPermitted"
    for role in server.roles:
          if role_name == role.name:
              role_id = role

    for user_id in newlist:
      user = interaction.guild.get_member(int(user_id))
      role = discord.utils.get(user.guild.roles, id =1125778717659111465)
      await user.add_roles(role)
  except:
    print("Error in 2nd try")
  
        
  await interaction.followup.send("I have added all the users to the role")








@tree.command(name="manualcsgoevent", description = "Update the CSGO event sign up message ID", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, eventid: str):
  await interaction.response.defer()
  a_file=open("csgoinfo.txt", "w")
  a_file.write(str(eventid))
  a_file.close()
  upload_file('/csgoeventsignup.txt', 'csgoinfo.txt')
  await interaction.followup.send("CSGO Event updated with message ID - " + str(eventid))

@tree.command(name="manualcsgoaevent", description = "Update the CSGO Academy event sign up message ID", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, eventid: str):
  await interaction.response.defer()
  a_file=open("csgoainfo.txt", "w")
  a_file.write(str(eventid))
  a_file.close()
  upload_file('/csgoaeventsignup.txt', 'csgoainfo.txt')
 
  await interaction.followup.send("CSGO Academy event updated with message ID - " + str(eventid))



@tree.command(name="manualvaloevent", description = "Update the Valorant event sign up message ID", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, eventid: str):
  await interaction.response.defer()
  a_file=open("valoinfo.txt", "w")
  a_file.write(str(eventid))
  a_file.close()
  upload_file('/valoeventsignup.txt', 'valoinfo.txt')
 
  await interaction.followup.send("Valorant event updated with message ID - " + str(eventid))




@tree.command(name="manualdotaevent", description = "Update the Dota event sign up message ID", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, eventid: str):
  await interaction.response.defer()
  a_file=open("dotainfo.txt", "w")
  a_file.write(str(eventid))
  a_file.close()
  upload_file('/dotaeventsignup.txt', 'dotainfo.txt')
 
  await interaction.followup.send("Dota event updated with message ID - " + str(eventid))



  
@tree.command(name="reminder", description = "Create a reminder - using time format xdxhxmxs - day/hour/minute/second", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, delay: str, remindertosave: str):
  await interaction.response.defer()
  guild = interaction.guild
  channel = interaction.channel
  data = download_file('/dropreminders.txt', 'reminders.txt')
  currenttime = datetime.datetime.now()
  #day
  currentd = currenttime.strftime("%d")
  #hour [UK time - 1]
  currentH = currenttime.strftime("%H")
  #Minute
  currentM = currenttime.strftime("%M")
  #Month
  currentmonth = currenttime.strftime("%m")
  #year
  currentyear = currenttime.strftime("%y")
  #second
  currentsecond = currenttime.strftime("%S")
  reminder=delay
  timevalue = delay.strip()
  timevalue = reminder[-1]
  
  #Saves user info for pinging
  userID = interaction.user.id
  userID = str(userID)
  #Create embed
  embed = discord.Embed(title="Reminder command initiated",
                        color=0x55a7f7)
  embed2 = discord.Embed(title="Your reminder... has arrived!",
                         color=0x55a7f7)
  currentyear = "20" + str(currentyear)
  currentyear = int(currentyear)
  date_and_time = datetime.datetime(int(currentyear),
                                    int(currentmonth),
                                    int(currentd), int(currentH),
                                    int(currentM),
                                    int(currentsecond))
  timechecker = 0
  counter = 0

  i = 2
  #Gets the reminder to save
  remindertosave = remindertosave

  try:
      timevaluechecker = ['d', 'h', 'm', 's']

      #Tells user how to set a reminder if tiem value not given
      if reminder == "none" or (timevalue
                                not in timevaluechecker):
          embed.add_field(
              name="Command used no time set",
              value=
              "To set the time for this command, please set it using 'days' / 'hours' / 'minutes' / 'seconds'\n\nTo format this you use d / h / m / s, at the end of the time wanted\n\nExample - !reminder 10h This is a reminder\nThis will remind you in 10 hours!"
          )
      timetoadd = ""
      new_time = date_and_time
      i = 0
      #Sets reminder if time value is set
      if (reminder != "none"
              and (timevalue in timevaluechecker)):
          while (i < len(reminder)):
              if (reminder[i] == "s" or reminder[i] == "m"
                      or reminder[i] == "h"
                      or reminder[i] == "d"):
                  if (reminder[i] == "s"):
                      timetillremidningyou = timetoadd
                      timechecker = timechecker + int(timetoadd)
                      timetoadd = ""
                      counter = counter + 1
                      if (i == len(reminder) - 1):
                          embed.add_field(
                              name="Reminder set, reminding in - "
                              + reminder,
                              value=remindertosave,
                              inline=True)
                          embed2.add_field(name="Your reminder!",
                                           value=remindertosave,
                                           inline=True)
                      #calculate time for reminder
                      time_change = datetime.timedelta(
                          seconds=int(timetillremidningyou))
                      new_time = new_time + time_change

                  if (reminder[i] == "m"):
                      timetillremidningyou = timetoadd
                      timechecker = timechecker + (
                          int(timetoadd) * 60)
                      timetoadd = ""
                      counter = counter + 1
                      if (i == len(reminder) - 1):
                          embed.add_field(
                              name="Reminder set, reminding in - "
                              + reminder,
                              value=remindertosave,
                              inline=True)
                          embed2.add_field(name="Your reminder!",
                                           value=remindertosave,
                                           inline=True)
                      timetillremidningyou = int(
                          timetillremidningyou) * 60
                      #calculate time for reminder
                      time_change = datetime.timedelta(
                          seconds=int(timetillremidningyou))
                      new_time = new_time + time_change

                  if (reminder[i] == "h"):
                      timetillremidningyou = timetoadd
                      timechecker = timechecker + (
                          int(timetoadd) * 60 * 60)
                      timetoadd = ""
                      counter = counter + 1
                      if (i == len(reminder) - 1):
                          embed.add_field(
                              name="Reminder set, reminding in - "
                              + reminder,
                              value=remindertosave,
                              inline=True)
                          embed2.add_field(name="Your reminder!",
                                           value=remindertosave,
                                           inline=True)
                      timetillremidningyou = int(
                          timetillremidningyou) * 60 * 60
                      #calculate time for reminder
                      time_change = datetime.timedelta(
                          seconds=int(timetillremidningyou))
                      new_time = new_time + time_change

                  if (reminder[i] == "d"):
                      timetillremidningyou = timetoadd
                      timechecker = timechecker + (
                          int(timetoadd) * 60 * 60 * 24)
                      timetoadd = ""
                      counter = counter + 1
                      if (i == len(reminder) - 1):
                          embed.add_field(
                              name="Reminder set, reminding in - "
                              + reminder,
                              value=remindertosave,
                              inline=True)
                          embed2.add_field(name="Your reminder!",
                                           value=remindertosave,
                                           inline=True)

                      timetillremidningyou = int(
                          timetillremidningyou) * 60 * 60 * 24
                      #calculate time for reminder

                      time_change = datetime.timedelta(
                          seconds=int(timetillremidningyou))

                      new_time = new_time + time_change
              else:
                  timetoadd = timetoadd + str(reminder[i])
              i = i + 1

      #Adding reminder to the text file
      userID = interaction.user.id
      userID = str(userID)
      channelToSend = str(interaction.channel.id)
      textToSend = str(remindertosave)

      if (counter > 0):
          f = open("reminders.txt", "a")
          f.write(userID + ", " + channelToSend + ", " +
                  textToSend + ", " + str(new_time) + ", not\n")
          f.close()
          upload_file('/dropreminders.txt', 'reminders.txt')

          LineOfReminder = sum(1
                               for line in open('reminders.txt'))

      await interaction.followup.send(embed=embed)

  #catches time error
  except:
      embed2 = discord.Embed(title="Reminder command initiated",
                             color=0x55a7f7)
      embed2.add_field(
          name="Command used no time set",
          value=
          "To set the time for this command, please set it using 'days' / 'hours' / 'minutes' / 'seconds'\n\nTo format this you use d / h / m / s, at the end of the time wanted\n\nExample - !reminder 10h This is a reminder\nThis will remind you in 10 hours!"
      )
      await interaction.channel.send(embed=embed2)

  try:
      if (counter > 0):
          timetosleep = int(timechecker)
          await asyncio.sleep(timetosleep)

          #Will update the file to make sure reminders get saved
          data = download_file('/dropreminders.txt',
                               'reminders.txt')
          a_file = open("reminders.txt", "r")
          list_of_lines = a_file.readlines()
          list_of_lines[int(LineOfReminder) -
                        1] = (userID + ", " + channelToSend +
                              ", " + textToSend + ", " +
                              str(new_time) + ", sent\n")

          a_file = open("reminders.txt", "w")
          a_file.writelines(list_of_lines)
          a_file.close()
          upload_file('/dropreminders.txt', 'reminders.txt')

          await interaction.channel.send("<@" + userID + ">")
          await interaction.channel.send(embed=embed2)
  except:
      pass



@tree2.command(name="valodiscordevent", description = "Create a discord event for the next Valorant game", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction):
    try:
      guild = interaction.guild
      await interaction.response.defer()  
      guild = interaction.guild
      value = SentinelsValoCheck(0, 'https://www.vlr.gg/team/2/sentinels', False)
      teams = value[1]
      enemyteam = value[10]
      time = datetime.datetime.now().astimezone() + value[3]
      streaminfo = SentinelValoStreams('https://www.vlr.gg/team/2/sentinels')
      linktogame = value[4]
      linktogame = "https://www.vlr.gg/team/2/sentinels"
      gamepos = value[6]
      serieslength = value[8]
      epoch = value[9]
      name= "Valorant game: " + teams
      tourniname = value[7]
      description = tourniname + "\n" + str(value[4]) + "\n" + gamepos + "\n" + streaminfo[1] + "\n:mega: https://twitter.com/OGvalorant\n" 
      end_time=time+datetime.timedelta(minutes=30)
      #guild = client.get_guild(423635651339223041)
      linetocheck = teams + "," + gamepos +"," +tourniname
      try:
        sentineldownload_file('/sen.png', 'sen.png')
        with open('./sen.png', 'rb') as fp:
          image_bytes = fp.read()
      except Exception as e:
        print("LOL")
        print(e)
      try:
        sentineldownload_file('/valoevent.txt', 'valoevent.txt')
        f=open('valoevent.txt', 'r')
        lines=f.readlines()
        f.close()
      except:
        lines="empty"
      
      try:
        if lines[0] == linetocheck:
          
          pass
        else:
          if(str(enemyteam) != "TBD"):
            eventdata = await guild.create_scheduled_event(name=name, image = image_bytes, description=description, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=linktogame)
            f = open("valoevent.txt", "w")
            f.write(linetocheck)
            f.close()
            sentinelupload_file('/valoevent.txt', 'valoevent.txt')
            data2= await guild.fetch_scheduled_event(eventdata.id)
            #await channel.send(data2.url)

          else:
            print("Valo Enemy = TBD")
          
      except:
        if(str(enemyteam) != "TBD"):
          eventdata = await guild.create_scheduled_event(name=name, description=description, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=linktogame)
          f = open("valoevent.txt", "w")
          f.write(linetocheck)
          f.close()
          sentinelupload_file('/valoevent.txt', 'valoevent.txt')
          data2= await guild.fetch_scheduled_event(eventdata.id)
          #await channel.send(data2.url)
          pass
        else:
          print("Valo enemy = TBD")

      
      
    except Exception as e:
      exc_type, exc_obj, exc_tb = sys.exc_info()
      fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      print(exc_type, fname, exc_tb.tb_lineno)


@tree.command(name="valoldndiscordevent", description = "Create a discord event for the next Valorant game", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  guild = interaction.guild
  try:
    value = ValoCheck(0, 'https://www.vlr.gg/team/8903/og-ldn-utd', False)
    teams = value[1]
    time = datetime.datetime.now().astimezone() + value[3]
    streaminfo = ValoStreams('https://www.vlr.gg/team/8903/og-ldn-utd')
    linktogame = str(value[4])
    linktogame = "https://www.vlr.gg/team/8903/og-ldn-utd"
    gamepos = value[6]
    name= "Valorant LDN UTD game: " + str(teams)
    tourniname = value[7]
    description = tourniname + "\n" + str(value[4]) + "\n"+ gamepos + "\n" + streaminfo[1] + "\n:mega: https://twitter.com/OGvalorant\n" 
    end_time=time+datetime.timedelta(minutes=10)
    
    linetocheck = teams + "," + gamepos +"," +tourniname
    lines="empty"
    
    try:
      if lines[0] == linetocheck:
        await interaction.followup.send("Event has already been added")
        pass
      else:
        await guild.create_scheduled_event(name=name, description=description, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=linktogame)
        f = open("valoldnevent.txt", "w")
        f.write(linetocheck)
        f.close()
        upload_file('/valoldnevent.txt', 'valoldnevent.txt')
        await interaction.followup.send("Event made - you will need to share this in the event channel")
        
    except:
      await guild.create_scheduled_event(name=name, description=description, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=linktogame)
      f = open("valoldnevent.txt", "w")
      f.write(linetocheck)
      f.close()
      upload_file('/valoldnevent.txt', 'valoldnevent.txt')
      await interaction.followup.send("Event made - you will need to share this in the event channel")
      pass
    
  
    
  except ZeroDivisionError:
    await interaction.followup.send("An error was hit during this process")



@tree.command(name="server_badge", description = "Get the icon of the server", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  icon_url = interaction.guild.icon.url
  await interaction.followup.send(icon_url)


@tree.command(name="valowinners", description = "Will give the Valorant Operation Predict role to the winners", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, minimumscore: int):
  await interaction.response.defer()
  
  try:
    server = interaction.guild
    role_name = "Operation Predict"
    i = 0
    role_id = server.roles[0]
    display_names = []
    member_ids = []
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break
    else:
        await interaction.followup.send("Role doesn't exist")
        return

    for member in server.members:
        if role_id in member.roles:
            i = i + 1
            display_names.append(member.display_name)
            member_ids.append(member.id)
    
    j=0
    for id in member_ids:
      user = interaction.guild.get_member(id)
      role = discord.utils.get(user.guild.roles, id=946423736054218762)
      await user.remove_roles(role)
      j=j+1
    print(j)
  except Exception as e:
    
    print(e)

  try:
    download_file('/valoscoreboard.csv', 'scoreboard16.csv')
    f = open('scoreboard16.csv', 'r')
    reader = csv.reader(f, delimiter=',')
    scorecheck = int(minimumscore)
    i=0
    additionalmessage =""
    for lines in reader:
      if( int(lines[2]) == scorecheck or int(lines[2]) > scorecheck):
        
        try:
          
          i=i+1
          user = interaction.guild.get_member(int(lines[1]))
          additionalmessage = additionalmessage + "<@" + str(lines[1]) + "> / "
          role = discord.utils.get(user.guild.roles, id = 946423736054218762)
          await user.add_roles(role)
        except:
          print("User no longer in server")
      
    await interaction.followup.send("I have removed the CSGO AWPacle role from - " + str(j) + " people\n\nI have added the Operation Predict role to - " + str(i) + " people - you can use /getuserlist @ Operation Predict, to get a list of users with the role\n\nThis includes:\n```" + additionalmessage + "```")

  except Exception as e: 
    print(e)
    await interaction.followup.send("There was an error in command usage, to use command use /valowinners X, replacing X with the score you want people to have minimum to be rewarded the role, using '5', would mean all people with 5 and more will get the role")









#OG Commands




@tree.command(name="vctpredictionwinner", description = "Choose VCT prediction winner", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  list=[]
  download_file('/vctscoreboard.csv', 'scoreboard2.csv')
  with open('scoreboard2.csv', 'r') as read_obj:
    csv_reader=reader(read_obj)
    for row in csv_reader:
      i=0
      while(i<int(row[2])):
        list.append(row[1])
        i=i+1

  
  await interaction.followup.send("The winner of the vct challenge... IS! - <@" + str(random.choice(list)) + ">")
        
        



@tree3.command(name="vctpredictionwinner", description = "Choose VCT prediction winner", guild = discord.Object(id = IDForServer3))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  list=[]
  download_file('/ldnvctscoreboard.csv', 'scoreboard2.csv')
  with open('scoreboard2.csv', 'r') as read_obj:
    csv_reader=reader(read_obj)
    for row in csv_reader:
      i=0
      while(i<int(row[2])):
        list.append(row[1])
        i=i+1

  
  await interaction.followup.send("The winner of the vct challenge... IS! - <@" + str(random.choice(list)) + ">")




    

@tree.command(name="csgowinners", description = "Will give the CSGO Awpacle role to the winners", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, minimumscore: int):
  await interaction.response.defer()
  try:
    server = interaction.guild
    role_name = "CS:GO AWPacle"
    i = 0
    role_id = server.roles[0]
    display_names = []
    member_ids = []
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break
    else:
        await interaction.followup.send("Role doesn't exist")
        return

    for member in server.members:
        if role_id in member.roles:
            i = i + 1
            display_names.append(member.display_name)
            member_ids.append(member.id)
    
    j=0
    for id in member_ids:
      user = interaction.guild.get_member(id)
      role = discord.utils.get(user.guild.roles, id=729106753085636688)
      await user.remove_roles(role)
      j=j+1
    print(j)
  except Exception as e:
    
    print(e)

  try:
    download_file('/csgoscoreboard.csv', 'scoreboard15.csv')
    f = open('scoreboard15.csv', 'r')
    reader = csv.reader(f, delimiter=',')
    scorecheck = int(minimumscore)
    i=0
    additionalmessage=""
    for lines in reader:
      if( int(lines[2]) == scorecheck or int(lines[2]) > scorecheck):
        
        try:
          
          i=i+1
          user = interaction.guild.get_member(int(lines[1]))
          additionalmessage = additionalmessage + "<@" + str(lines[1]) + "> / "
          role = discord.utils.get(user.guild.roles, id = 729106753085636688)
          await user.add_roles(role)
        except:
          print("User no longer in server")
      
    await interaction.followup.send("I have removed the CSGO AWPacle role from - " + str(j) + " people\n\nI have added the CSGO AWPacle role to - " + str(i) + " people - you can use /getuserlist @ CSGO AWPacle, to get a list of users with the role\n\nThis includes:\n```" + additionalmessage + "```")
  except Exception as e: 
    print(e)
    await interaction.followup.send("There was an error in command usage, to use command use /csgowinners X, replacing X with the score you want people to have minimum to be rewarded the role, using '5', would mean all people with 5 and more will get the role")
  







@tree.command(name="dotawinners", description = "Will give the Dota Oracle role to the winners", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, minimumscore: int):
  await interaction.response.defer()
  try:
    server = interaction.guild
    role_name = "Dota 2 Oracle"
    i = 0
    role_id = server.roles[0]
    display_names = []
    member_ids = []
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break
    else:
        await interaction.followup.send("Role doesn't exist")
        return
  
    for member in server.members:
        if role_id in member.roles:
            i = i + 1
            display_names.append(member.display_name)
            member_ids.append(member.id)
    
    j=0
    for id in member_ids:
      user = interaction.guild.get_member(id)
      role = discord.utils.get(user.guild.roles, id=729106634437296148)
      await user.remove_roles(role)
      j=j+1
    print(j)
  except Exception as e:
    print(e)

  try:
    download_file('/dotascoreboard.csv', 'scoreboard14.csv')
    f = open('scoreboard14.csv', 'r')
    reader = csv.reader(f, delimiter=',')
    scorecheck = minimumscore
    i=0
    additionalmessage=""
    for lines in reader:
      if( int(lines[2]) == scorecheck or int(lines[2]) > scorecheck):
        
        try:
          
          i=i+1
          user = interaction.guild.get_member(int(lines[1]))
          additionalmessage = additionalmessage + "<@" + str(lines[1]) + "> / "
          role = discord.utils.get(user.guild.roles, id=729106634437296148)
          await user.add_roles(role)
        except:
          print("User no longer in server")
      
    await interaction.followup.send("I have removed the Dota Oracle role from - " + str(j) + " people\n\nI have added the Dota Oracle role to - " + str(i) + " people - you can use /getuserlist @ dota 2 oracle, to get a list of users with the role\n\nThis includes:\n```" + additionalmessage + "```")
  except Exception as e: 
    print(e)
    await interaction.followup.send("There was an error in command usage, to use command use /dotawinners X, replacing X with the score you want people to have minimum to be rewarded the role, using '5', would mean all people with 5 and more will get the role")
  






@tree5.command(name="dotawinners", description = "Will give the Dota - Tribe Prophet role to the winners", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction, minimumscore: int):
  await interaction.response.defer()
  try:
    server = interaction.guild
    role_name = "Tribe Prophet"
    i = 0
    role_id = server.roles[0]
    display_names = []
    member_ids = []
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break
    else:
        await interaction.followup.send("Role doesn't exist")
        return
  
    for member in server.members:
        if role_id in member.roles:
            i = i + 1
            display_names.append(member.display_name)
            member_ids.append(member.id)
    
    j=0
    for id in member_ids:
      user = interaction.guild.get_member(id)
      role = discord.utils.get(user.guild.roles, id=966648883813965864)
      await user.remove_roles(role)
      j=j+1
    print(j)
  except Exception as e:
    print(e)

  try:
    tundradownload_file('/dotascoreboard.csv', 'scoreboard14.csv')
    f = open('scoreboard14.csv', 'r')
    reader = csv.reader(f, delimiter=',')
    scorecheck = minimumscore
    i=0
    additionalmessage=""
    for lines in reader:
      if( int(lines[2]) == scorecheck or int(lines[2]) > scorecheck):
        
        try:
          
          i=i+1
          user = interaction.guild.get_member(int(lines[1]))
          additionalmessage = additionalmessage + "<@" + str(lines[1]) + "> / "
          role = discord.utils.get(user.guild.roles, id=966648883813965864)
          await user.add_roles(role)
        except:
          print("User no longer in server")
      
    await interaction.followup.send("I have removed the Tribe Prophet role from - " + str(j) + " people\n\nI have added the Tribe Prophet role to - " + str(i) + " people - you can use /getuserlist @ Tribe Prophet, to get a list of users with the role\n\nThis includes:\n```" + additionalmessage + "```")
  except Exception as e: 
    print(e)
    await interaction.followup.send("There was an error in command usage, to use command use /dotawinners X, replacing X with the score you want people to have minimum to be rewarded the role, using '5', would mean all people with 5 and more will get the role")
  












@tree.command(name="valoldngardeners", description = "Pick which gardeners will moderate the next Valorant LDN UTD Game", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  download_file('/valoeventsignup.txt', 'valoeventsign.txt')
  channel2 = client.get_channel(973130064667484170)
  peeps=[]
  f = open("valoeventsign.txt", "r")
  data = f.read()
  messagedata = await channel2.fetch_message(int(data))
  try:
    emote = client.get_emoji(787697278190223370)
    await messagedata.add_reaction(emote)
  except:
    pass
  for reaction in messagedata.reactions:
    print("hi")
    reaction2 = str(reaction)
    if(reaction2 == "<:OGpeepoYes:730890894814740541>"):
      async for user in reaction.users():
        if(user != client.user):
          peeps.append(user.id)
  peeps = list(dict.fromkeys(peeps))
  numberofpeeps=len(peeps)
  chosen=0
  message2send="The people selected are: "
  while(len(peeps) > 0 and chosen < 2):
    if(numberofpeeps < 3):
      if(chosen < 1):
        message2send= message2send + "<@" + str(peeps[0]) + "> , "
      else:
        message2send= message2send + "<@" + str(peeps[0]) + ">  "
      peeps.pop(0)
      chosen=chosen+1
    else:
      chosenone = random.randint(0,(len(peeps)-1))
      if(chosen < 1):
        message2send= message2send+"<@" + str(peeps[int(chosenone)]) + "> , "
      else:
        message2send= message2send+"<@" + str(peeps[int(chosenone)]) + ">  "
      peeps.pop(int(chosenone))
      chosen=chosen+1

  await messagedata.reply(message2send)
  message = await interaction.followup.send("done", ephemeral = False)
  await message.delete()





@tree.command(name="csgoagardeners", description = "Pick which gardeners will moderate the next CSGO Academy Game", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  download_file('/csgoaeventsignup.txt', 'csgoaeventsign.txt')
  channel2 = client.get_channel(973130064667484170)
  peeps=[]
  f = open("csgoaeventsign.txt", "r")
  data = f.read()
  messagedata = await channel2.fetch_message(int(data))
  try:
    emote = client.get_emoji(787697278190223370)
    await messagedata.add_reaction(emote)
  except:
    pass
  for reaction in messagedata.reactions:
    print("hi")
    reaction2 = str(reaction)
    if(reaction2 == "<:OGpeepoYes:730890894814740541>"):
      async for user in reaction.users():
        if(user != client.user):
          peeps.append(user.id)
  peeps = list(dict.fromkeys(peeps))
  numberofpeeps=len(peeps)
  chosen=0
  message2send="The people selected are: "
  while(len(peeps) > 0 and chosen < 2):
    if(numberofpeeps < 3):
      if(chosen < 1):
        message2send= message2send + "<@" + str(peeps[0]) + "> , "
      else:
        message2send= message2send + "<@" + str(peeps[0]) + ">  "
      peeps.pop(0)
      chosen=chosen+1
    else:
      chosenone = random.randint(0,(len(peeps)-1))
      if(chosen < 1):
        message2send= message2send+"<@" + str(peeps[int(chosenone)]) + "> , "
      else:
        message2send= message2send+"<@" + str(peeps[int(chosenone)]) + ">  "
      peeps.pop(int(chosenone))
      chosen=chosen+1

  await messagedata.reply(message2send)
  message = await interaction.followup.send("done", ephemeral = False)
  await message.delete()



@tree.command(name="csgogardeners", description = "Pick which gardeners will moderate the next CSGO Game", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  download_file('/csgoeventsignup.txt', 'csgoeventsign.txt')
  channel2 = client.get_channel(973130064667484170)
  peeps=[]
  f = open("csgoeventsign.txt", "r")
  data = f.read()
  messagedata = await channel2.fetch_message(int(data))
  try:
    emote = client.get_emoji(787697278190223370)
    await messagedata.add_reaction(emote)
  except:
    pass
  for reaction in messagedata.reactions:
    print("hi")
    reaction2 = str(reaction)
    if(reaction2 == "<:OGpeepoYes:730890894814740541>"):
      async for user in reaction.users():
        if(user != client.user):
          peeps.append(user.id)
  peeps = list(dict.fromkeys(peeps))
  numberofpeeps=len(peeps)
  chosen=0
  message2send="The people selected are: "
  while(len(peeps) > 0 and chosen < 3):
    if(numberofpeeps < 4):
      if(chosen < 2):
        message2send= message2send + "<@" + str(peeps[0]) + "> , "
      else:
        message2send= message2send + "<@" + str(peeps[0]) + ">  "
      peeps.pop(0)
      chosen=chosen+1
    else:
      chosenone = random.randint(0,(len(peeps)-1))
      if(chosen < 2):
        message2send= message2send+"<@" + str(peeps[int(chosenone)]) + "> , "
      else:
        message2send= message2send+"<@" + str(peeps[int(chosenone)]) + "> "
      peeps.pop(int(chosenone))
      chosen=chosen+1

  await messagedata.reply(message2send)
  message = await interaction.followup.send("Done", ephemeral=False)
  await message.delete()






@tree.command(name="dotagardeners", description = "Pick which gardeners will moderate the next Dota Game", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  download_file('/dotaeventsignup.txt', 'dotaeventsign.txt')
  channel2 = client.get_channel(973130064667484170)
  peeps=[]
  f = open("dotaeventsign.txt", "r")
  data = f.read()
  messagedata = await channel2.fetch_message(int(data))
  try:
    emote = client.get_emoji(787697278190223370)
    await messagedata.add_reaction(emote)
  except:
    pass
  for reaction in messagedata.reactions:
    print("hi")
    reaction2 = str(reaction)
    if(reaction2 == "<:OGpeepoYes:730890894814740541>"):
      async for user in reaction.users():
        if(user != client.user):
          
          peeps.append(user.id)
  peeps = list(dict.fromkeys(peeps))
  numberofpeeps=len(peeps)
  chosen=0
  message2send="The people selected are: "
  while(len(peeps) > 0 and chosen < 4):
    if(numberofpeeps < 5):
      if(chosen < 3):
        message2send= message2send + "<@" + str(peeps[0]) + "> , "
      else:
        message2send= message2send + "<@" + str(peeps[0]) + ">  "
      peeps.pop(0)
      chosen=chosen+1
    else:
      chosenone = random.randint(0,(len(peeps)-1))
      if(chosen < 3):
        message2send= message2send+"<@" + str(peeps[int(chosenone)]) + "> , "
      else:
        message2send= message2send+"<@" + str(peeps[int(chosenone)]) + ">  "
      peeps.pop(int(chosenone))
      chosen=chosen+1

  await messagedata.reply(message2send)
  message = await interaction.followup.send("Done", ephemeral=False)
  await message.delete()




@tree.command(name="giveawaytracking", description = "Giveaway channel tracking", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, role: discord.Role, channel: str):
  await interaction.response.defer()
  channel = channel.split()
  channel = channel[0]

  if (str(channel[:2]) == "<#"):
    download_file('/giveawaychanneldoc.txt', 'giveawaychanneldocument.txt')
    download_file('/giveawayroledoc.txt', 'giveawayroledocument.txt')
    
    channel = channel[2:-1]
    role = role.id
    f = open('giveawayroledocument.txt', 'a')
    f.write(str(role) + ",")
    f.close()

    g = open('giveawaychanneldocument.txt', 'a')
    g.write(str(channel) + ',')
    g.close()

    upload_file('/giveawaychanneldoc.txt', 'giveawaychanneldocument.txt')
    upload_file('/giveawayroledoc.txt', 'giveawayroledocument.txt')
    await interaction.followup.send("Tracking updated")
  else:
    await interaction.followup.send("Incorrect value inputted for channel please use '#General' for example")
    
    
  





@tree.command(name="giveaway_winner", description = "Picks a random winner from the role chosen [won't include gardeners]", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, role: discord.Role):
  await interaction.response.defer()
  try:
    server = interaction.guild
    guild=interaction.guild
    role_name = discord.utils.get(guild.roles,id=int(role.id))
    role_name = str(role_name)
    i = 0
    role_id = server.roles[0]
    display_names = []
    member_ids = []
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break

    else:
        await interaction.followup.send("Role doesn't exist")
        return
    for member in server.members:
        if role_id in member.roles:
            i = i + 1
            valoscoreboardadder(member.display_name,member.id, -1, i)
            display_names.append(member.display_name)
            member_ids.append(member.id)
    if (i == 0):
        await interaction.followup.send("No one was found in that role!")

    picked=0
    gardeners =[204923365205475329, 293360731867316225, 165146318954692608, 389454049528774662, 492549065041510403, 183707605032501248, 172360818715918337, 141651693694746624, 754724309276164159, 332438787588227072, 530121845760851968]
    value = random.choice(member_ids)
    while(picked==0):
      value = random.choice(member_ids)
      if(int(value) in gardeners):
        print("Is a gardener")
      else:
        picked=1
   
    await interaction.followup.send("The giveaway winner is - <@" + str(value) + ">")
  except:
    print("error")


@tree.command(name="valoremove", description = "Remove 1 point from the Valorant scoreboard", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, role: discord.Role):
  await interaction.response.defer()
  download_file('/valoscoreboard.csv', 'scoreboard8.csv')
  try:
    server = interaction.guild
    guild=interaction.guild
    role_name = discord.utils.get(guild.roles,id=int(role.id))
    role_name = str(role_name)
    i = 0
    role_id = server.roles[0]
    display_names = []
    member_ids = []
    file = open("filetosend.txt", "w")
    file.close()
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break
    else:
        await interaction.followup.send("Role doesn't exist")
        return
    for member in server.members:
        if role_id in member.roles:
            i = i + 1
            valoscoreboardadder(member.display_name,member.id, -1, i)
            display_names.append(member.display_name)
            member_ids.append(member.id)
    if (i == 0):
        await interaction.followup.send("No one was found in that role!")
    else:
        upload_file('/valoscoreboard.csv', 'scoreboard9.csv')
        await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
  except:
    await interaction.followup.send("You need to tag the winning role: example /valoremove @V9-0")




@tree.command(name="csgoremove", description = "Remove 1 point from the CSGO scoreboard", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, role: discord.Role):
  await interaction.response.defer()
  download_file('/csgoscoreboard.csv', 'scoreboard2.csv')
  try:
    server = interaction.guild
    guild=interaction.guild
    role_name = discord.utils.get(guild.roles,id=int(role.id))
    role_name = str(role_name)
    i = 0
    role_id = server.roles[0]
    display_names = []
    member_ids = []
    file = open("filetosend.txt", "w")
    file.close()
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break
    else:
        await interaction.followup.send("Role doesn't exist")
        return
    for member in server.members:
        if role_id in member.roles:
            i = i + 1
            scoreboardadder(member.display_name, member.id,-1, i)
            display_names.append(member.display_name)
            member_ids.append(member.id)
    if (i == 0):
        await interaction.followup.send("No one was found in that role!")
    else:
        upload_file('/csgoscoreboard.csv', 'scoreboard3.csv')
        await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
  except:
    await interaction.followup.send("You need to tag the winning role: example /csgoremove @cs9-0")




@tree.command(name="vctremove", description = "Remove 1 point from the VCT scoreboard", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, role: discord.Role):
  await interaction.response.defer()
  download_file('/vctscoreboard.csv', 'scoreboard2.csv')
  try:
    server = interaction.guild
    guild=interaction.guild
    role_name = discord.utils.get(guild.roles,id=int(role.id))
    role_name = str(role_name)
    i = 0
    role_id = server.roles[0]
    display_names = []
    member_ids = []
    file = open("filetosend.txt", "w")
    file.close()
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break
    else:
        await interaction.followup.send("Role doesn't exist")
        return
    for member in server.members:
        if role_id in member.roles:
            i = i + 1
            vctscoreboardadder(member.display_name, member.id,-1, i)
            display_names.append(member.display_name)
            member_ids.append(member.id)
    if (i == 0):
        await interaction.followup.send("No one was found in that role!")
    else:
        upload_file('/vctscoreboard.csv', 'scoreboard3.csv')
        await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
  except:
    await interaction.followup.send("You need to tag the winning role: example /vctremove @cs9-0")




@tree3.command(name="valovctwinner", description = "Picks the winner", guild = discord.Object(id = IDForServer3))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  list=[98468521951924224, 312656577045987328, 212512241076011008]
  winner = random.choice(list)
  await interaction.followup.send("The winner of the VCT prediction game is - <@" + str(winner) + ">")




@tree3.command(name="vctremove", description = "Remove 1 point from the VCT scoreboard", guild = discord.Object(id = IDForServer3))
async def self(interaction: discord.Interaction, role: discord.Role):
  await interaction.response.defer()
  download_file('/ldnvctscoreboard.csv', 'scoreboard2.csv')
  try:
    server = interaction.guild
    guild=interaction.guild
    role_name = discord.utils.get(guild.roles,id=int(role.id))
    role_name = str(role_name)
    i = 0
    role_id = server.roles[0]
    display_names = []
    member_ids = []
    file = open("filetosend.txt", "w")
    file.close()
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break
    else:
        await interaction.followup.send("Role doesn't exist")
        return
    for member in server.members:
        if role_id in member.roles:
            i = i + 1
            ldnvctscoreboardadder(member.display_name, member.id,-1, i)
            display_names.append(member.display_name)
            member_ids.append(member.id)
    if (i == 0):
        await interaction.followup.send("No one was found in that role!")
    else:
        upload_file('/ldnvctscoreboard.csv', 'scoreboard3.csv')
        await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
  except:
    await interaction.followup.send("You need to tag the winning role: example /vctremove @cs9-0")





@tree.command(name="dotaremove", description = "Remove 1 point from the Dota scoreboard", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, role: discord.Role):
  await interaction.response.defer()
  download_file('/dotascoreboard.csv', 'scoreboard45.csv')
  try:
    server = interaction.guild
    guild = interaction.guild
    role_name = discord.utils.get(guild.roles,id=int(role.id))
    role_name = str(role_name)
    i = 0
    role_id = server.roles[0]
    display_names = []
    member_ids = []
    file = open("filetosend.txt", "w")
    file.close()
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break
    else:
        await interaction.followup.send(("Role doesn't exist"))
        return
    for member in server.members:
        if role_id in member.roles:
            i = i + 1
            dotascoreboardadder(member.display_name,member.id, -1, i)
            display_names.append(member.display_name)
            member_ids.append(member.id)
    if (i == 0):
        await interaction.followup.send("No one was found in that role!")
    else:
        upload_file('/dotascoreboard.csv', 'scoreboard46.csv')
        await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
  except:
    await interaction.followup.send("You need to tag the winning role: example /dotaremove @D9-0")




@tree5.command(name="dotaremove", description = "Remove 1 point from the Dota scoreboard", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction, role: discord.Role):
  await interaction.response.defer()
  tundradownload_file('/dotascoreboard.csv', 'scoreboard25.csv')
  try:
    server = interaction.guild
    guild = interaction.guild
    role_name = discord.utils.get(guild.roles,id=int(role.id))
    role_name = str(role_name)
    i = 0
    role_id = server.roles[0]
    display_names = []
    member_ids = []
    file = open("filetosend.txt", "w")
    file.close()
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break
    else:
        await interaction.followup.send(("Role doesn't exist"))
        return
    for member in server.members:
        if role_id in member.roles:
            i = i + 1
            tundradotascoreboardadder(member.display_name,member.id, -1, i)
            display_names.append(member.display_name)
            member_ids.append(member.id)
    if (i == 0):
        await interaction.followup.send("No one was found in that role!")
    else:
        tundraupload_file('/dotascoreboard.csv', 'scoreboard26.csv')
        await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
  except:
    await interaction.followup.send("You need to tag the winning role: example /dotaremove @D9-0")







@tree.command(name="deletereminder", description = "Delete 1 of your reminders - use /myreminders to get a list", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, remindertodelete: int):
  await interaction.response.defer()
  data = download_file('/dropreminders.txt', 'reminders.txt')
  a_file = open("reminders.txt", "r")
  list_of_lines = a_file.readlines()

  remindertodelete = remindertodelete
  author = interaction.user.id

  i = 0
  j = 1
  k = 0
  datatosave = []
  try:
      while (i < len(list_of_lines)):
          reminderdata = list_of_lines[i]
          remindersplitup = reminderdata.rsplit(", ")
          text = remindersplitup[0]
          text = text.strip()
          checksent = remindersplitup[len(remindersplitup) - 1]
          checksent = checksent.strip()

          if (text == str(author) and checksent != "sent"):
              if (j == int(remindertodelete)):
                  print("we are here")
                  user = remindersplitup[0]

                  channel = remindersplitup[1]
                  reminder = remindersplitup[2]
                  timetosend = remindersplitup[3]
                  issent = "sent"
                  remindersaved = reminder + ", to be sent on - " + timetosend
                  linetosave = user + ", " + channel + ", " + reminder + ", " + timetosend + ", " + issent + "\n"
                  embed = discord.Embed(title="Reminder removed",
                                        color=0x55a7f7)
                  embed.add_field(name="The deleted reminder",
                                  value=remindersaved,
                                  inline=True)
                  datatosave.append(linetosave)
                  j = j + 1
                  k = k + 1
              else:
                  datatosave.append(reminderdata)
                  print(j)
                  j = j + 1
          else:
              datatosave.append(reminderdata)
          i = i + 1

      a_file = open("reminders.txt", "w")
      a_file.writelines(datatosave)
      a_file.close()
      upload_file('/dropreminders.txt', 'reminders.txt')
      if (k != 0):
          await interaction.followup.send(embed=embed)
      else:
          embed = discord.Embed(title="Reminder deletion error",
                                color=0x55a7f7)
          embed.add_field(
              name="Suggestion",
              value=
              "To use this find your reminders via /myreminders, and choose the reminder based on the value to the left of your reminder!\n E.G - /deletereminder 1",
              inline=True)
          await interaction.followup.send(embed=embed)
  except:
      embed = discord.Embed(title="Reminder deletion error",
                            color=0x55a7f7)
      embed.add_field(
          name="Suggestion",
          value=
          "To use this find your reminders via /myreminders, and choose the reminder based on the value to the left of your reminder!\n E.G - /deletereminder 1",
          inline=True)
      await interaction.followup.send(embed=embed)







@tree.command(name="myreminders", description = "Get a list of your reminders", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  data = download_file('/dropreminders.txt', 'reminders.txt')
  a_file = open("reminders.txt", "r")
  list_of_lines = a_file.readlines()
  i = 0
  userID = interaction.user.id
  userID = str(userID)

  reminders = []
  timeofreminders = []
  dayofreminding = []
  monthofreminding = []
  yearofreminding = []
  timetosendreminder = []
  channeltosend = []
  while (i < len(list_of_lines)):
      base_reminder = list_of_lines[i]
      splitUpValues = base_reminder.rsplit(", ")
      checkIfSent = splitUpValues[4]
      dateOfSend = splitUpValues[3]
      textofreminder = splitUpValues[2]
      channelToSend = splitUpValues[1]
      userToSend = splitUpValues[0]
      checkifSent = checkIfSent[0:2]

      dateofremindbsplit = dateOfSend.rsplit(" ")
      datesplitup = dateofremindbsplit[0].rsplit("-")
      dayofreminder = datesplitup[2]
      monthofsend = datesplitup[1]
      yearofsend = datesplitup[0]
      timeofsend = dateofremindbsplit[1]

      if (checkifSent == "no"):
          if (userID == str(userToSend)):
              reminders.append(textofreminder)
              timeofreminders.append(dateOfSend)
              dayofreminding.append(dayofreminder)
              monthofreminding.append(monthofsend)
              yearofreminding.append(yearofsend)
              timetosendreminder.append(timeofsend)
              channeltosend.append(channelToSend)

      i = i + 1
  j = 0
  textToSend = ""
  if (len(reminders) > 0):
      while (j < len(reminders)):
          textToSend = textToSend + str(
              j + 1) + " - " + reminders[j] + " - " + str(
                  dayofreminding[j]
              ) + "/" + str(monthofreminding[j]) + "/" + str(
                  yearofreminding[j]) + " at " + str(
                      timetosendreminder[j]) + " UTC - <#" + str(
                          channeltosend[j]) + ">\n"
          #textToSend = textToSend + reminders[j] + " - " + timeofreminders[j] + "\n"
          j = j + 1

      embed = discord.Embed(
          title="Your currently saved reminders", color=0x55a7f7)
      embed.add_field(name="Reminders",
                      value=textToSend,
                      inline=True)

      embed.add_field(
          name="Note",
          value=
          "If you see #deleted-channel, you are unable to access the channel tagged / or it is deleted",
          inline=False)

      await interaction.followup.send(embed=embed)

  else:
      await interaction.followup.send("You currently have no saved reminders")


@tree.command(name="valoadd", description = "Add 1 point to the Valo scoreboard", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, role: discord.Role, points_to_add: typing.Optional[int]):
  await interaction.response.defer()
  download_file('/valoscoreboard.csv', 'scoreboard8.csv')
  if(str(points_to_add) == "None"):
    try:
      server = interaction.guild
      guild=interaction.guild
      role_name = discord.utils.get(guild.roles,id=int(role.id))
      role_name = str(role_name)
      i = 0
      role_id = server.roles[0]
      display_names = []
      member_ids = []
      file = open("filetosend.txt", "w")
      file.close()
      for role in server.roles:
          if role_name == role.name:
              role_id = role
              break
      else:
          await interaction.followup.send("Role doesn't exist")
          return
      for member in server.members:
          if role_id in member.roles:
              i = i + 1
              valoscoreboardadder(member.display_name,member.id, 1, i)
              display_names.append(member.display_name)
              member_ids.append(member.id)
      if (i == 0):
          await interaction.followup.send("No one was found in that role!")
      else:
          upload_file('/valoscoreboard.csv', 'scoreboard9.csv')
          await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
    except:
      await interaction.followup.send("You need to tag the winning role: example /valoadd @v9-0")
  else:
    try:
      server = interaction.guild
      guild=interaction.guild
      role_name = discord.utils.get(guild.roles,id=int(role.id))
      role_name = str(role_name)
      i = 0
      role_id = server.roles[0]
      display_names = []
      member_ids = []
      file = open("filetosend.txt", "w")
      file.close()
      for role in server.roles:
          if role_name == role.name:
              role_id = role
              break
      else:
          await interaction.followup.send("Role doesn't exist")
          return
      for member in server.members:
          if role_id in member.roles:
              i = i + 1
              valoscoreboardadder(member.display_name,member.id, points_to_add, i)
              display_names.append(member.display_name)
              member_ids.append(member.id)
      if (i == 0):
          await interaction.followup.send("No one was found in that role!")
      else:
          upload_file('/valoscoreboard.csv', 'scoreboard9.csv')
          await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
    except:
      await interaction.followup.send("You need to tag the winning role: example /valoadd @v9-0")


@tree.command(name="csgoadd", description = "Add 1 point to the CSGO scoreboard", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, role: discord.Role, points_to_add: typing.Optional[int]):
  await interaction.response.defer()
  download_file('/csgoscoreboard.csv', 'scoreboard2.csv')
  if(str(points_to_add)=="None"):
    try:
      server = interaction.guild
      guild=interaction.guild
      role_name = discord.utils.get(guild.roles,id=int(role.id))
      role_name = str(role_name)
      i = 0
      role_id = server.roles[0]
      display_names = []
      member_ids = []
      file = open("filetosend.txt", "w")
      file.close()
      for role in server.roles:
          if role_name == role.name:
              role_id = role
              break
      else:
          await interaction.followup.send("Role doesn't exist")
          return
      for member in server.members:
          if role_id in member.roles:
              i = i + 1
              scoreboardadder(member.display_name, member.id, 1, i)
              display_names.append(member.display_name)
              member_ids.append(member.id)
      if (i == 0):
          await interaction.followup.send("No one was found in that role!")
      else:
          upload_file('/csgoscoreboard.csv', 'scoreboard3.csv')
          await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
    except:
      await interaction.followup.send("You need to tag the winning role: example /csgoadd @cs9-0")
  else:
    try:
      server = interaction.guild
      guild=interaction.guild
      role_name = discord.utils.get(guild.roles,id=int(role.id))
      role_name = str(role_name)
      i = 0
      role_id = server.roles[0]
      display_names = []
      member_ids = []
      file = open("filetosend.txt", "w")
      file.close()
      for role in server.roles:
          if role_name == role.name:
              role_id = role
              break
      else:
          await interaction.followup.send("Role doesn't exist")
          return
      for member in server.members:
          if role_id in member.roles:
              i = i + 1
              scoreboardadder(member.display_name, member.id, points_to_add, i)
              display_names.append(member.display_name)
              member_ids.append(member.id)
      if (i == 0):
          await interaction.followup.send("No one was found in that role!")
      else:
          upload_file('/csgoscoreboard.csv', 'scoreboard3.csv')
          await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
    except:
      await interaction.followup.send("You need to tag the winning role: example /csgoadd @cs9-0")






@tree.command(name="vctadd", description = "Add 1 point to the VCT scoreboard", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, role: discord.Role):
  await interaction.response.defer()
  download_file('/vctscoreboard.csv', 'scoreboard2.csv')
  try:
    server = interaction.guild
    guild=interaction.guild
    role_name = discord.utils.get(guild.roles,id=int(role.id))
    role_name = str(role_name)
    i = 0
    role_id = server.roles[0]
    display_names = []
    member_ids = []
    file = open("filetosend.txt", "w")
    file.close()
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break
    else:
        await interaction.followup.send("Role doesn't exist")
        return
    for member in server.members:
        if role_id in member.roles:
            i = i + 1
            vctscoreboardadder(member.display_name, member.id, 1, i)
            display_names.append(member.display_name)
            member_ids.append(member.id)
    if (i == 0):
        await interaction.followup.send("No one was found in that role!")
    else:
        upload_file('/vctscoreboard.csv', 'scoreboard3.csv')
        await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
  except:
    await interaction.followup.send("You need to tag the winning role: example /vctadd @cs9-0")





@tree3.command(name="vctadd", description = "Add 1 point to the VCT scoreboard", guild = discord.Object(id = IDForServer3))
async def self(interaction: discord.Interaction, role: discord.Role):
  await interaction.response.defer()
  download_file('/ldnvctscoreboard.csv', 'scoreboard2.csv')
  try:
    server = interaction.guild
    guild=interaction.guild
    role_name = discord.utils.get(guild.roles,id=int(role.id))
    role_name = str(role_name)
    i = 0
    role_id = server.roles[0]
    display_names = []
    member_ids = []
    file = open("filetosend.txt", "w")
    file.close()
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break
    else:
        await interaction.followup.send("Role doesn't exist")
        return
    for member in server.members:
        if role_id in member.roles:
            i = i + 1
            ldnvctscoreboardadder(member.display_name, member.id, 1, i)
            display_names.append(member.display_name)
            member_ids.append(member.id)
    if (i == 0):
        await interaction.followup.send("No one was found in that role!")
    else:
        upload_file('/ldnvctscoreboard.csv', 'scoreboard3.csv')
        await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
  except:
    await interaction.followup.send("You need to tag the winning role: example /vctadd @cs9-0")

@tree5.command(name="dotaadd", description = "Add 1 point to the Dota scoreboard", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction, role: discord.Role, points_to_add: typing.Optional[int]):
  if(str(points_to_add)=="None"):
    await interaction.response.defer()
    try:
      tundradownload_file('/dotascoreboard.csv', 'scoreboard25.csv')
      guild = interaction.guild
      server = interaction.guild
      role_name = discord.utils.get(guild.roles, id=int(role.id))
      role_name = str(role_name)
      i = 0
      role_id = server.roles[0]
      display_names = []
      member_ids = []
      file = open("filetosend.txt", "w")
      file.close()
      for role in server.roles:
          if role_name == role.name:
              role_id = role
              break
      else:
          await interaction.followup.send("Role doesn't exist")
          return
      for member in server.members:
          if role_id in member.roles:
              i = i + 1
              tundradotascoreboardadder(member.display_name,member.id, 1, i)
              display_names.append(member.display_name)
              member_ids.append(member.id)
      if (i == 0):
          await interaction.followup.send("No one was found in that role!")
      else:
        tundraupload_file('/dotascoreboard.csv', 'scoreboard26.csv')
        await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
    except:
      await interaction.followup.send("You need to tag the winning role: example /dotaadd @D9-0" )
  else:
    await interaction.response.defer()
    try:
      guild = interaction.guild
      server = interaction.guild
      role_name = discord.utils.get(guild.roles, id=int(role.id))
      role_name = str(role_name)
      i = 0
      role_id = server.roles[0]
      display_names = []
      member_ids = []
      file = open("filetosend.txt", "w")
      file.close()
      for role in server.roles:
          if role_name == role.name:
              role_id = role
              break
      else:
          await interaction.followup.send("Role doesn't exist")
          return
      for member in server.members:
          if role_id in member.roles:
              i = i + 1
              tundradotascoreboardadder(member.display_name,member.id, points_to_add, i)
              display_names.append(member.display_name)
              member_ids.append(member.id)
      if (i == 0):
          await interaction.followup.send("No one was found in that role!")
      else:
        tundraupload_file('/dotascoreboard.csv', 'scoreboard26.csv')
        await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
    except:
      await interaction.followup.send("You need to tag the winning role: example /dotaadd @D9-0" )








@tree5.command(name="fifaadd", description = "Add 1 point to the Fifa scoreboard", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction, role: discord.Role, points_to_add: typing.Optional[int]):
  if(str(points_to_add)=="None"):
    await interaction.response.defer()
    try:
      guild = interaction.guild
      server = interaction.guild
      role_name = discord.utils.get(guild.roles, id=int(role.id))
      role_name = str(role_name)
      i = 0
      role_id = server.roles[0]
      display_names = []
      member_ids = []
      file = open("filetosend.txt", "w")
      file.close()
      for role in server.roles:
          if role_name == role.name:
              role_id = role
              break
      else:
          await interaction.followup.send("Role doesn't exist")
          return
      for member in server.members:
          if role_id in member.roles:
              i = i + 1
              tundrafifascoreboardadder(member.display_name,member.id, 1, i)
              display_names.append(member.display_name)
              member_ids.append(member.id)
      if (i == 0):
          await interaction.followup.send("No one was found in that role!")
      else:
        tundraupload_file('/fifascoreboard.csv', 'scoreboard22.csv')
        await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
    except:
      await interaction.followup.send("You need to tag the winning role: example /fifaadd @D9-0" )
  else:
    await interaction.response.defer()
    try:
      guild = interaction.guild
      server = interaction.guild
      role_name = discord.utils.get(guild.roles, id=int(role.id))
      role_name = str(role_name)
      i = 0
      role_id = server.roles[0]
      display_names = []
      member_ids = []
      file = open("filetosend.txt", "w")
      file.close()
      for role in server.roles:
          if role_name == role.name:
              role_id = role
              break
      else:
          await interaction.followup.send("Role doesn't exist")
          return
      for member in server.members:
          if role_id in member.roles:
              i = i + 1
              tundrafifascoreboardadder(member.display_name,member.id, points_to_add, i)
              display_names.append(member.display_name)
              member_ids.append(member.id)
      if (i == 0):
          await interaction.followup.send("No one was found in that role!")
      else:
        tundraupload_file('/fifascoreboard.csv', 'scoreboard22.csv')
        await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
    except:
      await interaction.followup.send("You need to tag the winning role: example /fifaadd @D9-0" )









@tree.command(name="dotaadd", description = "Add 1 point to the Dota scoreboard", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, role: discord.Role, points_to_add: typing.Optional[int]):
  if(str(points_to_add)=="None"):
    await interaction.response.defer()
    try:
      guild = interaction.guild
      server = interaction.guild
      role_name = discord.utils.get(guild.roles, id=int(role.id))
      role_name = str(role_name)
      i = 0
      role_id = server.roles[0]
      display_names = []
      member_ids = []
      file = open("filetosend.txt", "w")
      file.close()
      download_file('/dotascoreboard.csv', 'scoreboard45.csv')
      for role in server.roles:
          if role_name == role.name:
              role_id = role
              break
      else:
          await interaction.followup.send("Role doesn't exist")
          return
      for member in server.members:
          if role_id in member.roles:
              i = i + 1
              dotascoreboardadder(member.display_name,member.id, 1, i)
              display_names.append(member.display_name)
              member_ids.append(member.id)
      if (i == 0):
          await interaction.followup.send("No one was found in that role!")
      else:
        upload_file('/dotascoreboard.csv', 'scoreboard46.csv')
        await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
    except:
      await interaction.followup.send("You need to tag the winning role: example /dotaadd @D9-0" )
  else:
    await interaction.response.defer()
    try:
      guild = interaction.guild
      server = interaction.guild
      role_name = discord.utils.get(guild.roles, id=int(role.id))
      role_name = str(role_name)
      i = 0
      role_id = server.roles[0]
      display_names = []
      member_ids = []
      file = open("filetosend.txt", "w")
      file.close()
      for role in server.roles:
          if role_name == role.name:
              role_id = role
              break
      else:
          await interaction.followup.send("Role doesn't exist")
          return
      for member in server.members:
          if role_id in member.roles:
              i = i + 1
              dotascoreboardadder(member.display_name,member.id, points_to_add, i)
              display_names.append(member.display_name)
              member_ids.append(member.id)
      if (i == 0):
          await interaction.followup.send("No one was found in that role!")
      else:
        upload_file('/dotascoreboard.csv', 'scoreboard46.csv')
        await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
    except:
      await interaction.followup.send("You need to tag the winning role: example /dotaadd @D9-0" )


@tree.command(name="clearvaloldnevent", description = "This will clear the event file for Valo LDN", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  f = open("valoevent.txt", "w")
  f.write("empty")
  f.close()
  upload_file('/valoldnevent.txt', 'valoldnevent.txt')
  await interaction.followup.send("Event cleared")



@tree.command(name="cleardotaevent", description = "This will clear the event file for Dota", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  f = open("dotaevent.txt", "w")
  f.write("empty")
  f.close()
  upload_file('/dotaevent.txt', 'dotaevent.txt')
  await interaction.followup.send("Event cleared")


@tree5.command(name="cleardotaevent", description = "This will clear the event file for Dota", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  f = open("dotaevent.txt", "w")
  f.write("empty")
  f.close()
  tundraupload_file('/dotaevent.txt', 'dotaevent.txt')
  await interaction.followup.send("Event cleared")


@tree.command(name="clearcsgoevent", description = "This will clear the event file for CSGO", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  f = open("csgoevent.txt", "w")
  f.write("empty")
  f.close()
  upload_file('/csgoevent.txt', 'csgoevent.txt')
  await interaction.followup.send("Event cleared")

@tree.command(name="clearcsgoboard", description = "This will clear the CSGO leaderboard", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  scoreboarding()
  await interaction.followup.send("The CSGO Leaderboard is reset")


@tree.command(name="clearvctboard", description = "This will clear the VCT leaderboard", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  vctscoreboarding()
  await interaction.followup.send("The VCT Leaderboard is reset")



@tree3.command(name="clearvctboard", description = "This will clear the VCT leaderboard", guild = discord.Object(id = IDForServer3))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  ldnvctscoreboarding()
  await interaction.followup.send("The VCT Leaderboard is reset")




@tree.command(name="cleardotaboard", description = "This will clear the Dota leaderboard", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  dotascoreboarding()
  await interaction.followup.send("The Dota leaderboard has been reset")



@tree5.command(name="clearfifaboard", description = "This will clear the Fifa leaderboard", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  tundrafifascoreboarding()
  await interaction.followup.send("The Fifa leaderboard has been reset")



@tree5.command(name="cleardotaboard", description = "This will clear the Dota leaderboard", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  tundradotascoreboarding()
  await interaction.followup.send("The Dota leaderboard has been reset")


@tree.command(name="clearvaloboard", description = "This will clear the Dota leaderboard", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  valoscoreboarding()
  await interaction.followup.send("The Valorant leaderboard has been reset")

@tree.command(name="clearcsgoaevent", description = "This will clear the event file for CSGO Academy", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  f = open("csgoaevent.txt", "w")
  f.write("empty")
  f.close()
  upload_file('/csgoaevent.txt', 'csgoaevent.txt')
  await interaction.followup.send("Event cleared")




@tree.command(name="csgoadiscordevent", description = "Create a discord event for the next CSGO Academy game", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  guild = interaction.guild
  try:
    value = CSGOCheck(0, 'https://www.hltv.org/team/11672/og-academy#tab-matchesBox', False)
    teams = value[0]
    gamepage = value[4]
    tourniname = value[8]
    name = "CSGO Academy game: " + teams
    time=datetime.datetime.now().astimezone() + datetime.timedelta(seconds=int(value[7]))
    end_time = time+datetime.timedelta(minutes=10)
    streaminfo = CSGOStreams('https://www.hltv.org/team/11672/og-academy#tab-matchesBox')
    streamdata = streaminfo[3]
    description = tourniname + "\n" + streamdata + "\n:mega: https://twitter.com/OGcsgo\n"
    
    linetocheck= teams+","+gamepage
    lines= "empty"

    try:
    
      if lines[0] == linetocheck:
        await interaction.followup.send("Event has already been added")
        pass
      else:
        await guild.create_scheduled_event(name=name, description=description, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=gamepage)
        f = open("csgoaevent.txt", "w")
        f.write(linetocheck)
        f.close()
        upload_file('/csgoaevent.txt', 'csgoaevent.txt')
        await interaction.followup.send("Event made - you will need to share this in the event channel")
        
    except:
      await guild.create_scheduled_event(name=name, description=description, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=gamepage)
      f = open("csgoaevent.txt", "w")
      f.write(linetocheck)
      f.close()
      upload_file('/csgoaevent.txt', 'csgoaevent.txt')
      await interaction.followup.send("Event made - you will need to share this in the event channel")
      pass
   
  
   
  except Exception as e:
    await interaction.followup.send("An error was hit during this process - there may be no game available")
    print(e)



@tree.command(name="dotadiscordevent", description = "Create a discord event for the next Dota game", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  try:
    value = DotaCheck(0, False)
    Teams = value[1]
    guild = interaction.guild
    name = "Dota 2 game: " + Teams
    time=datetime.datetime.now().astimezone() + value[3]
    end_time=time+datetime.timedelta(minutes=10)
    linktogame = value[7]
    tourniname = value[6]
    streaminfo = DotaStreams()
    
    flagMessage = streaminfo[2]
    description = tourniname +"\n" + flagMessage + "\n:mega: https://twitter.com/OGesports\n"
    
    linetocheck = Teams+","+linktogame

    lines="empty"

    try:
      if lines[0] == linetocheck:
        await interaction.followup.send("Event has already been added")
        pass
      else:
        
        await guild.create_scheduled_event(name=name, description=description,privacy_level = discord.PrivacyLevel.guild_only, start_time=time, end_time=end_time,entity_type=discord.enums.EntityType(3), location=linktogame)
        f = open("dotaevent.txt", "w")
        f.write(linetocheck)
        f.close()
        upload_file('/dotaevent.txt', 'dotaevent.txt')
        await interaction.followup.send("Event made - you will need to share this in the event channel")
        
    except:
      await guild.create_scheduled_event(name=name, description=description,privacy_level = discord.PrivacyLevel.guild_only, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=linktogame)
      f = open("dotaevent.txt", "w")
      f.write(linetocheck)
      f.close()
      upload_file('/dotaevent.txt', 'dotaevent.txt')
      await interaction.followup.send("Event made - you will need to share this in the event channel")
      pass
    
  
    
  except Exception as e:
    await interaction.followup.send("An error was hit during this process")
    print(e)



@tree.command(name="lastdota", description = "Last Dota match stats", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  lastinfo = LastDota()
  Dateandtime1 = lastinfo[0]
  Dateandtime2 = lastinfo[1]
  Dateandtime3 = lastinfo[2]
  LastGameScore1 = lastinfo[3]
  LastGameEnemy1 = lastinfo[6]
  LastGameScore2 = lastinfo[4]
  LastGameEnemy2 = lastinfo[7]
  LastGameScore3 = lastinfo[5]
  LastGameEnemy3 = lastinfo[8]

  embed = discord.Embed(title="The last game OG Dota played",url='https://liquipedia.net/dota2/OG/Played_Matches',color=0xf10909)
  embed.add_field(name="Date / tournament", value=(Dateandtime1 + "\n" + Dateandtime2 + "\n" + Dateandtime3),inline=True)
  embed.add_field(name="Score",value=(("OG " + LastGameScore1 + " " + LastGameEnemy1) + "\n" + ("OG " + LastGameScore2 + " " + LastGameEnemy2) + "\n" +("OG " + LastGameScore3 + " " + LastGameEnemy3)),inline=True)
  await interaction.followup.send(embed=embed)

@tree.command(name="getuserlist", description = "Get the list of users in a role", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, role: discord.Role):
  await interaction.response.defer()
  guild = interaction.guild
  server = interaction.guild
  role_name = discord.utils.get(guild.roles,id=int(role.id))
  role_name = str(role_name)

  role_id = server.roles[0]
  display_names = []
  member_ids = []
  file = open("filetosend.txt", "w")
  file.close()
  for role in server.roles:
      if role_name == role.name:
          role_id = role
          break
  else:
      await interaction.followup.send("Role doesn't exist")
      return
  for member in server.members:
      if role_id in member.roles:
          display_names.append(member.display_name)
          member_ids.append(member.id)

  i = 0
  while (i < len(display_names)):
      f = open("filetosend.txt", "a")
      f.write("name: " + display_names[i] + " - their id number: " +str(member_ids[i]) + "\n")
      f.close
      i = i + 1

  j=0
  while(j < len(display_names)):
    f = open("filetosend.txt", "a")
    f.write("<@" + str(member_ids[j]) + ">, ")
    f.close
    j=j+1
  f = open("filetosend.txt", "r")
  print(f.read())
  await interaction.followup.send("Role returned: " + role_name + '!',file=discord.File("filetosend.txt"))



@tree.command(name="lastvaloldn", description = "Last Valorant LDN map stats", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  last_valo = lastvalo('https://www.vlr.gg/team/matches/8903/og-ldn-utd/?group=completed')
  await interaction.followup.send(last_valo)

@tree.command(name="lastcsgo", description = "Last CSGO map stats", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  last = lastcsgo('https://www.hltv.org/team/10503/og#tab-matchesBox')
  await interaction.followup.send(last)

@tree.command(name="lastcsgoa", description = "Last CSGO Academy map stats", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  last = lastcsgo('https://www.hltv.org/team/11672/og-academy#tab-matchesBox')
  await interaction.followup.send(last)

@tree.command(name="showdota", description = "Show the Dota Prediction leaderboard", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, user: typing.Optional[discord.User]):
  await interaction.response.defer()
  try:
    test = dotascoreboardsingle(user.id)
    await interaction.followup.send(test)
  except Exception as e :
    test = dotascoreboardreader("none")
    embed = discord.Embed(title="Dota 2 prediction leaderboard", color=0x55a7f7)
    embed.add_field(name="Dota 2 Prediction - page: " + str(test[2]) + "/" + str(test[1]),value="```\n" + test[0] + "\n```",inline=True)
    embed.add_field(name="Can't see yourself?",value="Can't see yourself on the table? use /show dota @*yourself* to see where you stand!",inline=False)
    await interaction.followup.send(embed=embed)



@tree5.command(name="showfifa", description = "Show the Fifa Prediction leaderboard", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction, user: typing.Optional[discord.User]):
  await interaction.response.defer()
  try:
    test = tundrafifascoreboardsingle(user.id)
    await interaction.followup.send(test)
  except Exception as e :
    test = tundrafifascoreboardreader("none")
    embed = discord.Embed(title="Dota 2 prediction leaderboard", color=0x55a7f7)
    embed.add_field(name="Dota 2 Prediction - page: " + str(test[2]) + "/" + str(test[1]),value="```\n" + test[0] + "\n```",inline=True)
    embed.add_field(name="Can't see yourself?",value="Can't see yourself on the table? use /show dota @*yourself* to see where you stand!",inline=False)
    await interaction.followup.send(embed=embed)
    


@tree5.command(name="showdota", description = "Show the Dota Prediction leaderboard", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction, user: typing.Optional[discord.User]):
  await interaction.response.defer()
  try:
    test = tundradotascoreboardsingle(user.id)
    await interaction.followup.send(test)
  except Exception as e :
    test = tundradotascoreboardreader("none")
    embed = discord.Embed(title="Dota 2 prediction leaderboard", color=0x55a7f7)
    embed.add_field(name="Dota 2 Prediction - page: " + str(test[2]) + "/" + str(test[1]),value="```\n" + test[0] + "\n```",inline=True)
    embed.add_field(name="Can't see yourself?",value="Can't see yourself on the table? use /show dota @*yourself* to see where you stand!",inline=False)
    await interaction.followup.send(embed=embed)





@tree.command(name="showcsgo", description = "Show the CSGO Prediction leaderboard", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, user: typing.Optional[discord.User]):

  await interaction.response.defer()
  try:
    test = scoreboardsingle(user.id)
    await interaction.followup.send(test)
    
  except:
    test = scoreboardreader("none")
    embed = discord.Embed(title="CSGO prediction leaderboard",color=0x55a7f7)
    embed.add_field(name="CSGO Prediction - page: " + str(test[2]) + "/" + str(test[1]),value="```\n" + test[0] + "\n```",inline=True)
    embed.add_field(name="Can't see yourself?",value="Can't see yourself on the table? use /show csgo @*yourself* to see where you stand!",inline=False)
    await interaction.followup.send(embed=embed)



@tree.command(name="showvct", description = "Show the VCT Prediction leaderboard", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, user: typing.Optional[discord.User]):

  await interaction.response.defer()
  try:
    test = vctscoreboardsingle(user.id)
    await interaction.followup.send(test)
    
  except:
    test = vctscoreboardreader("none")
    embed = discord.Embed(title="VCT prediction leaderboard",color=0x55a7f7)
    embed.add_field(name="VCT Prediction - page: " + str(test[2]) + "/" + str(test[1]),value="```\n" + test[0] + "\n```",inline=True)
    embed.add_field(name="Can't see yourself?",value="Can't see yourself on the table? use /show vct @*yourself* to see where you stand!",inline=False)
    await interaction.followup.send(embed=embed)




@tree3.command(name="showvct", description = "Show the VCT Prediction leaderboard", guild = discord.Object(id = IDForServer3))
async def self(interaction: discord.Interaction, user: typing.Optional[discord.User]):

  await interaction.response.defer()
  try:
    test = ldnvctscoreboardsingle(user.id)
    await interaction.followup.send(test)
    
  except:
    test = ldnvctscoreboardreader("none")
    embed = discord.Embed(title="VCT prediction leaderboard",color=0x55a7f7)
    embed.add_field(name="VCT Prediction - page: " + str(test[2]) + "/" + str(test[1]),value="```\n" + test[0] + "\n```",inline=True)
    embed.add_field(name="Can't see yourself?",value="Can't see yourself on the table? use /show vct @*yourself* to see where you stand!",inline=False)
    await interaction.followup.send(embed=embed)












@tree.command(name="showvalo", description = "Show the Valorant Prediction leaderboard", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, user: typing.Optional[discord.User]):
  await interaction.response.defer()
  try:
    test = valoscoreboardsingle(user.id)
    await interaction.followup.send(test)
  except:
    test = valoscoreboardreader("none")
    embed = discord.Embed(title="Valorant prediction leaderboard",color=0x55a7f7)
    embed.add_field(name="Valorant prediction - page: " + str(test[2]) + "/" + str(test[1]),value="```\n" + test[0] + "\n```",inline=True)
    embed.add_field(name="Can't see yourself?",value= "Can't see yourself on the table? use /show valo @*yourself* to see where you stand!",inline=False)
    await interaction.followup.send(embed=embed)





@tree5.command(name="discordstats", description = "Get the Discord Stats of yourself or a user", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction, ping: typing.Optional[discord.User]):
  await interaction.response.defer()
  try:
    user = ping
    createdon = user.created_at
    joinedon = user.joined_at
    cyear = createdon.year
    cmonth = createdon.month
    cday = createdon.day
    chour = createdon.hour
    cminute = createdon.minute
    csecond = createdon.second
    timecreation = str(cday) + "/" + str(cmonth) + "/" + str(
        cyear) + " - " + str(chour) + ":" + str(
            cminute) + ":" + str(csecond)

    jyear = joinedon.year
    jmonth = joinedon.month
    jday = joinedon.day
    jhour = joinedon.hour
    jminute = joinedon.minute
    jsecond = joinedon.second
    timejoining = str(jday) + "/" + str(jmonth) + "/" + str(jyear) + " - " + str(jhour) + ":" + str(jminute) + ":" + str(jsecond)
    if (str(user.id) == "733626039002988574"): 
      timejoining = " 11/12/2020 - 16:54"

    embed = discord.Embed(title="Account information of - " +str(user.display_name),color=0x55a7f7)
    embed.add_field(name="Account details",value="User account was created on - " +str(timecreation) +"\nJoined the server on- " +str(timejoining),inline=True)

    await interaction.followup.send(embed=embed)
  except:
    
    user = interaction.user
    createdon = user.created_at
    joinedon = user.joined_at
    cyear = createdon.year
    cmonth = createdon.month
    cday = createdon.day
    chour = createdon.hour
    cminute = createdon.minute
    csecond = createdon.second
    timecreation = str(cday) + "/" + str(cmonth) + "/" + str(cyear) + " - " + str(chour) + ":" + str(cminute) + ":" + str(csecond)
    jyear = joinedon.year
    jmonth = joinedon.month
    jday = joinedon.day
    jhour = joinedon.hour
    jminute = joinedon.minute
    jsecond = joinedon.second
    timejoining = str(jday) + "/" + str(jmonth) + "/" + str(jyear) + " - " + str(jhour) + ":" + str(jminute) + ":" + str(jsecond)
    if (str(user.id) == "733626039002988574"):
        timejoining = " 11/12/2020 - 16:54"

    embed = discord.Embed(title="Account information of - " +str(user.display_name),color=0x55a7f7)
    embed.add_field(name="Account details",value="User account was created on - " +str(timecreation) +"\nJoined the server on- " + str(timejoining),inline=True)
    await interaction.followup.send(embed=embed)




  

@tree.command(name="discordstats", description = "Get the Discord Stats of yourself or a user", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, ping: typing.Optional[discord.User]):
  await interaction.response.defer()
  try:
    user = ping
    createdon = user.created_at
    joinedon = user.joined_at
    cyear = createdon.year
    cmonth = createdon.month
    cday = createdon.day
    chour = createdon.hour
    cminute = createdon.minute
    csecond = createdon.second
    timecreation = str(cday) + "/" + str(cmonth) + "/" + str(
        cyear) + " - " + str(chour) + ":" + str(
            cminute) + ":" + str(csecond)

    jyear = joinedon.year
    jmonth = joinedon.month
    jday = joinedon.day
    jhour = joinedon.hour
    jminute = joinedon.minute
    jsecond = joinedon.second
    timejoining = str(jday) + "/" + str(jmonth) + "/" + str(jyear) + " - " + str(jhour) + ":" + str(jminute) + ":" + str(jsecond)
    if (str(user.id) == "733626039002988574"): 
      timejoining = " 11/12/2020 - 16:54"

    embed = discord.Embed(title="Account information of - " +str(user.display_name),color=0x55a7f7)
    embed.add_field(name="Account details",value="User account was created on - " +str(timecreation) +"\nJoined the server on- " +str(timejoining),inline=True)

    await interaction.followup.send(embed=embed)
  except:
    
    user = interaction.user
    createdon = user.created_at
    joinedon = user.joined_at
    cyear = createdon.year
    cmonth = createdon.month
    cday = createdon.day
    chour = createdon.hour
    cminute = createdon.minute
    csecond = createdon.second
    timecreation = str(cday) + "/" + str(cmonth) + "/" + str(cyear) + " - " + str(chour) + ":" + str(cminute) + ":" + str(csecond)
    jyear = joinedon.year
    jmonth = joinedon.month
    jday = joinedon.day
    jhour = joinedon.hour
    jminute = joinedon.minute
    jsecond = joinedon.second
    timejoining = str(jday) + "/" + str(jmonth) + "/" + str(jyear) + " - " + str(jhour) + ":" + str(jminute) + ":" + str(jsecond)
    if (str(user.id) == "733626039002988574"):
        timejoining = " 11/12/2020 - 16:54"

    embed = discord.Embed(title="Account information of - " +str(user.display_name),color=0x55a7f7)
    embed.add_field(name="Account details",value="User account was created on - " +str(timecreation) +"\nJoined the server on- " + str(timejoining),inline=True)
    await interaction.followup.send(embed=embed)

@tree5.command(name="nextdota", description="Get information on the next dota game", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  channelDataID = int(interaction.channel_id)
  userID = int(interaction.user.id)
  try:
    if(channelDataID in ShortList):
      embed = tundraDotaCheck(channelDataID, True)
    else:
      embed = tundraDotaCheck(channelDataID, False)
    embed = embed[0]
    if(channelDataID in ShortList):
        await interaction.followup.send(embed)
    else:
        await interaction.followup.send(embed=embed)
        #await message.reply(embed=embed)
  except:
    if(channelDataID in ShortList):
      #await message.reply("No games planned currently - For more information use /nextdota in <#721391448812945480>")
      await interaction.followup.send("No games planned currently - For more information use /nextdota in <#867689807214542899>")
    else:
      embed=discord.Embed(title="Tundra Dota's next game", url="https://liquipedia.net/dota2/Tundra_Esports", color=0xf10909)
      embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/8/85/Tundra_Esports_2020_full_lightmode.png/600px-Tundra_Esports_2020_full_lightmode.png")
      embed.add_field(name="Time remaining", value = "No games currently planned" , inline=False)
      embed.add_field(name="Notice",value="Please check Liquipedia by clicking the title of this embed for more information as the time might not be accurate", inline=False)
      embed.add_field(name="Links", value="Tundra Liquipedia: https://liquipedia.net/dota2/Tundra_Esports", inline=False)
      #await message.reply(embed=embed)
      await interaction.followup.send(embed=embed)




@tree.command(name="test2", description="test2", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  try:
    select = Select(placeholder="Choose a team!",
                   options=[
                     discord.SelectOption(label="OG", emoji="👀", description="Get dota game for the OG squad"),
                     discord.SelectOption(label="Ol'G", emoji="👴", description= "Get dota game for Ol'G squad")
                   ])

    async def my_callback(interaction):
      await interaction.response.defer()
      value = select.values[0]
      channelDataID = int(interaction.channel_id)
      if(value=="OG"):
        await client.http.delete_message(int(channelDataID), g.id)
        streaminfo = DotaStreams()
        Teams1 = streaminfo[0]
        Teams2 = streaminfo[1]
        flagMessage = streaminfo[2]
        convertedURL = streaminfo[3]
      
        if (Teams1 == "No games found"):
            embed = discord.Embed(title="No Dota streams / games were found",color=0xf10909)
            embed.add_field(name="What you can try",value="You can try using /nextdota / /nextdota2 to see if there are any games coming up",inline=True)
            embed.add_field(name="Links",value="https://liquipedia.net/dota2/OG",inline=False)
            await interaction.followup.send(embed=embed)
      
        else:
            embed = discord.Embed(title="Dota streams found!", color=0xf10909)
            embed.add_field(name="The game found",value=Teams1 + " vs " + Teams2,inline=True)
          
            if(interaction.channel_id != 689903856095723569 and interaction.channel_id != 926214194280419368 and interaction.channel_id != 1007303552445726750):
              embed.add_field(name="Streams / Flags",value="```" + flagMessage + "```",inline=False)
            embed.add_field(name="Streams available",value=flagMessage,inline=False)
            embed.add_field(name="Where I found the streams",value=convertedURL,inline=False)
            await interaction.followup.send(embed=embed)
      if(value=="Ol'G"):
        
        await client.http.delete_message(int(channelDataID), g.id)
        streaminfo = OldDotaStreams()
        Teams1 = streaminfo[0]
        Teams2 = streaminfo[1]
        flagMessage = streaminfo[2]
        convertedURL = streaminfo[3]
      
        if (Teams1 == "No games found"):
            embed = discord.Embed(title="No Dota streams / games were found",color=0xf10909)
            embed.add_field(name="What you can try",value="You can try using /nextdota to see if there are any games coming up",inline=True)
            embed.add_field(name="Links",value="https://liquipedia.net/dota2/OG",inline=False)
            await interaction.followup.send(embed=embed)
      
        else:
            embed = discord.Embed(title="Dota streams found!", color=0xf10909)
            embed.add_field(name="The game found",value=Teams1 + " vs " + Teams2,inline=True)
          
            if(interaction.channel_id != 689903856095723569 and interaction.channel_id != 926214194280419368 and interaction.channel_id != 1007303552445726750):
              embed.add_field(name="Streams / Flags",value="```" + flagMessage + "```",inline=False)
            embed.add_field(name="Streams available",value=flagMessage,inline=False)
            embed.add_field(name="Where I found the streams",value=convertedURL,inline=False)
            await interaction.followup.send(embed=embed)

    select.callback = my_callback
    view = View()
    view.add_item(select)
    
    g = await interaction.followup.send("Choose a squad", view=view)
    
  except Exception as e:
    print(e)


      

@tree.command(name="test", description="test", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  try:
    select = Select(placeholder="Choose a team!",
                   options=[
                     discord.SelectOption(label="OG", emoji="👀", description="Get dota game for the OG squad"),
                     discord.SelectOption(label="Ol'G", emoji="👴", description= "Get dota game for Ol'G squad")
                   ])

    async def my_callback(interaction):
      await interaction.response.defer()
      
      value = select.values[0]
      if(value == "OG"):
        
        channelDataID = int(interaction.channel_id)
        userID = int(interaction.user.id)
        try:
          await client.http.delete_message(int(channelDataID), g.id)
          if(channelDataID in ShortList):
            embed = DotaCheck(channelDataID, True)
          else:
            embed = DotaCheck(channelDataID, False)
          embed = embed[0]
          if(channelDataID in ShortList):
              await interaction.followup.send(embed)
          else:
              await interaction.followup.send(embed=embed)
              #await message.reply(embed=embed)
        except:
          if(channelDataID in ShortList):
            #await message.reply("No games planned currently - For more information use /nextdota in <#721391448812945480>")
            await interaction.followup.send("No games planned currently - For more information use /nextdota in <#721391448812945480>")
          else:
            embed=discord.Embed(title="OaG Dota's next game", url="https://liquipedia.net/dota2/OG", color=0xf10909)
            embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
            embed.add_field(name="Time remaining", value = "No games currently planned" , inline=False)
            embed.add_field(name="Notice",value="Please check Liquipedia by clicking the title of this embed for more information as the time might not be accurate", inline=False)
            embed.add_field(name="Links", value="OG Liquipedia: https://liquipedia.net/dota2/OG", inline=False)
            #await message.reply(embed=embed)
            await interaction.followup.send(embed=embed)
            
            
      if (value=="Ol'G"):
        
        channelDataID = int(interaction.channel_id)
        userID = int(interaction.user.id)
        try:
          await client.http.delete_message(int(channelDataID), g.id)
          if(channelDataID in ShortList):
            embed = OlGDotaCheck(channelDataID, True)
          else:
            embed = OlGDotaCheck(channelDataID, False)
          embed = embed[0]
          if(channelDataID in ShortList):
              await interaction.followup.send(embed)
          else:
              await interaction.followup.send(embed=embed)
              #await message.reply(embed=embed)
        except:
          if(channelDataID in ShortList):
            #await message.reply("No games planned currently - For more information use /nextdota in <#721391448812945480>")
            await interaction.followup.send("No games planned currently - For more information use /nextdota in <#721391448812945480>")
          else:
            embed=discord.Embed(title="Oal'G Dota's next game", url="https://liquipedia.net/dota2/OG", color=0xf10909)
            embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
            embed.add_field(name="Time remaining", value = "No games currently planned" , inline=False)
            embed.add_field(name="Notice",value="Please check Liquipedia by clicking the title of this embed for more information as the time might not be accurate", inline=False)
            embed.add_field(name="Links", value="Ol'GG Liquipedia: https://liquipedia.net/dota2/OG", inline=False)
            #await message.reply(embed=embed)
            await interaction.followup.send(embed=embed)
            
      
      

    select.callback = my_callback
    view = View()
    view.add_item(select)
    
    g = await interaction.followup.send("Choose a squad", view=view)
  except Exception as e:
    print(e)

@tree.command(name="nextdota", description="Get information on the next dota game", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  channelDataID = int(interaction.channel_id)
  userID = int(interaction.user.id)
  try:
    if(channelDataID in ShortList):
      embed = DotaCheck(channelDataID, True)
    else:
      embed = DotaCheck(channelDataID, False)
    embed = embed[0]
    if(channelDataID in ShortList):
        await interaction.followup.send(embed)
    else:
        await interaction.followup.send(embed=embed)
        #await message.reply(embed=embed)
  except:
    if(channelDataID in ShortList):
      #await message.reply("No games planned currently - For more information use /nextdota in <#721391448812945480>")
      await interaction.followup.send("No games planned currently - For more information use /nextdota in <#721391448812945480>")
    else:
      embed=discord.Embed(title="OG Dota's next game", url="https://liquipedia.net/dota2/OG", color=0xf10909)
      embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
      embed.add_field(name="Time remaining", value = "No games currently planned" , inline=False)
      embed.add_field(name="Notice",value="Please check Liquipedia by clicking the title of this embed for more information as the time might not be accurate", inline=False)
      embed.add_field(name="Links", value="OG Liquipedia: https://liquipedia.net/dota2/OG", inline=False)
      #await message.reply(embed=embed)
      await interaction.followup.send(embed=embed)








@tree.command(name="nextcsgo", description="Get information on the next CSGO game", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  channelDataID = int(interaction.channel_id)
  if(channelDataID in ShortList):
    CSGOGame = CSGOCheck(channelDataID, 'https://www.hltv.org/team/10503/og#tab-matchesBox', True)
  else:
    CSGOGame = CSGOCheck(channelDataID, 'https://www.hltv.org/team/10503/og#tab-matchesBox', False)
  embed = CSGOGame[6]
  if(channelDataID in ShortList):
      await interaction.followup.send(embed)
  else:
      await interaction.followup.send(embed=embed)

@tree.command(name="nextcsgoa", description="Get information on the next CSGO academy game", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  channelDataID = int(interaction.channel_id)
  if(channelDataID in ShortList):
    CSGOGame = CSGOCheck(channelDataID, 'https://www.hltv.org/team/11672/og-academy#tab-matchesBox', True)
  else:
    CSGOGame = CSGOCheck(channelDataID, 'https://www.hltv.org/team/11672/og-academy#tab-matchesBox', False)
  embed = CSGOGame[6]
  if(channelDataID in ShortList):
      await interaction.followup.send(embed)
  else:
      await interaction.followup.send(embed=embed)




@tree.command(name="nextvaloldn", description="Get information on the next Valorant LDN United game", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  channelDataID = int(interaction.channel_id)
  
  try:
    if(channelDataID in ShortList):
      embed = ValoCheck(channelDataID, 'https://www.vlr.gg/team/8903/og-ldn-utd', True)
      embed=embed[0]
    else:
      embed = ValoCheck(channelDataID, 'https://www.vlr.gg/team/8903/og-ldn-utd', False)
      embed=embed[0]
    

    if (embed == "N"):
        if (channelDataID in ShortList):
            await interaction.followup.send("No games planned currently - For more information use /nextvalo in <#721391448812945480>")
        else:
            embed = discord.Embed(title="OG LDN Valorant's next game",url="https://www.vlr.gg/team/8903/og-ldn-utd",color=0xd57280)
            embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
            embed.add_field(name="No games planned",value="No games planned",inline=True)
            embed.add_field(name="Links",value="[OG LDN VLR](https://www.vlr.gg/team/8903/og-ldn-utd) / [OG LDN Valrant Liquipedia](https://liquipedia.net/valorant/OG_LDN_UTD)",inline=False)
            await interaction.followup.send(embed=embed)
    else:
        if (channelDataID in ShortList):
            await interaction.followup.send(embed)
        else:
            await interaction.followup.send(embed=embed)
  except:

    if (channelDataID in ShortList):
      await interaction.followup.send("No games planned currently - For more information use /nextvalo in <#721391448812945480>")
    else:
          embed = discord.Embed(title="OG LDN Valorant's next game",url="https://www.vlr.gg/team/8903/og-ldn-utd",color=0xd57280)
          embed.set_thumbnail(url="https://liquipedia.net/commons/images/thumb/0/00/OG_RB_Logo.png/600px-OG_RB_Logo.png")
          embed.add_field(name="No games planned",value="No games planned",inline=True)
          embed.add_field(name="Links",value="[OG LDN VLR](https://www.vlr.gg/team/8903/og-ldn-utd) / [OG LDN Valorant Liquipedia](https://liquipedia.net/valorant/OG_LDN_UTD)",inline=False)
          await interaction.followup.send(embed=embed)

@tree.command(name="tiqualroles", description = "Create roles for TI qualifier predictions", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, team_count: int, prefix: str):
  await interaction.response.defer()
  guild = interaction.guild
  i=0
  while i< team_count:
    roletomake = prefix + "team-" + str(i+1)
    i=i+1
    await(guild.create_role(name=roletomake))
 
  await interaction.followup.send("I have created - " + str(team_count) + " roles, with prefix - " + prefix)

@tree.command(name="tiqualrolesdelete", description = "Delete roles for TI qualifier predictions", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, team_count: int, prefix: str):
  await interaction.response.defer()
  guild = interaction.guild
  i=0
  try:
    while(i<team_count):
      roletodelete = prefix + "team-"+str(i+1)
      role_object = discord.utils.get(guild.roles, name=roletodelete)
      await role_object.delete()
      i=i+1
  except Exception as e:
      print(e)
  
  
  await interaction.followup.send("I have deleted - " + str(i) + " roles, with prefix - " + prefix)


@tree3.command(name="teamroles", description = "Create roles for qualifier predictions", guild = discord.Object(id = IDForServer3))
async def self(interaction: discord.Interaction, team_count: int, prefix: str):
  await interaction.response.defer()
  guild = interaction.guild
  i=0
  while i< team_count:
    roletomake = prefix + "team-" + str(i+1)
    i=i+1
    await(guild.create_role(name=roletomake))
 
  await interaction.followup.send("I have created - " + str(team_count) + " roles, with prefix - " + prefix)




@tree3.command(name="teamrolesdelete", description = "Delete roles for TI qualifier predictions", guild = discord.Object(id = IDForServer3))
async def self(interaction: discord.Interaction, team_count: int, prefix: str):
  await interaction.response.defer()
  guild = interaction.guild
  i=0
  try:
    while(i<team_count):
      roletodelete = prefix + "team-"+str(i+1)
      role_object = discord.utils.get(guild.roles, name=roletodelete)
      await role_object.delete()
      i=i+1
  except Exception as e:
      print(e)
  
  
  await interaction.followup.send("I have created - " + str(i) + " roles, with prefix - " + prefix)



@tree5.command(name="dotabo", description = "Create Dota roles", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction, series_length: int):
  await interaction.response.defer()
  guild = interaction.guild
  isdone = 0
  if(series_length == 1):
    await guild.create_role(name="D1-0")
    await guild.create_role(name="D0-1")
    isdone=1
    await interaction.followup.send("I have created the roles for a Dota Bo1")
    
  if(series_length == 2):
    await guild.create_role(name="D2-0")
    await guild.create_role(name="D1-1")
    await guild.create_role(name="D0-2")
    isdone=1
    await interaction.followup.send("I have created the roles for a Dota Bo2")
    
  if(series_length==3):
    await guild.create_role(name="D2-0")
    await guild.create_role(name="D2-1")
    await guild.create_role(name="D1-2")
    await guild.create_role(name="D0-2")
    isdone=1
    await interaction.followup.send("I have created the roles for a Dota Bo3")
    
  if(series_length==5):
    await guild.create_role(name="D3-0")
    await guild.create_role(name="D3-2")
    await guild.create_role(name="D3-1")
    await guild.create_role(name="D1-3")
    await guild.create_role(name="D2-3")
    await guild.create_role(name="D0-3")
    isdone=1
    await interaction.followup.send("I have created the roles for a Dota Bo5")
    
  else:
    if(isdone== 0):
      await interaction.followup.send("Value for series length invalid, must be 1 / 2 / 3 / 5, please try again")
  


@tree5.command(name="fifabo", description = "Create Fifa roles", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction, series_length: int):
  await interaction.response.defer()
  guild = interaction.guild
  isdone = 0
  if(series_length == 1):
    await guild.create_role(name="F1-0")
    await guild.create_role(name="F0-1")
    isdone=1
    await interaction.followup.send("I have created the roles for a Fifa Bo1")
    
  if(series_length == 2):
    await guild.create_role(name="F2-0")
    await guild.create_role(name="F1-1")
    await guild.create_role(name="F0-2")
    isdone=1
    await interaction.followup.send("I have created the roles for a Fifa Bo2")
    
  if(series_length==3):
    await guild.create_role(name="F2-0")
    await guild.create_role(name="F2-1")
    await guild.create_role(name="F1-2")
    await guild.create_role(name="F0-2")
    isdone=1
    await interaction.followup.send("I have created the roles for a Fifa Bo3")
    
  if(series_length==5):
    await guild.create_role(name="F3-0")
    await guild.create_role(name="F3-2")
    await guild.create_role(name="F3-1")
    await guild.create_role(name="F1-3")
    await guild.create_role(name="F2-3")
    await guild.create_role(name="F0-3")
    isdone=1
    await interaction.followup.send("I have created the roles for a Fifa Bo5")
    
  else:
    if(isdone== 0):
      await interaction.followup.send("Value for series length invalid, must be 1 / 2 / 3 / 5, please try again")














@tree.command(name="dotabo", description = "Create Dota roles", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, series_length: int):
  await interaction.response.defer()
  guild = interaction.guild
  isdone = 0
  if(series_length == 1):
    await guild.create_role(name="D1-0")
    await guild.create_role(name="D0-1")
    isdone=1
    await interaction.followup.send("I have created the roles for a Dota Bo1")
    
  if(series_length == 2):
    await guild.create_role(name="D2-0")
    await guild.create_role(name="D1-1")
    await guild.create_role(name="D0-2")
    isdone=1
    await interaction.followup.send("I have created the roles for a Dota Bo2")
    
  if(series_length==3):
    await guild.create_role(name="D2-0")
    await guild.create_role(name="D2-1")
    await guild.create_role(name="D1-2")
    await guild.create_role(name="D0-2")
    isdone=1
    await interaction.followup.send("I have created the roles for a Dota Bo3")
    
  if(series_length==5):
    await guild.create_role(name="D3-0")
    await guild.create_role(name="D3-2")
    await guild.create_role(name="D3-1")
    await guild.create_role(name="D1-3")
    await guild.create_role(name="D2-3")
    await guild.create_role(name="D0-3")
    isdone=1
    await interaction.followup.send("I have created the roles for a Dota Bo5")
    
  else:
    if(isdone== 0):
      await interaction.followup.send("Value for series length invalid, must be 1 / 2 / 3 / 5, please try again")

@tree.command(name="csgobo", description = "Create CSGO roles", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, series_length: int):
  await interaction.response.defer()
  guild = interaction.guild
  isdone = 0
  if(series_length == 1):
    await guild.create_role(name="CS1-0")
    await guild.create_role(name="CS0-1")
    isdone=1
    await interaction.followup.send("I have created the roles for a CSGO Bo1")
    
  if(series_length == 2):
    await guild.create_role(name="CS2-0")
    await guild.create_role(name="CS1-1")
    await guild.create_role(name="CS0-2")
    isdone=1
    await interaction.followup.send("I have created the roles for a CSGO Bo2")
    
  if(series_length==3):
    await guild.create_role(name="CS2-0")
    await guild.create_role(name="CS2-1")
    await guild.create_role(name="CS1-2")
    await guild.create_role(name="CS0-2")
    isdone=1
    await interaction.followup.send("I have created the roles for a CSGO Bo3")
    
  if(series_length==5):
    await guild.create_role(name="CS3-0")
    await guild.create_role(name="CS3-2")
    await guild.create_role(name="CS3-1")
    await guild.create_role(name="CS1-3")
    await guild.create_role(name="CS2-3")
    await guild.create_role(name="CS0-3")
    isdone=1
    await interaction.followup.send("I have created the roles for a CSGO Bo5")
    
  else:
    if(isdone==0):
      await interaction.followup.send("Value for series length invalid, must be 1 / 2 / 3 / 5, please try again")


@tree.command(name="csgoabo", description = "Create CSGO Academy roles", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, series_length: int):
  await interaction.response.defer()
  guild = interaction.guild
  isdone = 0
  if(series_length == 1):
    await guild.create_role(name="CSA1-0")
    await guild.create_role(name="CSA0-1")
    isdone=1
    await interaction.followup.send("I have created the roles for a CSGO Academy Bo1")
    
  if(series_length == 2):
    await guild.create_role(name="CSA2-0")
    await guild.create_role(name="CSA1-1")
    await guild.create_role(name="CSA0-2")
    isdone=1
    await interaction.followup.send("I have created the roles for a CSGO Academy Bo2")
    
  if(series_length==3):
    await guild.create_role(name="CSA2-0")
    await guild.create_role(name="CSA2-1")
    await guild.create_role(name="CSA1-2")
    await guild.create_role(name="CSA0-2")
    isdone=1
    await interaction.followup.send("I have created the roles for a CSGO Academy Bo3")
    
  if(series_length==5):
    await guild.create_role(name="CSA3-0")
    await guild.create_role(name="CSA3-2")
    await guild.create_role(name="CSA3-1")
    await guild.create_role(name="CSA1-3")
    await guild.create_role(name="CSA2-3")
    await guild.create_role(name="CSA0-3")
    isdone=1
    await interaction.followup.send("I have created the roles for a CSGO Academy Bo5")
    
  else:
    if(isdone== 0):
      await interaction.followup.send("Value for series length invalid, must be 1 / 2 / 3 / 5, please try again")


@tree.command(name="valoldnbo", description = "Create Valorant LDN roles", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, series_length: int):
  await interaction.response.defer()
  guild = interaction.guild
  isdone = 0
  if(series_length == 1):
    await guild.create_role(name="VLDN1-0")
    await guild.create_role(name="VLDN0-1")
    isdone=1
    await interaction.followup.send("I have created the roles for a Valorant LDN Bo1")
    
  if(series_length == 2):
    await guild.create_role(name="VLDN2-0")
    await guild.create_role(name="VLDN1-1")
    await guild.create_role(name="VLDN0-2")
    isdone=1
    await interaction.followup.send("I have created the roles for a Valorant LDN Bo2")
    
  if(series_length==3):
    await guild.create_role(name="VLDN2-0")
    await guild.create_role(name="VLDN2-1")
    await guild.create_role(name="VLDN1-2")
    await guild.create_role(name="VLDN0-2")
    isdone=1
    await interaction.followup.send("I have created the roles for a Valorant LDN Bo3")
    
  if(series_length==5):
    await guild.create_role(name="VLDN3-0")
    await guild.create_role(name="VLDN3-2")
    await guild.create_role(name="VLDN3-1")
    await guild.create_role(name="VLDN1-3")
    await guild.create_role(name="VLDN2-3")
    await guild.create_role(name="VLDN0-3")
    isdone=1
    await interaction.followup.send("I have created the roles for a Valorant LDN Bo5")
    
  else:
    if(isdone== 0):
      await interaction.followup.send("Value for series length invalid, must be 1 / 2 / 3 / 5, please try again")

@tree.command(name="randombo", description = "Create Random roles", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, series_length: int):
  await interaction.response.defer()
  guild = interaction.guild
  isdone = 0
  if(series_length == 1):
    await guild.create_role(name="R1-0")
    await guild.create_role(name="R0-1")
    isdone=1
    await interaction.followup.send("I have created the roles for a Random Bo1")
    
  if(series_length == 2):
    await guild.create_role(name="R2-0")
    await guild.create_role(name="R1-1")
    await guild.create_role(name="R0-2")
    isdone=1
    await interaction.followup.send("I have created the roles for a Random Bo2")
    
  if(series_length==3):
    await guild.create_role(name="R2-0")
    await guild.create_role(name="R2-1")
    await guild.create_role(name="R1-2")
    await guild.create_role(name="R0-2")
    isdone=1
    await interaction.followup.send("I have created the roles for a Random Bo3")
    
  if(series_length==5):
    await guild.create_role(name="R3-0")
    await guild.create_role(name="R3-2")
    await guild.create_role(name="R3-1")
    await guild.create_role(name="R1-3")
    await guild.create_role(name="R2-3")
    await guild.create_role(name="R0-3")
    isdone=1
    await interaction.followup.send("I have created the roles for a Random Bo5")
    
  else:
    if(isdone== 0):
      await interaction.followup.send("Value for series length invalid, must be 1 / 2 / 3 / 5, please try again")
    







@tree.command(name="deletedotaroles", description = "Delete dota roles for prediction", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, series_length: int):
  await interaction.response.defer()
  guild = interaction.guild
  isdone=0
  if(series_length==1):
    role_object = discord.utils.get(guild.roles, name="D1-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D0-1")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Dota Bo1")
    isdone=1
  if(series_length==2):
    role_object = discord.utils.get(guild.roles, name="D2-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D1-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D0-2")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Dota Bo2")
    isdone=1
  if(series_length==3):
    role_object = discord.utils.get(guild.roles, name="D2-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D2-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D1-2")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D0-2")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Dota Bo3")
    isdone=1
  if(series_length==5):
    role_object = discord.utils.get(guild.roles, name="D3-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D3-2")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D3-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D1-3")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D2-3")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D0-3")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Dota Bo5")
    isdone=1
  else:
    if(isdone== 0):
      await interaction.followup.send("I was unable to delete any of the roles please verify series length - 1 / 2 / 3 / 5")
    
  

@tree5.command(name="deletedotaroles", description = "Delete dota roles for prediction", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction, series_length: int):
  await interaction.response.defer()
  guild = interaction.guild
  isdone=0
  if(series_length==1):
    role_object = discord.utils.get(guild.roles, name="D1-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D0-1")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Dota Bo1")
    isdone=1
  if(series_length==2):
    role_object = discord.utils.get(guild.roles, name="D2-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D1-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D0-2")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Dota Bo2")
    isdone=1
  if(series_length==3):
    role_object = discord.utils.get(guild.roles, name="D2-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D2-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D1-2")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D0-2")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Dota Bo3")
    isdone=1
  if(series_length==5):
    role_object = discord.utils.get(guild.roles, name="D3-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D3-2")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D3-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D1-3")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D2-3")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="D0-3")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Dota Bo5")
    isdone=1
  else:
    if(isdone== 0):
      await interaction.followup.send("I was unable to delete any of the roles please verify series length - 1 / 2 / 3 / 5")
    
  

@tree5.command(name="deletefifaroles", description = "Delete Fifa roles for prediction", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction, series_length: int):
  await interaction.response.defer()
  guild = interaction.guild
  isdone=0
  if(series_length==1):
    role_object = discord.utils.get(guild.roles, name="F1-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="F0-1")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Fifa Bo1")
    isdone=1
  if(series_length==2):
    role_object = discord.utils.get(guild.roles, name="F2-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="F1-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="F0-2")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Fifa Bo2")
    isdone=1
  if(series_length==3):
    role_object = discord.utils.get(guild.roles, name="F2-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="F2-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="F1-2")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="F0-2")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Fifa Bo3")
    isdone=1
  if(series_length==5):
    role_object = discord.utils.get(guild.roles, name="F3-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="F3-2")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="F3-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="F1-3")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="F2-3")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="F0-3")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Fifa Bo5")
    isdone=1
  else:
    if(isdone== 0):
      await interaction.followup.send("I was unable to delete any of the roles please verify series length - 1 / 2 / 3 / 5")
    



@tree.command(name="deletecsgoroles", description = "Delete CSGO roles for prediction", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, series_length: int):
  await interaction.response.defer()
  guild = interaction.guild
  isdone=0
  if(series_length==1):
    role_object = discord.utils.get(guild.roles, name="CS1-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CS0-1")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a CSGO Bo1")
    isdone=1
  if(series_length==2):
    role_object = discord.utils.get(guild.roles, name="CS2-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CS1-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CS0-2")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a CSGO Bo2")
    isdone=1
  if(series_length==3):
    role_object = discord.utils.get(guild.roles, name="CS2-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CS2-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CS1-2")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CS0-2")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a CSGO Bo3")
    isdone=1
  if(series_length==5):
    role_object = discord.utils.get(guild.roles, name="CS3-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CS3-2")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CS3-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CS1-3")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CS2-3")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CS0-3")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a CSGO Bo5")
    isdone=1
  else:
    if(isdone== 0):
      await interaction.followup.send("I was unable to delete any of the roles please verify series length - 1 / 2 / 3 / 5")





@tree.command(name="deletecsgoaroles", description = "Delete CSGO Academy roles for prediction", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, series_length: int):
  await interaction.response.defer()
  guild = interaction.guild
  isdone=0
  if(series_length==1):
    role_object = discord.utils.get(guild.roles, name="CSA1-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CSA0-1")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a CSGO Academy Bo1")
    isdone=1
  if(series_length==2):
    role_object = discord.utils.get(guild.roles, name="CSA2-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CSA1-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CSA0-2")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a CSGO Academy Bo2")
    isdone=1
  if(series_length==3):
    role_object = discord.utils.get(guild.roles, name="CSA2-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CSA2-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CSA1-2")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CSA0-2")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a CSGO Academy Bo3")
    isdone=1
  if(series_length==5):
    role_object = discord.utils.get(guild.roles, name="CSA3-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CSA3-2")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CSA3-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CSA1-3")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CSA2-3")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="CSA0-3")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a CSGO Academy Bo5")
    isdone=1
  else:
    if(isdone== 0):
      await interaction.followup.send("I was unable to delete any of the roles please verify series length - 1 / 2 / 3 / 5")



@tree.command(name="deletevaloldnroles", description = "Delete Valorant LDN roles for prediction", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, series_length: int):
  await interaction.response.defer()
  guild = interaction.guild
  isdone=0
  if(series_length==1):
    role_object = discord.utils.get(guild.roles, name="VLDN1-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="VLDN0-1")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Valorant LDN United Bo1")
    isdone=1
  if(series_length==2):
    role_object = discord.utils.get(guild.roles, name="VLDN2-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="VLDN1-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="VLDN0-2")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Valorant LDN United Bo2")
    isdone=1
  if(series_length==3):
    role_object = discord.utils.get(guild.roles, name="VLDN2-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="VLDN2-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="VLDN1-2")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="VLDN0-2")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Valorant LDN United Bo3")
    isdone=1
  if(series_length==5):
    role_object = discord.utils.get(guild.roles, name="VLDN3-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="VLDN3-2")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="VLDN3-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="VLDN1-3")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="VLDN2-3")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="VLDN0-3")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Valorant LDN United Bo5")
    isdone=1
  else:
    if(isdone== 0):
      await interaction.followup.send("I was unable to delete any of the roles please verify series length - 1 / 2 / 3 / 5")



      






@tree.command(name="deleterandomroles", description = "Delete Random roles for prediction", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, series_length: int):
  await interaction.response.defer()
  guild = interaction.guild
  isdone=0
  if(series_length==1):
    role_object = discord.utils.get(guild.roles, name="R1-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="R0-1")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Random Game Bo1")
    isdone=1
  if(series_length==2):
    role_object = discord.utils.get(guild.roles, name="R2-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="R1-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="R0-2")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Random Game Bo2")
    isdone=1
  if(series_length==3):
    role_object = discord.utils.get(guild.roles, name="R2-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="R2-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="R1-2")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="R0-2")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Random Game Bo3")
    isdone=1
  if(series_length==5):
    role_object = discord.utils.get(guild.roles, name="R3-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="R3-2")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="R3-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="R1-3")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="R2-3")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="R0-3")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Random Game Bo5")
    isdone=1
  else:
    if(isdone== 0):
      await interaction.followup.send("I was unable to delete any of the roles please verify series length - 1 / 2 / 3 / 5")




@tree.command(name="dotastreams", description = "Get the streams for the next dota series", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  streaminfo = DotaStreams()
  Teams1 = streaminfo[0]
  Teams2 = streaminfo[1]
  flagMessage = streaminfo[2]
  convertedURL = streaminfo[3]

  if (Teams1 == "No games found"):
      embed = discord.Embed(title="No Dota streams / games were found",color=0xf10909)
      embed.add_field(name="What you can try",value="You can try using /nextdota / /nextdota2 to see if there are any games coming up",inline=True)
      embed.add_field(name="Links",value="https://liquipedia.net/dota2/OG",inline=False)
      await interaction.followup.send(embed=embed)

  else:
      embed = discord.Embed(title="Dota streams found!", color=0xf10909)
      embed.add_field(name="The game found",value=Teams1 + " vs " + Teams2,inline=True)
    
      if(interaction.channel_id != 689903856095723569 and interaction.channel_id != 926214194280419368 and interaction.channel_id != 1007303552445726750):
        embed.add_field(name="Streams / Flags",value="```" + flagMessage + "```",inline=False)
      embed.add_field(name="Streams available",value=flagMessage,inline=False)
      embed.add_field(name="Where I found the streams",value=convertedURL,inline=False)
      await interaction.followup.send(embed=embed)




@tree5.command(name="dotastreams", description = "Get the streams for the next dota series", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  streaminfo = tundraDotaStreams()
  Teams1 = streaminfo[0]
  Teams2 = streaminfo[1]
  flagMessage = streaminfo[2]
  convertedURL = streaminfo[3]

  if (Teams1 == "No games found"):
      embed = discord.Embed(title="No Dota streams / games were found",color=0xf10909)
      embed.add_field(name="What you can try",value="You can try using /nextdota / /nextdota2 to see if there are any games coming up",inline=True)
      embed.add_field(name="Links",value="https://liquipedia.net/dota2/Tundra_Esports",inline=False)
      await interaction.followup.send(embed=embed)

  else:
      embed = discord.Embed(title="Dota streams found!", color=0xf10909)
      embed.add_field(name="The game found",value=Teams1 + " vs " + Teams2,inline=True)
    
      if(interaction.channel_id != 689903856095723569 and interaction.channel_id != 926214194280419368 and interaction.channel_id != 1007303552445726750):
        embed.add_field(name="Streams / Flags",value="```" + flagMessage + "```",inline=False)
      embed.add_field(name="Streams available",value=flagMessage,inline=False)
      embed.add_field(name="Where I found the streams",value=convertedURL,inline=False)
      await interaction.followup.send(embed=embed)




  

@tree.command(name="valoldnstreams", description = "Get the streams for the next Valorant LDN United series", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  streaminfo = ValoStreams('https://www.vlr.gg/team/8903/og-ldn-utd')
  valoenemyteam = streaminfo[0]
  streams = streaminfo[1]
  matchlink = streaminfo[2]

  if (matchlink == "No games found"):
      embed = discord.Embed(title="No Valorant streams / games were found",color=0xd57280)
      embed.add_field(name="What you can try",value="You can try using /nextldnvalo / /nextldnvalorant to see if there are any games coming up",inline=True)
      embed.add_field(name="Links",value="https://www.vlr.gg/team/8903/og-ldn-utd / https://liquipedia.net/valorant/OG_LDN_UTD",inline=False)
      await interaction.followup.send(embed=embed)

  else:
      embed = discord.Embed(title="Valorant streams coming up!",color=0xd57280)
      embed.add_field(name="The game found",value="OG LDN UTD vs " + valoenemyteam,inline=True)
    
      if(interaction.channel_id != 810939258222936094 and interaction.channel_id != 926214194280419368 and interaction.channel_id != 1007303552445726750):
        embed.add_field(name="Streams for copying", value="```" + streams + "```",inline=False)
        
      embed.add_field(name="Streams with flags",value=streams,inline=False)
      embed.add_field(name="Game page info",value=matchlink,inline=False)
      await interaction.followup.send(embed=embed)



@tree.command(name="csgostreams", description = "Get the streams for the next CSGO series", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  streaminfo = CSGOStreams('https://www.hltv.org/team/10503/og#tab-matchesBox')
  team1 = streaminfo[1]
  team2 = streaminfo[2]
  links = streaminfo[3]
  matchlink = streaminfo[4]

  if (team1 == "No games found"):
      embed = discord.Embed(title="No CSGO streams / games were found",color=0xff8800)
      embed.add_field(name="What you can try",value="You can try using /nextcsgo to see if there are any games coming up",inline=True)
      embed.add_field(name="Links",value="OG Liquipedia:  https://liquipedia.net/counterstrike/OG\nOG HLTV: https://www.hltv.org/team/10503/og#tab-matchesBox",inline=False)
      await interaction.followup.send(embed=embed)
    
  else:
      embed = discord.Embed(title="CSGO Stream links",color=0xff8800)
      embed.add_field(name="The game found",value=team1 + " vs " + team2,inline=True)
      if(interaction.channel_id !=690952309827698749 and interaction.channel_id != 926214194280419368 and interaction.channel_id != 1007300362237128705):
        embed.add_field(name="Streams",value="```" + links + "```",inline=False)
      embed.add_field(name="Streams available",value=links,inline=False)
      embed.add_field(name="Game page info",value=matchlink,inline=False)
      await interaction.followup.send(embed=embed)

@tree.command(name="csgoastreams", description = "Get the streams for the next CSGO Academy series", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  streaminfo = CSGOStreams('https://www.hltv.org/team/11672/og-academy#tab-matchesBox')
  team1 = streaminfo[1]
  team2 = streaminfo[2]
  links = streaminfo[3]
  matchlink = streaminfo[4]

  if (team1 == "No games found"):
      embed = discord.Embed(title="No CSGO streams / games were found",color=0xff8800)
      embed.add_field(name="What you can try",value="You can try using /nextcsgo to see if there are any games coming up",inline=True)
      embed.add_field(name="Links",value="OG Liquipedia:  https://liquipedia.net/counterstrike/OG_Academy\nOG HLTV: https://www.hltv.org/team/11672/og-academy#tab-matchesBox",inline=False)
      await interaction.followup.send(embed=embed)
    
  else:
      embed = discord.Embed(title="CSGO Academy Stream links", color=0xff8800)
      embed.add_field(name="The game found",value=team1 + " vs " + team2,inline=True)
      
      if(interaction.channel_id !=690952309827698749 and interaction.channel_id != 926214194280419368 and interaction.channel_id != 1007303552445726750):
        embed.add_field(name="Streams",value="```" + links + "```",inline=False)
      
      embed.add_field(name="Streams available",value=links,inline=False)
      embed.add_field(name="Game page info",value=matchlink,inline=False)
      await interaction.followup.send(embed=embed)






@tree.command(name="dotaevents", description="Get upcoming dota events", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  test = dotaevents()
  await interaction.followup.send(embed=test)



@tree.command(name="csgoevents", description="Get upcoming CSGO events", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  test = csgoevents('https://www.hltv.org/team/10503/og#tab-eventsBox')
  await interaction.followup.send(embed=test)

@tree.command(name="csgoaevents", description="Get upcoming CSGO Academy events", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  test = csgoevents('https://www.hltv.org/team/11672/og-academy#tab-eventsBox')
  await interaction.followup.send(embed=test)


@tree5.command(name="dotastats", description="Get stats for Dota players", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction, player: str):
  await interaction.response.defer()
  embed = dotaplayerstats(player)
  await interaction.followup.send(embed=embed)





@tree.command(name="dotastats", description="Get stats for Dota players", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, player: str):
  await interaction.response.defer()
  embed = dotaplayerstats(player)
  await interaction.followup.send(embed=embed)

@tree.command(name="csgostats", description="Get stats for CSGO players", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, player: str):
  await interaction.response.defer()
  embed = csgoplayerstat(player)
  await interaction.followup.send(embed=embed)

@tree.command(name="valostats", description="Get stats for Valorant players", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, player: str):
  await interaction.response.defer()
  embed = valoplayerstats(str(player)) 
  await interaction.followup.send(embed=embed)


@tree.command(name="csmaps", description="Get CSGO maps and stats for current game", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  maps = csgomap('https://www.hltv.org/team/10503/og#tab-matchesBox')
  await interaction.followup.send(maps)

@tree.command(name="csamaps", description="Get CSGO Academy maps and stats for current game", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  maps = csgomap('https://www.hltv.org/team/11672/og-academy#tab-matchesBox')
  await interaction.followup.send(maps)

@tree.command(name="valoldnmaps", description="Get Valorant LDN United maps and stats for current game", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  valo_maps = valomaps()
  await interaction.followup.send(valo_maps)



@tree.command(name="changedt", description = "Change the Dota tournament tracked", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction, liquipediaurl: str):
  await interaction.response.defer()
  newlink = liquipediaurl
  f = open("dotatournament.txt", "w")
  f.write(newlink)
  f.close()
  upload_file('/dropdotatournament.txt', 'dotatournament.txt')
  await interaction.followup.send("The tournament tracked has been updated to the link you have sent - <"+ newlink +">\n\nIf there is an error in your link, you are able to use /verifydturl to check the link or try changing again!")



@tree5.command(name="changedt", description = "Change the Dota tournament tracked", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction, liquipediaurl: str):
  await interaction.response.defer()
  newlink = liquipediaurl
  f = open("dotatournament.txt", "w")
  f.write(newlink)
  f.close()
  tundraupload_file('/dropdotatournament.txt', 'dotatournament.txt')
  await interaction.followup.send("The tournament tracked has been updated to the link you have sent - <"+ newlink +">\n\nIf there is an error in your link, you are able to use /verifydturl to check the link or try changing again!")


@tree5.command(name="resetdt", description = "Reset the Dota tournament tracked", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  data = tundradownload_file('/dropdotatournament.txt','dotatournament.txt')
  f = open("dotatournament.txt", "w")
  f.write("none")
  f.close()
  tundraupload_file('/dropdotatournament.txt', 'dotatournament.txt')
  await interaction.followup.send("The tournament currently tracked has been removed")


@tree.command(name="resetdt", description = "Reset the Dota tournament tracked", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  data = download_file('/dropdotatournament.txt','dotatournament.txt')
  f = open("dotatournament.txt", "w")
  f.write("none")
  f.close()
  upload_file('/dropdotatournament.txt', 'dotatournament.txt')
  await interaction.followup.send("The tournament currently tracked has been removed")

@tree.command(name="verifydt", description = "Verify the Dota tournament tracked", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  data = download_file('/dropdotatournament.txt','dotatournament.txt')
  f = open("dotatournament.txt", "r")
  link = f.read()
  await interaction.followup.send("The link currently stored is - <" +link + ">")


@tree5.command(name="verifydt", description = "Verify the Dota tournament tracked", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  data = tundradownload_file('/dropdotatournament.txt','dotatournament.txt')
  f = open("dotatournament.txt", "r")
  link = f.read()
  await interaction.followup.send("The link currently stored is - <" +link + ">")


@tree.command(name="nextdt", description = "Next game in the Dota Tournament tracked", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  channelDataID = interaction.channel_id
  embed = DotaCheckTourni(channelDataID)
  embed = embed[0]
  if ((channelDataID == 689903856095723569) or (channelDataID == 690952309827698749)):
      await interaction.followup.send(embed)
  else:
      await interaction.followup.send(embed=embed)


@tree5.command(name="nextdt", description = "Next game in the Dota Tournament tracked", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  channelDataID = interaction.channel_id
  embed = tundraDotaCheckTourni(channelDataID)
  embed = embed[0]
  if ((channelDataID == 867690069981003807) or (channelDataID == 867690069981003807)):
      await interaction.followup.send(embed)
  else:
      await interaction.followup.send(embed=embed)



@tree.command(name="dtstreams", description = "Get streams for the Dota tournament tracked", guild = discord.Object(id = IDForServer))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  data = download_file('/dropdotatournament.txt','dotatournament.txt')
  f = open("dotatournament.txt", "r")
  my_url = f.read()
  f.close()
  dtstreaminfo = dtStreams(my_url)
  streamlinks = dtstreaminfo[0]
  urloftourni = dtstreaminfo[1]

  embed = discord.Embed(title="Streams for the tournament", color=0x55a7f7)
  embed.add_field(name="Streams", value=streamlinks, inline=True)
  embed.add_field(name="Where I found the streams",value=urloftourni,inline=False)
  await interaction.followup.send(embed=embed)




@tree5.command(name="dtstreams", description = "Get streams for the Dota tournament tracked", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  data = tundradownload_file('/dropdotatournament.txt','dotatournament.txt')
  f = open("dotatournament.txt", "r")
  my_url = f.read()
  f.close()
  dtstreaminfo = dtStreams(my_url)
  streamlinks = dtstreaminfo[0]
  urloftourni = dtstreaminfo[1]

  embed = discord.Embed(title="Streams for the tournament", color=0x55a7f7)
  embed.add_field(name="Streams", value=streamlinks, inline=True)
  embed.add_field(name="Where I found the streams",value=urloftourni,inline=False)
  await interaction.followup.send(embed=embed)

@treehouse.command(name="powerstuff", description = "huuhuh", guild = discord.Object(id = IDForServerHouse))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  api_url = 'https://api.octopus.energy/v1/electricity-meter-points/1100770774030/meters/19M0031156/consumption/'
  api_key = str(os.getenv('apiforocto'))
  header = {'Content-type': 'application/json','Authorization': api_key}
  method ="get"
  auth = HTTPBasicAuth('apikey', api_key)
  #response = requests.get(api_url)
  #rsp = requests.request(method, api_url, headers=headers)
  rsp = requests.get(api_url, headers=header)
  print(rsp)



@treehouse.command(name="addviewing", description = "Add a house for viewing", guild = discord.Object(id = IDForServerHouse))
async def self(interaction: discord.Interaction, linktohouse: str, pcm: int, dateofviewing: str):
  await interaction.response.defer()
  try:
    linetoadd = str(linktohouse) + ", £" + str(pcm) + ", Date of viewing - " + str(dateofviewing) + "\n"
    #data = download_file('/dropviewings.txt', 'viewings.txt')
    f = open("viewings.txt", "a")
    f.write(linetoadd)
    f.close()
    upload_file('/dropviewings.txt', 'viewings.txt')
    await interaction.followup.send("I have added house: " + str(linktohouse) + " , at cost - £" + str(pcm) + ", on: " + str(dateofviewing))
  except Exception as e:
    print(e)

    
@treehouse.command(name="upcomingviewings", description = "list viewings", guild = discord.Object(id = IDForServerHouse))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  try:
    data = download_file('/dropviewings.txt', 'viewings.txt')
  except:
    await interaction.followup.send("No viewings yet :( LETS GET SOME IN!!")
  a_file = open("viewings.txt", "r")
  x = a_file.readlines()
  print(len(x))
  text=""
  try:
    i = 0
    while(i < len(x)):
      text = str(text) + str(i+1) + " - " + str(x[i]) 
      i=i+1
    
    embed = discord.Embed(title="Upcoming viewings", color=0x55a7f7)
    embed.add_field(name="Viewings",value=text,inline=True)
    await interaction.followup.send(embed=embed)

  except Exception as e:
    await interaction.followup.send("No viewings yet :( LETS GET SOME IN!!")
    print(e)

@treehouse.command(name="reviewhouse", description = "Review the house we visited", guild = discord.Object(id = IDForServerHouse))
async def self(interaction: discord.Interaction, viewingnumber: int, review: str):
  try:
    await interaction.response.defer()
    text="error"
    check = int(os.getenv('checker'))
    
    data = download_file('/dropviewings.txt', 'viewings.txt')
    a_file = open("viewings.txt", "r")
    x = a_file.readlines()  
    viewings=""
    viewingdone=""
    viewingafter=""
    viewingnumber = viewingnumber -1
    i=0
    j=0
    while(i < len(x)):
      if(i != viewingnumber and i < viewingnumber):
        viewings = str(viewings) + str(x[i])
      if (i != viewingnumber and i > viewingnumber):
        viewingafter = str(x[i])
        viewings = str(viewings) + str(viewingafter)
      else:
        viewingdone = str(review) + " - " + str(x[i])
        j=+1
        text="NoError"
      i=i+1
    b_file = open("viewings.txt", "w")
    b_file.write(viewings)
    b_file.close()
    upload_file('/dropviewings.txt', 'viewings.txt')
    if(check==0):
      data2 = download_file('/dropviewed.txt', 'viewed.txt')
    c_file = open("viewed.txt", "a")
    c_file.write(viewingdone)
    c_file.close()
    upload_file('/dropviewed.txt', 'viewed.txt')
    if(j==0):
      await interaction.followup.send("Wagwan whats goin on, you put a number that aint on the list fam! Give it another go! You got this!")
    await interaction.followup.send("Done")
  except Exception as e:
    print(e)
    await interaction.followup.send("Wagwan whats goin on, you put a number that aint on the list fam! Give it another go! You got this!")





@treehouse.command(name="viewedhomes", description = "list homes we've seen with reviews", guild = discord.Object(id = IDForServerHouse))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  try:
    data = download_file('/dropviewed.txt', 'viewed.txt')
  except:
    await interaction.followup.send("We haven't viewed any homes yet what ya doin!")
  a_file = open("viewed.txt", "r")
  x = a_file.readlines()
  text=""
  print(len(x))
  
  try:
    i = 0
    while(i < len(x)):
      toadd = str(x[i])
      text = str(text) + str(toadd)
      i=i+1
    embed = discord.Embed(title="Viewed homes", color=0x55a7f7)
    embed.add_field(name="Viewed homes and notes",value=text,inline=True)
    
    await interaction.followup.send(embed=embed)

  except Exception as e:
    print(e)

    


#Cleans out reminder file if no reminders are left
async def cleanreminders():
    data = download_file('/dropreminders.txt', 'reminders.txt')
    a_file = open("reminders.txt", "r")
    list_of_lines = a_file.readlines()
    i = 0

    reminders = []
    while (i < len(list_of_lines)):

        base_reminder = list_of_lines[i]
        splitUpValues = base_reminder.rsplit(", ")

        checkIfSent = splitUpValues[4]
        checkIfSent = checkIfSent[0:2]

        if (checkIfSent == "no"):
            reminders.append(base_reminder + ", " + str(i))

        i = i + 1

    print(len(reminders))
    if (len(reminders) == 0):
        file = open("reminders.txt", "r+")
        file.truncate(0)
        file.close()
        upload_file('/dropreminders.txt', 'reminders.txt')


#Opening the file with last message every 5 mins
async def openingfile():
    data = download_file('/droplastmessage.txt', 'lastmessage.txt')
    g = open("lastmessage.txt", "r")
    g2 = g.read()
    g.close()
    print("File opened, value = " + g2)

    data = tundradownload_file('/droplastmessage.txt', 'lastmessage.txt')
    g = open("lastmessage.txt", "r")
    g2 = g.read()
    g.close()
    print("File opened, value = " + g2)



  




#Daily posts
async def testingspam():
    
    c = client.get_channel(839466348970639391)
    currenttime = datetime.datetime.now()
   
    #Dota daily
    try:
      emote = client.get_emoji(730890894814740541)
      channel = client.get_channel(964298402089275462)
      channel2 = client.get_channel(973130064667484170)
      value = DotaCheck(0, False)
      Teams = value[1]
      name = "Dota 2 game: " + Teams
      time=datetime.datetime.now().astimezone() + value[3]
      end_time=time+datetime.timedelta(minutes=10)
      linktogame = value[7]
      tourniname = value[6]
      serieslength=value[8]
      epoch=value[9]
      streaminfo = DotaStreams()
      if(serieslength == "Bo1"):
        cover=2
      if(serieslength == "Bo2"):
        cover =3
      if(serieslength=="Bo3"):
        cover=4
      if(serieslength=="Bo5"):
        cover="Determined by series length"
      
      flagMessage = streaminfo[2]
      description = tourniname +"\n" + flagMessage + "\n:mega: https://twitter.com/OGesports\n"
      guild = client.get_guild(689865753662455829)
      linetocheck = Teams+","+linktogame
      gardenerinfo = "Hey <@&720253636797530203>\n\nI need up to four moderators to work the Dota game - " +  Teams + " , at <t:" + str(epoch) + ">\n\nPlease react below with a <:OGpeepoYes:730890894814740541> to sign up!\n\nAs this is a " + str(serieslength) +", you will be able to add " + str(cover) +" hours of work to your invoice for the month."

      try:
        download_file('/dotaevent.txt', 'dotaevent.txt')
        f=open('dotaevent.txt', 'r')
        lines=f.readlines()
        f.close()
      except:
        lines=linetocheck

      try:
        if lines[0] == linetocheck  or len(lines[0]) < 10:
          
          pass
        else:
          if(Teams == "OG vs TBD" or Teams == "TBD vs OG"):
            print("TBD")
          else:
            eventdata = await guild.create_scheduled_event(name=name, description=description,privacy_level = discord.PrivacyLevel.guild_only, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=linktogame)
            data2= await guild.fetch_scheduled_event(eventdata.id)
            await channel.send(data2.url)
            test = await channel2.send(str(gardenerinfo))
            await test.add_reaction(emote)
            f=open("dotaeventsign.txt", "w")
            f.write(str(test.id))
            f.close()
            upload_file('/dotaeventsignup.txt', 'dotaeventsign.txt')
            
          f = open("dotaevent.txt", "w")
          f.write(linetocheck)
          f.close()
          upload_file('/dotaevent.txt', 'dotaevent.txt')
          
          
          
      except:
        if(Teams == "OG vs TBD" or Teams == "TBD vs OG"):
            print("TBD")
        else:
            eventdata = await guild.create_scheduled_event(name=name, description=description,privacy_level = discord.PrivacyLevel.guild_only, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=linktogame)
            data2= await guild.fetch_scheduled_event(eventdata.id)
            await channel.send(data2.url)
            test = await channel2.send(str(gardenerinfo))
            await test.add_reaction(emote)
            f=open("dotaeventsign.txt", "w")
            f.write(str(test.id))
            f.close()
            upload_file('/dotaeventsignup.txt', 'dotaeventsign.txt')
        
        f = open("dotaevent.txt", "w")
        f.write(linetocheck)
        f.close()
        upload_file('/dotaevent.txt', 'dotaevent.txt')
        
        pass

      
    
      
    except Exception as e:
      print(e)

    #Valo daily - regular OG
    try:
      emote = client.get_emoji(730890894814740541)
      channel = client.get_channel(964298835453169664)
      channel2 = client.get_channel(973130064667484170)
      value = ValoCheck(0, 'https://www.vlr.gg/team/2965/og', False)
      teams = value[1]
      enemyteam = value[10]
      time = datetime.datetime.now().astimezone() + value[3]
      streaminfo = ValoStreams('https://www.vlr.gg/team/2965/og')
      linktogame = value[4]
      linktogame = "https://www.vlr.gg/team/2965/og"
      gamepos = value[6]
      serieslength = value[8]
      epoch = value[9]
      if(serieslength == "Bo1"):
        cover=2
      if(serieslength == "Bo2"):
        cover =3
      if(serieslength=="Bo3"):
        cover=4
      if(serieslength=="Bo5"):
        cover="Determined by series length"
      gardenerinfo = "Hey <@&720253636797530203>\n\nI need up to two moderators to work the Valorant game - " +  teams + " , at <t:" + str(epoch) + ">\n\nPlease react below with a <:OGpeepoYes:730890894814740541> to sign up!\n\nAs this is a " + str(serieslength) +", you will be able to add " + str(cover) +" hours of work to your invoice for the month."
      name= "Valorant game: " + teams
      tourniname = value[7]
      description = tourniname + "\n" + str(value[4]) + "\n" + gamepos + "\n" + streaminfo[1] + "\n:mega: https://twitter.com/OGvalorant\n" 
      end_time=time+datetime.timedelta(minutes=10)
      guild = client.get_guild(689865753662455829)
      linetocheck = teams + "," + gamepos +"," +tourniname
      try:
        download_file('/valoevent.txt', 'valoevent.txt')
        f=open('valoevent.txt', 'r')
        lines=f.readlines()
        f.close()
      except:
        lines=linetocheck
      
      try:
        if lines[0] == linetocheck  or len(lines[0]) < 10:
          
          pass
        else:
          if(str(enemyteam) != "TBD"):
            eventdata = await guild.create_scheduled_event(name=name, description=description,privacy_level = discord.PrivacyLevel.guild_only, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=linktogame)
            f = open("valoevent.txt", "w")
            f.write(linetocheck)
            f.close()
            upload_file('/valoevent.txt', 'valoevent.txt')
            data2= await guild.fetch_scheduled_event(eventdata.id)
            await channel.send(data2.url)
            test = await channel2.send(str(gardenerinfo))
            await test.add_reaction(emote)
          else:
            print("Valo Enemy = TBD")
          
      except:
        if(str(enemyteam) != "TBD"):
          eventdata = await guild.create_scheduled_event(name=name, description=description,privacy_level = discord.PrivacyLevel.guild_only, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=linktogame)
          f = open("valoevent.txt", "w")
          f.write(linetocheck)
          f.close()
          upload_file('/valoevent.txt', 'valoevent.txt')
          data2= await guild.fetch_scheduled_event(eventdata.id)
          await channel.send(data2.url)
          test = await channel2.send(str(gardenerinfo))
          await test.add_reaction(emote)
          pass
        else:
          print("Valo enemy = TBD")

      
      
    except Exception as e:
      print(e)

    #Get events for ldn utd OG
    try:
      emote = client.get_emoji(730890894814740541)
      channel = client.get_channel(964298835453169664)
      channel2 = client.get_channel(973130064667484170)
      value = ValoCheck(0, 'https://www.vlr.gg/team/8903/og-ldn-utd', False)
      teams = value[1]
      enemyteam = value[10]
      time = datetime.datetime.now().astimezone() + value[3]
      streaminfo = ValoStreams('https://www.vlr.gg/team/8903/og-ldn-utd')
      linktogame = value[4]
      linktogame = "https://www.vlr.gg/team/8903/og-ldn-utd"
      gamepos = value[6]
      name= "Valorant game: " + teams
      tourniname = value[7]
      serieslength = value[8]
      epoch = value[9]
      if(serieslength == "Bo1"):
        cover=2
      if(serieslength == "Bo2"):
        cover =3
      if(serieslength=="Bo3"):
        cover=4
      if(serieslength=="Bo5"):
        cover="Determined by series length"
      gardenerinfo = "Hey <@&720253636797530203>\n\nI need up to two moderators to work the Valorant game - " +  teams + " , at <t:" + str(epoch) + ">\n\nPlease react below with a <:OGpeepoYes:730890894814740541> to sign up!\n\nAs this is a " + str(serieslength) +", you will be able to add " + str(cover) +" hours of work to your invoice for the month."
      description = tourniname + "\n" + str(value[4]) + "\n" + gamepos + "\n" + streaminfo[1] + "\n:mega: https://twitter.com/OGvalorant\n" 
      end_time=time+datetime.timedelta(minutes=10)
      guild = client.get_guild(689865753662455829)
      linetocheck = teams + "," + gamepos +"," +tourniname
      try:
        download_file('/ldnvaloevent.txt', 'ldnvaloevent.txt')
        f=open('ldnvaloevent.txt', 'r')
        lines=f.readlines()
        f.close()
      except:
        lines=linetocheck
      
      try:
        if lines[0] == linetocheck  or len(lines[0]) < 10 :
          
          pass
        else:
          if(str(enemyteam) != "TBD"):
            eventdata = await guild.create_scheduled_event(name=name, description=description,privacy_level = discord.PrivacyLevel.guild_only, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=linktogame)
            f = open("ldnvaloevent.txt", "w")
            f.write(linetocheck)
            f.close()
            upload_file('/ldnvaloevent.txt', 'ldnvaloevent.txt')
            data2= await guild.fetch_scheduled_event(eventdata.id)
            await channel.send(data2.url)
            test = await channel2.send(str(gardenerinfo))
            await test.add_reaction(emote)
            f=open("valoeventsign.txt", "w")
            f.write(str(test.id))
            f.close()
            upload_file('/valoeventsignup.txt', 'valoeventsign.txt')
          else:
            print("TBD - Valo Ldn Team")
                              
          
      except:
        if(str(enemyteam) != "TBD"):
          eventdata = await guild.create_scheduled_event(name=name, description=description,privacy_level = discord.PrivacyLevel.guild_only, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=linktogame)
          f = open("ldnvaloevent.txt", "w")
          f.write(linetocheck)
          f.close()
          upload_file('/ldnvaloevent.txt', 'ldnvaloevent.txt')
          data2= await guild.fetch_scheduled_event(eventdata.id)
          await channel.send(data2.url)
          test = await channel2.send(str(gardenerinfo))
          await test.add_reaction(emote)
          f=open("valoeventsign.txt", "w")
          f.write(str(test.id))
          f.close()
          upload_file('/valoeventsignup.txt', 'valoeventsign.txt')
          pass
        else:
          print("TBD - Valo LDN Team")

      
      
    except Exception as e:
      print(e)


  #csgoacad
    try:
      emote = client.get_emoji(730890894814740541)
      channel = client.get_channel(964298754968649748)
      channel2 = client.get_channel(973130064667484170)
      value = CSGOCheck(0, 'https://www.hltv.org/team/11672/og-academy#tab-matchesBox', False)
      teams = value[0]
      gamepage = value[4]
      tourniname = value[8]
      serieslength = value[9]
      epoch = value[10]
      name = "OG CSGO Academy game: " + teams
      time=datetime.datetime.now().astimezone() + datetime.timedelta(seconds=int(value[7]))
      end_time = time+datetime.timedelta(minutes=10)
      streaminfo = CSGOStreams('https://www.hltv.org/team/11672/og-academy#tab-matchesBox')
      streamdata = streaminfo[3]
      description = tourniname + "\n" + streamdata + "\n:mega: https://twitter.com/OGcsgo\n"
      guild = client.get_guild(689865753662455829)
      linetocheck= teams+","+gamepage

      if(str(serieslength) == "1"):
        cover=2
      if(str(serieslength) == "2"):
        cover =3
      if(str(serieslength)=="3"):
        cover=4
      if(str(serieslength)=="5"):
        cover="Determined by series length"

      gardenerinfo = "Hey <@&720253636797530203>\n\nI need up to two moderators to work the OG CSGO Academy - " +  teams + " , at <t:" + str(epoch) + ">\n\nPlease react below with a <:OGpeepoYes:730890894814740541> to sign up!\n\nAs this is a Bo" + str(serieslength) +", you will be able to add " + str(cover) +" hours of work to your invoice for the month."


      
      try:
        download_file('/csgoaevent.txt', 'csgoaevent.txt')
        f=open('csgoaevent.txt', 'r')
        lines=f.readlines()
        f.close()
      except:
        lines= linetocheck

      try:
        counter = teams.count('/')
        if lines[0] == linetocheck or counter > 0  or len(lines[0]) < 10:
          pass
        else:
          try:
            eventdata = await guild.create_scheduled_event(name=name, description=description,privacy_level = discord.PrivacyLevel.guild_only, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=gamepage)
          except:
            eventdata = await guild.create_scheduled_event(name=name, description=description, start_time=time,privacy_level = discord.PrivacyLevel.guild_only, end_time=end_time, entity_type=discord.enums.EntityType(3), location="https://www.hltv.org/team/11672/og-academy")
          f = open("csgoaevent.txt", "w")
          f.write(linetocheck)
          f.close()
          upload_file('/csgoaevent.txt', 'csgoaevent.txt')
          data2= await guild.fetch_scheduled_event(eventdata.id)
          await channel.send(data2.url)
          test = await channel2.send(str(gardenerinfo))
          await test.add_reaction(emote)
          f=open("csgoaeventsign.txt", "w")
          f.write(str(test.id))
          f.close()
          upload_file('/csgoaeventsignup.txt', 'csgoaeventsign.txt')
          
      except:
        try:
          eventdata = await guild.create_scheduled_event(name=name, description=description,privacy_level = discord.PrivacyLevel.guild_only, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=gamepage)
        except:
          eventdata = await guild.create_scheduled_event(name=name, description=description,privacy_level = discord.PrivacyLevel.guild_only, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location="https://www.hltv.org/team/11672/og-academy")
        f = open("csgoaevent.txt", "w")
        f.write(linetocheck)
        f.close()
        upload_file('/csgoaevent.txt', 'csgoaevent.txt')
        data2= await guild.fetch_scheduled_event(eventdata.id)
        await channel.send(data2.url)
        test = await channel2.send(str(gardenerinfo))
        await test.add_reaction(emote)
        f=open("csgoaeventsign.txt", "w")
        f.write(str(test.id))
        f.close()
        upload_file('/csgoaeventsignup.txt', 'csgoaeventsign.txt')
        pass

        
        
    
     
    except Exception as e:
      print(e)


#CSGO daily
    try:
      emote = client.get_emoji(730890894814740541)
      channel = client.get_channel(964298754968649748)
      channel2 = client.get_channel(973130064667484170)
      value = CSGOCheck(0, 'https://www.hltv.org/team/10503/og#tab-matchesBox', False)
      teams = value[0]
      gamepage = value[4]
      tourniname = value[8]
      serieslength = value[9]
      epoch = value[10]
      name = "CSGO game: " + teams
      time=datetime.datetime.now().astimezone() + datetime.timedelta(seconds=int(value[7]))
      end_time = time+datetime.timedelta(minutes=10)
      streaminfo = CSGOStreams('https://www.hltv.org/team/10503/og#tab-matchesBox')
      streamdata = streaminfo[3]
      description = tourniname + "\n" + streamdata + "\n:mega: https://twitter.com/OGcsgo\n"
      guild = client.get_guild(689865753662455829)
      if(len(gamepage) > 99):
        gamepage=gamepage
      else:
        gamepage = "https://www.hltv.org/team/10503/og#tab-matchesBox"
      linetocheck= teams+","+gamepage


      if(str(serieslength) == "1"):
        cover=2
      if(str(serieslength) == "2"):
        cover =3
      if(str(serieslength)=="3"):
        cover=4
      if(str(serieslength)=="5"):
        cover="Determined by series length"

      gardenerinfo = "Hey <@&720253636797530203>\n\nI need up to three moderators to work the OG CSGO - " +  teams + " , at <t:" + str(epoch) + ">\n\nPlease react below with a <:OGpeepoYes:730890894814740541> to sign up!\n\nAs this is a Bo" + str(serieslength) +", you will be able to add " + str(cover) +" hours of work to your invoice for the month."
      try:
        download_file('/csgoevent.txt', 'csgoevent.txt')
        f=open('csgoevent.txt', 'r')
        lines=f.readlines()
        f.close()
      except:
      
        lines= linetocheck

      try:
        print(1)
        print(lines[0])
        print(linetocheck)
        errortxt = lines[0] + "," + linetocheck
        f2=open('error.txt', 'w')
        f2.write(errortxt)
        f2.close()
        upload_file('/error.txt', 'error.txt')
      except:
        print("Test upload error")
      
      try:
        counter = teams.count('/')
        if lines[0] == linetocheck or counter > 0 or len(lines[0]) < 10:
          pass
        else:
          if(len(gamepage) > 99):
            eventdata = await guild.create_scheduled_event(name=name, description=description,privacy_level = discord.PrivacyLevel.guild_only, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location="https://www.hltv.org/team/10503/og#tab-matchesBox")
          else:
            eventdata = await guild.create_scheduled_event(name=name, description=description, start_time=time,privacy_level = discord.PrivacyLevel.guild_only, end_time=end_time, entity_type=discord.enums.EntityType(3), location=gamepage)
          f = open("csgoevent.txt", "w")
          f.write(linetocheck)
          f.close()
          upload_file('/csgoevent.txt', 'csgoevent.txt')
          data2= await guild.fetch_scheduled_event(eventdata.id)
          await channel.send(data2.url)
          test = await channel2.send(str(gardenerinfo))
          await test.add_reaction(emote)
          f=open("csgoeventsign.txt", "w")
          f.write(str(test.id))
          f.close()
          upload_file('/csgoeventsignup.txt', 'csgoeventsign.txt')
          
      except:
        if(len(gamepage) > 99):
          eventdata = await guild.create_scheduled_event(name=name, description=description,privacy_level = discord.PrivacyLevel.guild_only, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location="https://www.hltv.org/team/10503/og#tab-matchesBox")
        else:
          eventdata = await guild.create_scheduled_event(name=name, description=description,privacy_level = discord.PrivacyLevel.guild_only, start_time=time, end_time=end_time, entity_type=discord.enums.EntityType(3), location=gamepage)
        f = open("csgoevent.txt", "w")
        f.write(linetocheck)
        f.close()
        upload_file('/csgoevent.txt', 'csgoevent.txt')
        data2= await guild.fetch_scheduled_event(eventdata.id)
        await channel.send(data2.url)
        test = await channel2.send(str(gardenerinfo))
        await test.add_reaction(emote)
        f=open("csgoeventsign.txt", "w")
        f.write(str(test.id))
        f.close()
        upload_file('/csgoeventsignup.txt', 'csgoeventsign.txt')
        pass

        
        
    
     
    except Exception as e:
      print(e)







async def reminder(reminderData):
  #Time Values for checking difference
  currenttime = datetime.datetime.now()
  #day
  currentd = currenttime.strftime("%d")
  #hour [UK time - 1]
  currentH = currenttime.strftime("%H")
  #Minute
  currentM = currenttime.strftime("%M")
  #Month
  currentmonth = currenttime.strftime("%m")
  #year
  currentyear = currenttime.strftime("%y")
  currentyear = "20" + str(currentyear)
  currentyear = int(currentyear)
  #second
  currentsecond = currenttime.strftime("%S")
  currentDandT = datetime.datetime(int(currentyear), int(currentmonth),
                                   int(currentd), int(currentH),
                                   int(currentM), int(currentsecond))

  #reminder data
  reminderinfo = reminderData
  #Splitting up the reminder
  splitUpValues = reminderinfo.rsplit(", ")
  userID = splitUpValues[0]
  channelToSend = splitUpValues[1]
  textToSend = splitUpValues[2]
  timeToSend = splitUpValues[3]
  lineOfFile = splitUpValues[5]

  #Splitting date values
  timesplitting = timeToSend.rsplit(" ")
  dateToSend = timesplitting[0]
  timeToSend = timesplitting[1]
  #Date splitting
  datesplitting = dateToSend.rsplit("-")
  timesplitting = timeToSend.rsplit(":")
  #day values
  yearToSend = datesplitting[0]
  monthToSend = datesplitting[1]
  dayToSend = datesplitting[2]
  #time values
  hourToSend = timesplitting[0]
  minuteToSend = timesplitting[1]
  secondToSend = timesplitting[2]

  sendonDandT = datetime.datetime(int(yearToSend), int(monthToSend),
                                  int(dayToSend), int(hourToSend),
                                  int(minuteToSend), int(secondToSend))
  time_delta = (sendonDandT - currentDandT)

  timeLeftInSeconds = time_delta.total_seconds()
  channel = client.get_channel(int(channelToSend))
  if timeLeftInSeconds < 0:
      #Creating the embed
      embed = discord.Embed(
          title=
          "Your reminder time had already arrived! - While I was offline",
          color=0x55a7f7)
      embed.add_field(name="Your reminder, scheduled at - " +
                      str(sendonDandT),
                      value=textToSend,
                      inline=True)

      #Overwrites the file with tagging the line as sent
      a_file = open("reminders.txt", "r")
      list_of_lines = a_file.readlines()
      list_of_lines[int(lineOfFile)] = (userID + ", " + channelToSend +
                                        ", " + textToSend + ", " +
                                        str(sendonDandT) + ", sent\n")

      a_file = open("reminders.txt", "w")
      a_file.writelines(list_of_lines)
      a_file.close()
      upload_file('/dropreminders.txt', 'reminders.txt')
      #Sends to user
      await channel.send("<@" + userID + ">")
      await channel.send(embed=embed)

  else:
      #Forces bot to wait till the reminder is set
      await asyncio.sleep(timeLeftInSeconds)
      embed = discord.Embed(title="Your reminder time has arrived!",
                            color=0x55a7f7)
      embed.add_field(name="Your reminder, scheduled at - " +
                      str(sendonDandT),
                      value=textToSend,
                      inline=True)

      #Overwrites the file with tagging the line as sent
      a_file = open("reminders.txt", "r")
      list_of_lines = a_file.readlines()
      list_of_lines[int(lineOfFile)] = (userID + ", " + channelToSend +
                                        ", " + textToSend + ", " +
                                        str(sendonDandT) + ", sent\n")

      a_file = open("reminders.txt", "w")
      a_file.writelines(list_of_lines)
      a_file.close()
      upload_file('/dropreminders.txt', 'reminders.txt')
      #Sends to user
      await channel.send("<@" + userID + ">")
      await channel.send(embed=embed)






    
#Sentinel commands
@tree2.command(name="nextvalo", description="Get information on the next Sentinels Valorant game", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  channelDataID = int(interaction.channel_id)
  
  try:
    if(channelDataID in ShortList):
      embed = SentinelsValoCheck(channelDataID, 'https://www.vlr.gg/team/2/sentinels', True)
      embed=embed[0]
    else:
      embed = SentinelsValoCheck(channelDataID, 'https://www.vlr.gg/team/2/sentinels', False)
      embed=embed[0]
    

    if (embed == "N"):
        if (channelDataID in ShortList):
            await interaction.followup.send("No games planned currently - For more information use /nextvalo")
        else:
            embed = discord.Embed(title="OG LDN Valorant's next game",url="https://www.vlr.gg/team/2/sentinels",color=0xd57280)
            embed.set_thumbnail(url="https://owcdn.net/img/62875027c8e06.png")
            embed.add_field(name="No games planned",value="No games planned",inline=True)
            embed.add_field(name="Links",value="[Sentinals VLR](https://www.vlr.gg/team/2/sentinels) / [Sentinels Valorant Liquipedia](https://liquipedia.net/valorant/Sentinels)",inline=False)
            await interaction.followup.send(embed=embed)
    else:
        if (channelDataID in ShortList):
            await interaction.followup.send(embed)
        else:
            await interaction.followup.send(embed=embed)
  except:

    if (channelDataID in ShortList):
      await interaction.followup.send("No games planned currently - For more information use /nextvalo")
    else:
          embed = discord.Embed(title="Sentinels Valorant's next game",url="https://www.vlr.gg/team/2/sentinels",color=0xd57280)
          embed.set_thumbnail(url="https://owcdn.net/img/62875027c8e06.png")
          embed.add_field(name="No games planned",value="No games planned",inline=True)
          embed.add_field(name="Links",value="[Sentinels Valorant](https://www.vlr.gg/team/2/sentinels) / [Sentinels Valorant Liquipedia](https://liquipedia.net/valorant/Sentinels)",inline=False)
          await interaction.followup.send(embed=embed)



@tree2.command(name="nextvt", description = "Next game in the Valorant Tournament tracked", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  channelDataID = interaction.channel_id
  embed = ValoCheckTourni(channelDataID)
  embed = embed[0]
  if ((channelDataID == 689903856095723569) or (channelDataID == 690952309827698749)):
      await interaction.followup.send(embed)
  else:
      await interaction.followup.send(embed=embed)


@tree2.command(name="changevt", description = "Change the Valo tournament tracked", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction, liquipediaurl: str):
  await interaction.response.defer()
  newlink = liquipediaurl
  f = open("valotournament.txt", "w")
  f.write(newlink)
  f.close()
  sentinelupload_file('/dropvalotournament.txt', 'valotournament.txt')
  await interaction.followup.send("The tournament tracked has been updated to the link you have sent - <"+ newlink +">\n\nIf there is an error in your link, you are able to use /verifyvturl to check the link or try changing again!")




@tree2.command(name="resetvt", description = "Reset the Valo tournament tracked", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  data = sentineldownload_file('/dropvalotournament.txt','valotournament.txt')
  f = open("valotournament.txt", "w")
  f.write("none")
  f.close()
  sentinelupload_file('/dropvalotournament.txt', 'valotournament.txt')
  await interaction.followup.send("The tournament currently tracked has been removed")


@tree2.command(name="valoevents", description = "Check what events are coming up for Sentinels Valorant", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  test = sentinelsvaloevents()
  await interaction.followup.send(embed=test)



@tree2.command(name="lastvalo", description = "Last Sentinels Valorant map stats", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  last_valo = lastvalo('https://www.vlr.gg/team/matches/2/sentinels/?group=completed')
  await interaction.followup.send(last_valo)



@tree2.command(name="verifyvt", description = "Verify the Valorant tournament tracked", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  data = sentineldownload_file('/dropvalotournament.txt','valotournament.txt')
  f = open("valotournament.txt", "r")
  link = f.read()
  await interaction.followup.send("The link currently stored is - <" +link + ">")


@tree2.command(name="valomaps", description="Get Sentinels Valorant maps and stats for current game", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  valo_maps = sentinelvalomaps()
  await interaction.followup.send(valo_maps)



@tree2.command(name="valostreams", description = "Get the streams for the next Valorant series", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  streaminfo = SentinelValoStreams('https://www.vlr.gg/team/2/sentinels')
  valoenemyteam = streaminfo[0]
  streams = streaminfo[1]
  matchlink = streaminfo[2]

  if (matchlink == "No games found"):
      embed = discord.Embed(title="No Valorant streams / games were found",color=0xd57280)
      embed.add_field(name="What you can try",value="You can try using /nextvalo to see if there are any games coming up",inline=True)
      embed.add_field(name="Links",value="https://www.vlr.gg/team/2/sentinels / https://liquipedia.net/valorant/Sentinels",inline=False)
      await interaction.followup.send(embed=embed)

  else:
      embed = discord.Embed(title="Valorant streams coming up!",color=0xd57280)
      embed.add_field(name="The game found",value="Sentinels vs " + valoenemyteam,inline=True)
    
      if(interaction.channel_id != 810939258222936094 and interaction.channel_id != 926214194280419368 and interaction.channel_id != 1007303552445726750):
        embed.add_field(name="Streams for copying", value="```" + streams + "```",inline=False)
        
      embed.add_field(name="Streams with flags",value=streams,inline=False)
      embed.add_field(name="Game page info",value=matchlink,inline=False)
      await interaction.followup.send(embed=embed)




@tree2.command(name="valobo", description = "Create Valorant roles for prediction [requires 1 / 2 / 3 / 5]", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction, series_length: int):
  await interaction.response.defer()
  guild = interaction.guild
  isdone = 0
  if(series_length == 1):
    await guild.create_role(name="V1-0")
    await guild.create_role(name="V0-1")
    isdone=1
    await interaction.followup.send("I have created the roles for a Valorant Bo1")
    
  if(series_length == 2):
    await guild.create_role(name="V2-0")
    await guild.create_role(name="V1-1")
    await guild.create_role(name="V0-2")
    isdone=1
    await interaction.followup.send("I have created the roles for a Valorant Bo2")
    
  if(series_length==3):
    await guild.create_role(name="V2-0")
    await guild.create_role(name="V2-1")
    await guild.create_role(name="V1-2")
    await guild.create_role(name="V0-2")
    isdone=1
    await interaction.followup.send("I have created the roles for a Valorant Bo3")
    
  if(series_length==5):
    await guild.create_role(name="V3-0")
    await guild.create_role(name="V3-2")
    await guild.create_role(name="V3-1")
    await guild.create_role(name="V1-3")
    await guild.create_role(name="V2-3")
    await guild.create_role(name="V0-3")
    isdone=1
    await interaction.followup.send("I have created the roles for a Valorant Bo5")
    
  else:
    if(isdone== 0):
      await interaction.followup.send("Value for series length invalid, must be 1 / 2 / 3 / 5, please try again")







@tree2.command(name="deletevaloroles", description = "Delete Valorant roles for prediction", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction, series_length: int):
  await interaction.response.defer()
  guild = interaction.guild
  isdone=0
  if(series_length==1):
    role_object = discord.utils.get(guild.roles, name="V1-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="V0-1")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Valorant Bo1")
    isdone=1
  if(series_length==2):
    role_object = discord.utils.get(guild.roles, name="V2-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="V1-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="V0-2")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Valorant Bo2")
    isdone=1
  if(series_length==3):
    role_object = discord.utils.get(guild.roles, name="V2-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="V2-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="V1-2")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="V0-2")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Valorant Bo3")
    isdone=1
  if(series_length==5):
    role_object = discord.utils.get(guild.roles, name="V3-0")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="V3-2")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="V3-1")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="V1-3")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="V2-3")
    await role_object.delete()
    role_object = discord.utils.get(guild.roles, name="V0-3")
    await role_object.delete()
    await interaction.followup.send("I have deleted the roles for a Valorant Bo5")
    isdone=1
  else:
    if(isdone== 0):
      await interaction.followup.send("I was unable to delete any of the roles please verify series length - 1 / 2 / 3 / 5")







@tree2.command(name="clearvaloboard", description = "This will clear the Valo leaderboard", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  sentinelsvaloscoreboarding()
  await interaction.followup.send("The Valorant leaderboard has been reset")



@tree2.command(name="showvalo", description = "Show the Valorant Prediction leaderboard", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction, user: typing.Optional[discord.User]):
  await interaction.response.defer()
  try:
    test = sentinelsvaloscoreboardsingle(user.id)
    await interaction.followup.send(test)
  except:
    test = sentinelsvaloscoreboardreader("none")
    embed = discord.Embed(title="Valorant prediction leaderboard",color=0x55a7f7)
    embed.add_field(name="Valorant prediction - page: " + str(test[2]) + "/" + str(test[1]),value="```\n" + test[0] + "\n```",inline=True)
    embed.add_field(name="Can't see yourself?",value= "Can't see yourself on the table? use /show valo @*yourself* to see where you stand!",inline=False)
    await interaction.followup.send(embed=embed)



@tree2.command(name="valoadd", description = "Add 1 point to the Valo scoreboard", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction, role: discord.Role):
  await interaction.response.defer()
  sentineldownload_file('/valoscoreboard.csv', 'scoreboard8.csv')
  try:
    server = interaction.guild
    guild=interaction.guild
    role_name = discord.utils.get(guild.roles,id=int(role.id))
    role_name = str(role_name)
    i = 0
    role_id = server.roles[0]
    display_names = []
    member_ids = []
    file = open("filetosend.txt", "w")
    file.close()
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break
    else:
        await interaction.followup.send("Role doesn't exist")
        return
    for member in server.members:
        if role_id in member.roles:
            i = i + 1
            sentinelsvaloscoreboardadder(member.display_name,member.id, 1, i)
            display_names.append(member.display_name)
            member_ids.append(member.id)
    if (i == 0):
        await interaction.followup.send("No one was found in that role!")
    else:
        sentinelupload_file('/valoscoreboard.csv', 'scoreboard9.csv')
        await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
  except:
    await interaction.followup.send("You need to tag the winning role: example /valoadd @v9-0")






@tree2.command(name="valoremove", description = "Remove 1 point from the Valorant scoreboard", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction, role: discord.Role):
  await interaction.response.defer()
  sentineldownload_file('/valoscoreboard.csv', 'scoreboard8.csv')
  try:
    server = interaction.guild
    guild=interaction.guild
    role_name = discord.utils.get(guild.roles,id=int(role.id))
    role_name = str(role_name)
    i = 0
    role_id = server.roles[0]
    display_names = []
    member_ids = []
    file = open("filetosend.txt", "w")
    file.close()
    for role in server.roles:
        if role_name == role.name:
            role_id = role
            break
    else:
        await interaction.followup.send("Role doesn't exist")
        return
    for member in server.members:
        if role_id in member.roles:
            i = i + 1
            sentinelsvaloscoreboardadder(member.display_name,member.id, -1, i)
            display_names.append(member.display_name)
            member_ids.append(member.id)
    if (i == 0):
        await interaction.followup.send("No one was found in that role!")
    else:
        sentinelupload_file('/valoscoreboard.csv', 'scoreboard9.csv')
        await interaction.followup.send("I have added the results! This affected: " +str(i) + " users")
  except:
    await interaction.followup.send("You need to tag the winning role: example /valoremove @V9-0")





@tree2.command(name="getuserlist", description = "Get the list of users in a role", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction, role: discord.Role):
  await interaction.response.defer()
  guild = interaction.guild
  server = interaction.guild
  role_name = discord.utils.get(guild.roles,id=int(role.id))
  role_name = str(role_name)

  role_id = server.roles[0]
  display_names = []
  member_ids = []
  file = open("filetosend.txt", "w")
  file.close()
  for role in server.roles:
      if role_name == role.name:
          role_id = role
          break
  else:
      await interaction.followup.send("Role doesn't exist")
      return
  for member in server.members:
      if role_id in member.roles:
          display_names.append(member.display_name)
          member_ids.append(member.id)

  i = 0
  while (i < len(display_names)):
      f = open("filetosend.txt", "a")
      f.write("name: " + display_names[i] + " - their id number: " +str(member_ids[i]) + "\n")
      f.close
      i = i + 1

  f = open("filetosend.txt", "r")
  print(f.read())
  await interaction.followup.send("Role returned: " + role_name + '!',file=discord.File("filetosend.txt"))




@tree5.command(name="getuserlist", description = "Get the list of users in a role", guild = discord.Object(id = IDForServer5))
async def self(interaction: discord.Interaction, role: discord.Role):
  await interaction.response.defer()
  guild = interaction.guild
  server = interaction.guild
  role_name = discord.utils.get(guild.roles,id=int(role.id))
  role_name = str(role_name)

  role_id = server.roles[0]
  display_names = []
  member_ids = []
  file = open("filetosend.txt", "w")
  file.close()
  for role in server.roles:
      if role_name == role.name:
          role_id = role
          break
  else:
      await interaction.followup.send("Role doesn't exist")
      return
  for member in server.members:
      if role_id in member.roles:
          display_names.append(member.display_name)
          member_ids.append(member.id)

  i = 0
  while (i < len(display_names)):
      f = open("filetosend.txt", "a")
      f.write("name: " + display_names[i] + " - their id number: " +str(member_ids[i]) + "\n")
      f.close
      i = i + 1

  f = open("filetosend.txt", "r")
  print(f.read())
  await interaction.followup.send("Role returned: " + role_name + '!',file=discord.File("filetosend.txt"))


@tree2.command(name="vtstreams", description = "Get streams for the Valo tournament tracked", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()
  data = sentineldownload_file('/dropvalotournament.txt','valotournament.txt')
  f = open("valotournament.txt", "r")
  my_url = f.read()
  f.close()
  dtstreaminfo = vtStreams(my_url)
  streamlinks = dtstreaminfo[0]
  urloftourni = dtstreaminfo[1]

  embed = discord.Embed(title="Streams for the tournament", color=0x55a7f7)
  embed.add_field(name="Streams", value=streamlinks, inline=True)
  embed.add_field(name="Where I found the streams",value=urloftourni,inline=False)
  await interaction.followup.send(embed=embed)


@tree2.command(name="valostats", description="Get stats for Valorant players", guild = discord.Object(id = IDForServer2))
async def self(interaction: discord.Interaction, player: str):
  await interaction.response.defer()
  embed = valoplayerstats(str(player)) 
  await interaction.followup.send(embed=embed)
  guild = interaction.guild







@tree4.command(name="testselectteam", description="Select Team", guild = discord.Object(id = IDForServer4))
async def self(interaction: discord.Interaction):
  await interaction.response.defer()






#Daily posts
async def testingtundraspam():

    c = client5.get_channel(839466348970639391)
    currenttime = datetime.datetime.now()

    #Dota daily
    try:
        channel = client5.get_channel(980148345030987806)
        value = tundraDotaCheck(0, False)
        Teams = value[1]
        name = "Dota 2 game: " + Teams
        time = datetime.datetime.now().astimezone() + value[3]
        end_time = time + datetime.timedelta(minutes=10)
        linktogame = value[7]
        tourniname = value[6]
        streaminfo = tundraDotaStreams()

        flagMessage = streaminfo[2]
        description = tourniname + "\n" + flagMessage + "\n:mega: https://twitter.com/TundraEsports\n"
        guild = client5.get_guild(798487245920141322)
        linetocheck = Teams + "," + linktogame

        try:
            tundradownload_file('/dotaevent.txt', 'dotaevent.txt')
            f = open('dotaevent.txt', 'r')
            lines = f.readlines()
            f.close()
        except:
            lines = "empty"

        try:
            if lines[0] == linetocheck:

                pass
            else:
                eventdata = await guild.create_scheduled_event(name=name,privacy_level = discord.PrivacyLevel.guild_only, description=description,start_time=time,end_time=end_time, entity_type=discord.enums.EntityType(3),
                    location=linktogame)
                f = open("dotaevent.txt", "w")
                f.write(linetocheck)
                f.close()
                tundraupload_file('/dotaevent.txt', 'dotaevent.txt')
                data2 = await guild.fetch_scheduled_event(eventdata.id)
                #await channel.send(data2.url)

        except:
            eventdata = await guild.create_scheduled_event(
                name=name,
                description=description,
                start_time=time,
                end_time=end_time,
                entity_type=discord.enums.EntityType(3),
                location=linktogame, privacy_level = discord.PrivacyLevel.guild_only)
            f = open("dotaevent.txt", "w")
            f.write(linetocheck)
            f.close()
            tundraupload_file('/dotaevent.txt', 'dotaevent.txt')
            data2 = await guild.fetch_scheduled_event(eventdata.id)
            #await channel.send(data2.url)
            pass

    except Exception as e:
        print(e)







async def testingspamsentinels():
  try:
      #emote = client.get_emoji(730890894814740541)
      channel = client2.get_channel(1011742847013245008)
      voice = client2.get_channel(845041197776109589)
      #channel2 = client.get_channel(1011742847013245008)
      value = SentinelsValoCheck(0, 'https://www.vlr.gg/team/2/sentinels', False)
      teams = value[1]
      enemyteam = value[10]
      time = datetime.datetime.now().astimezone() + value[3]
      streaminfo = SentinelValoStreams('https://www.vlr.gg/team/2/sentinels')
      linktogame = value[4]
      linktogame = "https://www.vlr.gg/team/2/sentinels"
      gamepos = value[6]
      serieslength = value[8]
      epoch = value[9]
      name= "Valorant game: " + teams
      tourniname = value[7]
      description = tourniname + "\n" + str(value[4]) + "\n" + gamepos + "\n" + streaminfo[1] + "\n:mega: https://twitter.com/Sentinels\n" 
      end_time=time+datetime.timedelta(minutes=30)
      guild = client2.get_guild(423635651339223041)
      linetocheck = teams + "," + gamepos +"," +tourniname
      sentineldownload_file('/sen.png', 'sen.png')
      with open('./sen.png', 'rb') as fp:
        image_bytes = fp.read()
      try:
        sentineldownload_file('/valoevent.txt', 'valoevent.txt')
        f=open('valoevent.txt', 'r')
        lines=f.readlines()
        f.close()
      except:
        lines="empty"
      
      try:
        if lines[0] == linetocheck:
          
          pass
        else:
          if(str(enemyteam) != "TBD"):
            eventdata = await guild.create_scheduled_event(name=name, privacy_level = discord.PrivacyLevel.guild_only, channel=voice, image = image_bytes, description=description, start_time=time, end_time=end_time)
            f = open("valoevent.txt", "w")
            f.write(linetocheck)
            f.close()
            sentinelupload_file('/valoevent.txt', 'valoevent.txt')
            data2= await guild.fetch_scheduled_event(eventdata.id)
            await channel.send(data2.url)

          else:
            print("Valo Enemy = TBD")
          
      except:
        if(str(enemyteam) != "TBD"):
          eventdata = await guild.create_scheduled_event(name=name,privacy_level = discord.PrivacyLevel.guild_only, channel=voice, description=description, start_time=time, end_time=end_time)
          f = open("valoevent.txt", "w")
          f.write(linetocheck)
          f.close()
          sentinelupload_file('/valoevent.txt', 'valoevent.txt')
          data2= await guild.fetch_scheduled_event(eventdata.id)
          await channel.send(data2.url)
          pass
        else:
          print("Valo enemy = TBD")

      
      
  except Exception as e:
    print(e)






loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


loop.create_task(client.start((os.getenv('TOKEN'))))
loop.create_task(houseclient.start((os.getenv('TOKENHOUSE'))))
loop.create_task(client2.start((os.getenv('TOKEN2'))))
loop.create_task(client3.start((os.getenv('TOKEN3'))))
loop.create_task(client5.start((os.getenv('TOKEN5'))))
loop.create_task(baliclient.start((os.getenv('BALITOKEN'))))
#loop.create_task(client4.start((os.getenv('TOKEN4'))))
loop.run_forever()
#client.run(os.getenv('TOKEN'))

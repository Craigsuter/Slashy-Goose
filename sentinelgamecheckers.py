#imports
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import discord
#from dotenv import load_dotenv
#load_dotenv()
import datetime
from time import strptime
import requests
from datetime import timedelta



def SentinelsValoCheck(channelDataID, pageURL, isShort):
  try:
    #Loads OG VLR page
    testv = str(pageURL)
    uClient = uReq(testv)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")


    now = datetime.datetime.now()
    #Gets current time for later comparisons
    dt_string_day = now.strftime("%d")
    dt_string_month = now.strftime("%m")
    dt_string_year= now.strftime("%y")
    dt_string_hour= now.strftime("%H")
    dt_string_minute= now.strftime("%M")
    dt_string_second= now.strftime("%S")


    tabledata = page_soup.find("div", attrs = {"class":"wf-card "})
    tabledata2 = page_soup.findAll("div", {"class":"text-of"})
    tabledata3 = page_soup.findAll("div", {"class":"m-item-date"})
    carrot = "carrot"
    #Gets the enemy team's name
    #valoenemyteam  = page_soup.find("div", attrs={"style":"font-size: 11px; min-width: 0; font-weight: 700; width: 120px;"}).text
    
    valoenemyteam = page_soup.findAll("div", {"class": "m-item-team text-of mod-right"})
    #print(valoenemyteam[0])
    valoenemyteam= valoenemyteam[0]

    valoenemyteam = valoenemyteam.text.strip()

    valoenemyteam = valoenemyteam.split('\n', 1)[0]
    
    valoenemyteam = valoenemyteam.strip().rstrip()
    

    random = page_soup.find("span", {"class": "rm-item-score-eta"})
    random2 = str(random)
    #This will error out of the check if the score value is null [catching if the game found has already happened / started]
    if random2 == "None":
      carrot = carrot  + 1
      print(carrot)
      

    nameOfEnemy = valoenemyteam

    valotimeofgame = tabledata3[0].text
    datebeforesplit = valotimeofgame.strip()
    datesplit = datebeforesplit.rsplit(" ")
    actualdatebeforeclean = datesplit[0]
    testing = actualdatebeforeclean.split()
    #Creating date / time from all values from VLR
    dateOfGame = testing[0]
    timeOfGame = testing[1]
    prefixOfTime = datesplit[1]
    
    timeOfGame = timeOfGame.rsplit(":")
    hourofgame = timeOfGame[0]
    hourofgame = int(hourofgame)
    minuteofgame = timeOfGame[1]
    print(timeOfGame)
    print(prefixOfTime)


    hourofgame = hourofgame
    
    
    
    timeOfGame = str(hourofgame) + ":" + str(minuteofgame)
    
   
    datesections = dateOfGame.rsplit("/")
    datep1 = datesections[0]
    datep2 = datesections[1]
    datep3 = datesections[2]
    dateOfGame = datep3 + "/" + datep2 + "/" + datep1
    #Splitting out the date vlaues
    yearofgame = datep1
    monthnumber = datep2
    dayofgame2 = datep3

    print(datesections)

    try:
      tags = page_soup.findAll("a", {"class":"wf-card fc-flex m-item", 'href':True })
      games=[]
      for tag in tags:
        games.append(tag['href'])
        #print(tag['href'])

      matchlink = 'https://www.vlr.gg' + games[0]
      
    except:
      pass

    try:
      testlink = matchlink
      uClient = uReq(testlink)
      page_html2 = uClient.read()
      uClient.close()
      page_soup2 = soup(page_html2, "html.parser")

      tabledata2 = page_soup2.findAll("div", {"class":"match-header-event-series"})
      gameposition = tabledata2[0].text.strip()
      gameposition = gameposition.replace("\t", "").replace("\n","")
      serieslength = page_soup2.findAll("div", {"class": "match-header-vs-note"})
      serieslength = serieslength[1].text.strip()
      serieslength = serieslength.replace(" ", "")
     
      
      
    except:
      gameposition="No game found"
      pass

    try:
      testlink = matchlink
      uClient = uReq(testlink)
      page_html3 = uClient.read()
      uClient.close()
      page_soup3 = soup(page_html3, "html.parser")

      
      
      tabledata3 = page_soup2.findAll("div", {"style":"font-weight: 700;"})
      tourniname = tabledata3[0].text.replace("\n","").replace("\t","")
         
    except:
      
      tourniname = "No game found"
      pass
    
    #
    UTCTime = timeOfGame.rsplit(":")
    UTCTime2 = timeOfGame.rsplit(":")
    timecheckingdevice = UTCTime[0]
    
      
    UTCBC = int(UTCTime[0])-1
    print(UTCBC)
    
    if UTCBC > 12:
      if prefixOfTime == "am":
        prefixOfTime = "pm"
        
      else:
        prefixOfTime = "am"
    if UTCBC > 12:
      hourofvalo = str(UTCBC-12)
      UTCTime = str(UTCBC - 12) + ":" + UTCTime[1] + prefixOfTime
    else:
      hourofvalo= UTCBC
      if(hourofvalo==12 and prefixOfTime=="am"):
        hourofvalo=0
        
      UTCTime = str(UTCBC) + ":" + UTCTime[1] + prefixOfTime
      
    
    #date/time comparisions to get a countdown
    
    
    print(prefixOfTime)
    if prefixOfTime == "pm" and hourofvalo != 12:
      hourofvalo = int(hourofvalo) + 12
      
      
    minuteofgame = UTCTime2[1]
    dt_string_year = "20" + str(dt_string_year)
    a = datetime.datetime(int(yearofgame), int(monthnumber), int(dayofgame2), (int(hourofvalo)) , int(minuteofgame), 0)
    if(timecheckingdevice == 12 and prefixOfTime =="am"):
      a = a.timedelta(-39600)
    b = datetime.datetime(int(dt_string_year), int(dt_string_month), int(dt_string_day), int(dt_string_hour), int(dt_string_minute), int(dt_string_second))


    epochtest = datetime.datetime(int(yearofgame), int(monthnumber), int(dayofgame2), int(hourofvalo), int(minuteofgame), 0).timestamp()
    
    lenofepoch = len(str(epochtest))
    epoch = str(epochtest)[:lenofepoch - 2]
    
    
    c = a-b
    
    #Will check if the game has already begun
    if (str(pageURL) == "https://www.vlr.gg/team/2/sentinels"):
        valorantTeams = "Sentinels vs " + nameOfEnemy
    else:
        valorantTeams = "Sentinels vs " + nameOfEnemy
    valorantTeamTime = dateOfGame + " - " + UTCTime + " UTC"
    if (c.days < 0):
      c = "The game is meant to have begun!"
    
    

    if (isShort == True):
      c= str(c)
      embed = valorantTeams + " - Starts in: " + c  + " / In your local time: <t:" + str(epoch) + "> - For more information use !nextvalo / !nextvalo"
      


    
      
    else:
      if (str(pageURL) == "https://www.vlr.gg/team/2/sentinels"):
        embed=discord.Embed(title="Sentinels next Valorant game", url=str(pageURL),color=0xd57280)
      else:
        embed=discord.Embed(title="Sentinels next Valorant game", url=str(pageURL),color=0xd57280)
      embed.set_thumbnail(url="https://owcdn.net/img/62875027c8e06.png")
      embed.add_field(name=valorantTeams, value= "In your local timezone - <t:" + str(epoch) + ">", inline=True)
      embed.add_field(name="Time remaining", value= c , inline = False)
      embed.add_field(name="Notice", value="Please check Liquipedia by clicking the title of this embed for more information as the time might not be accurate", inline=False)
      try:
        embed.add_field(name="Links", value="[Sentinels VLR](https://www.vlr.gg/team/2/sentinels) / [Sentinels Valorant Liquipedia](https://liquipedia.net/valorant/Sentinels)\n[Matchlink](" + str(matchlink) + ")", inline=False)
      except:
        embed.add_field(name="Links", value="[Sentinels VLR](https://www.vlr.gg/team/2/sentinels) / [Sentinels Valorant Liquipedia](https://liquipedia.net/valorant/Sentinels)", inline=False)
 
    #return(embed)
    print(c)
    return (embed, valorantTeams, valorantTeamTime, c, matchlink, dayofgame2, gameposition, tourniname, serieslength, epoch, nameOfEnemy)

  except Exception as e:
    print(exc_type, fname, exc_tb.tb_lineno)
    return("No games planned")
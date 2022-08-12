#imports
from bs4 import BeautifulSoup as soup
import discord
from dotenv import load_dotenv
load_dotenv()
import requests


def csgoevents(URL):
  try:
    #Loading HLTV of OG
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}


    #OGpage = Set the HLTV matchbox url for the team you wish to track here e.g - 'https://www.hltv.org/team/10503/og#tab-matchesBox'
    OGpage = URL
    r2 = requests.get(OGpage, headers=headers)

    page_soup2 = soup(r2.text, "html.parser")
    dataofpage = page_soup2.findAll("div", {"class":"upcoming-events-holder"})
    tourninamedata = dataofpage[0].findAll("div", {"class":"eventbox-eventname"})
    tournidatesdata = dataofpage[0].findAll("div", {"class":"eventbox-date"})

    
    
    linkinfo = []
    tourninames=[]
    tournidates=[]
    i=0
    j=0
    
    while(i < len(tourninamedata)):
      tourninaming = tourninamedata[i].text
      #tourninaming = tourninaming[2:]
      #tourninaming= tourninaming[:(len(tourninaming)-2)]
      tourninames.append(tourninaming)
      i += 1
    

    while(j < len(tournidatesdata)):
      tournidates.append(tournidatesdata[j].text)
      j += 1
    


    
    #If game found - open the page via the href / link info
    for a in dataofpage[0].findAll('a', href=True):
      
      linkinfotoattach =  "https://www.hltv.org" + str(a['href'])
      linkinfo.append(linkinfotoattach)
    
    text=""
    z =0
    if(len(tourninames) > 0):
      while(z < len(tourninames)):
        text = text + "" + str([tourninames[z]]) + "("+  str((linkinfo[z])) + ") - " + str(tournidates[z]) + "\n"

        z+=1
      if(URL != "https://www.hltv.org/team/11672/og-academy#tab-eventsBox"):
        embed=discord.Embed(title="Upcoming CSGO events for OG",color=0x55a7f7)
      else:
        embed=discord.Embed(title="Upcoming CSGO Academy events for OG",color=0x55a7f7)
      embed.add_field(name='Events found' ,value=text, inline=True)
    else:
      embed="There are currently no planned tournaments for OG"
        
      
    
   

  
    

      

    return(embed)



  except Exception as e:
    print(e)
    
    return("There are currently no planned tournaments for OG")

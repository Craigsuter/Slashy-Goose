# imports
from bs4 import BeautifulSoup as soup
import discord
from dotenv import load_dotenv
load_dotenv()
import requests

def sentinelsvaloevents():
  try:
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    OGPage = "https://liquipedia.net/valorant/Sentinels"
    r2 = requests.get(OGPage, headers=headers)
    print(1)
    page_soup2 = soup(r2.text, "html.parser")
    data_of_events = page_soup2.find_all("div", attrs={"class": "fo-nttax-infobox wiki-bordercolor-light noincludereddit"})
    event_containers = data_of_events[1]("table")
    event_names = []
    event_links = []
    event_dates = []
    print(1)
    for event_container in event_containers:
      event_names.append(event_container.find("a")['title'])
      event_links.append("https://liquipedia.net" + event_container.find("a")['href'])
      event_dates.append(event_container.find("div").text)
      print(1)
  
    info = ""
    n = 0
    print(1)
    if (len(event_names) > 0):
      print(1)
      embed = discord.Embed(title="Upcoming Valorant events for Sentinels", color=0x55a7f7)
      while(n < len(event_names)):
        info = info + "" + str([event_names[n]]) + "(" + str(event_links[n]) + ") - " + str(event_dates[n]) + "\n"
        n+=1
      
      embed.add_field(name="Events Found", value=info, inline=True)
    else:
      print(1)
      embed = discord.Embed(title="There are currently no planned tournaments for Sentinels Valorant")
    
    
    return(embed)

  except Exception as e:
    print(e)
    
    return("There are currently no planned tournaments for Sentinels Valorant")

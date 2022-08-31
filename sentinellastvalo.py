#imports
from bs4 import BeautifulSoup as soup
from dotenv import load_dotenv
load_dotenv()
import requests

def sentinellastvalo(url):
  try:
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
    base_url = 'https://www.vlr.gg'
    og_url = url
    og_page = requests.get(og_url, headers=headers)

    # Get the last match link
    page_soup2 = soup(og_page.text, "html.parser")
    match_link = page_soup2.find("a", {"class": "wf-card fc-flex m-item"})['href']
    last_match = base_url + match_link

    # Get the match page
    match_page = requests.get(last_match, headers=headers)
    match_html = soup(match_page.text, "html.parser")
    
    team1_html = match_html.find("div", {"class": "match-header-link-name mod-1"})
    team2_html = match_html.find("div", {"class": "match-header-link-name mod-2"})
    score_container = match_html.find_all("div", {"class": "match-header-vs-score"})
    maps_container = match_html.find_all("div", {"class": "vm-stats-game-header"})    
    team1 = team1_html.find_next().string.strip()
    team2 = team2_html.find_next().string.strip()

    score_html = score_container[1].find_all("span")
    team1_score = score_html[0].string.strip()
    team2_score = score_html[2].string.strip()

    maps_result = ""
    i = 0
    for map in maps_container:
      map_name = map.find("div", {"class": "map"}).find_next("span").next_element.strip()
      map_scores = map.find_all("div", {"class": "score"})
      team1_map_score = map_scores[0].string
      team2_map_score = map_scores[1].string
      if i == 0:
        maps_result = maps_result + f'{map_name} (||{team1} {team1_map_score} - {team2_map_score} {team2}||)'
      else:
        maps_result = maps_result + f', {map_name} (||{team1} {team1_map_score} - {team2_map_score} {team2}||)'
      i = i + 1
    
      
    message = f'The results for: {team1} vs {team2} - ||{team1} {team1_score} vs {team2_score} {team2}||, results on maps were: {maps_result}'

    return(message)
  
  except Exception as e:
    print(e)
    return("No Maps Found")
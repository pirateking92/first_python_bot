import requests
from bs4 import BeautifulSoup
import pandas as pd




url = "https://myanimelist.net/topanime.php?type=airing"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.text, 'html.parser')

# Find all anime listings
listings = soup.find_all('tr', class_='ranking-list')

# loop through all the elements I want (title, score) and print them to the terminal
def req_scrape():
    data = ""
    for listing in listings:
        title = listing.find('h3', class_='fl-l fs14 fw-b anime_ranking_h3').text.strip()
        score = listing.find('div', class_='js-top-ranking-score-col di-ib al').text.strip()
        data += f"{title}: {score}\n"
    return data
    
req_scrape()

# Assuming 'listings' is defined somewhere before this function call



# data = []

# proceed = True

# while(proceed):
  

      
      
# df = pd.DataFrame(data)
# df('top_airing_anime.csv', index=False)

# print("anime file created")
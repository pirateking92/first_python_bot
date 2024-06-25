import requests
from bs4 import BeautifulSoup
import pandas as pd



current_page = 1

data = []

proceed = True



while(proceed):
    print("Currently scraping bro: "+str(current_page))
    url = "https://books.toscrape.com/catalogue/page-"+str(current_page)+".html"

    res = requests.get(url)
    
    soup = BeautifulSoup(res.text, 'html.parser')
    
    if soup.title.text == "404 Not Found":
        proceed = False
    else:
        all_books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        
        for book in all_books:
            item = {}
            
            item['Title'] = book.find("img").attrs["alt"]
            
            item['Link'] = book.find("a").attrs["href"]
            
            item['Price'] = book.find("p", class_="price_color").text[2:]
            
            item['Stock'] = book.find("p", class_="instock availability").text.strip()
            
            data.append(item)
    
    current_page += 1


df = pd.DataFrame(data)
df.to_csv("books.csv")

















# movies = []

# for row in soup.select('tbody.lister-list tr'):
#     title = row.find('td', class_="titleColumn").find('a').get_text()
#     year = row.find('td', class_="titleColumn").find('span', class_='secondaryInfo').getText()[1:-1]
#     rating = row.find('td', class_="ratingColumn imdbRating").find('strong').get_text()
#     movies.append([title, year, rating])
    
# # store the information in a pandas dataframe
# df = pd.DataFrame(movies, columns=['Title', 'Year', 'Rating'])

# # add a delay between requests to avoid overwhelming the website with requests
# time.sleep(1)

# # Export the data to a CSV file
# df.to_csv('top-rated-movies.csv', index=False)
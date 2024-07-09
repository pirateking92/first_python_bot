import requests
import json
from bs4 import BeautifulSoup as bs

url = "https://api.mangadex.org/at-home/server/b7136bc8-7100-43a2-a861-8fcc5f255ff8"

res = requests.get(url)
print(res)

json_data = res.json()
readable_json = json.dumps(json_data, indent=4)
print(readable_json)

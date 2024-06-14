import requests
from bs4 import BeautifulSoup


# Making a GET request
r = requests.get('https://www.geeksforgeeks.org/python-programming-language/')

# check status code for response received
# success code - 200
print(r)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')

s = soup.find('div', class_='text')

# Check if 's' is not None
if s:
    content = s.find_all('p')
    print(content)
else:
    print("The specified div was not found.")

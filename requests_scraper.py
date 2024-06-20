import requests

# Making a GET request
r = requests.get('https://www.google.com')

# check status code for response received
# success code - 200
print(r)

# print content of request
print(r.content)


# uses basic parsing to get all the data from the website.
# i think this also can also do other http functions like post, put, delete
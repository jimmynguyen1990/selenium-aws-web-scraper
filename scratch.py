import requests
from bs4 import BeautifulSoup

WEBSITE_URL = 'https://www.freeconferencealerts.com/topicevent/human-rights'

response = requests.get(WEBSITE_URL)
doc = BeautifulSoup(response.text, 'html.parser')
conferences_divs = doc.find_all('div', {'class': 'conf-event-right'})
print(len (conferences_divs))

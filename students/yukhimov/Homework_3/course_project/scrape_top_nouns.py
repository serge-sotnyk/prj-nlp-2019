from bs4 import BeautifulSoup
import requests

URL = 'https://www.talkenglish.com/vocabulary/top-1500-nouns.aspx'

response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")
cells = soup.find_all('td')

with open('top_nouns.txt', "w") as output_file:
    for word in cells:
        try:
            noun = word.find('a').text.strip()
            output_file.write(noun + '\n')
        except AttributeError:
            pass

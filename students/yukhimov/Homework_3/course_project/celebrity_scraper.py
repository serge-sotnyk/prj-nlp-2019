from bs4 import BeautifulSoup
import requests

page_number = 0
page_link = 'https://www.famousfix.com/list/english-celebrities?pageno={}'

with open('english_celebrities.txt', "w") as output_file:
    while True:
        page_number += 1
        link = page_link.format(page_number)
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        names = soup.find_all('span', {'class': 'font16 text-content t-cb'})
        if names:
            for name in names:
                output_file.write(name.text.strip() + '\n')
        else:
            break



from bs4 import BeautifulSoup
import requests

URL = 'http://forum.lvivport.com/forums/velodorizhka.92/'
HOST_NAME = 'http://forum.lvivport.com/'


def find_pages_number(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    page = soup.find('div', {'class': 'PageNav'})
    return int(page['data-last'])


def scrape_section():
    with open('posts.txt', "w") as output_file:
        pages_number = find_pages_number(url=URL)
        for number in range(1, pages_number + 1):
            if number == 1:
                url = URL
            else:
                url = URL + 'page-{}'.format(number)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            titles = soup.find_all('h3', {'class': 'title'})
            for title in titles:
                link = title.find('a')
                full_link = HOST_NAME + link['href']
                try:
                    title_pages_number = find_pages_number(full_link)
                except TypeError:
                    title_pages_number = 1
                for title_page_number in range(1, title_pages_number + 1):
                    if title_page_number == 1:
                        url = full_link
                    else:
                        url = full_link + 'page-{}'.format(title_page_number)
                    response = requests.get(url)
                    soup = BeautifulSoup(response.text, "html.parser")
                    posts = soup.find_all('div', {'class': 'messageContent'})
                    for post in posts:
                        output_file.write(post.text)


if __name__ == '__main__':
    scrape_section()
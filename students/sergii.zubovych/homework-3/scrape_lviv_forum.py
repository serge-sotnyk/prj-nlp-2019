from bs4 import BeautifulSoup
import requests
import re
import json

class Topic:
    def __init__(self, href, title, create_date, creator, posts_num, views_num, last_update_date, last_updater):
        self.href = href
        self.title = title
        self.create_date = create_date
        self.creator = creator
        self.posts_num = posts_num
        self.views_num = views_num
        self.last_update_date = last_update_date
        self.last_updater = last_updater
        self.posts = []

    def add_posts(self, posts):
        self.posts.extend(posts) 

    def clear_posts(self):
        self.posts = []     


class Post:
    def __init__(self, href, create_date, creator, likes_num, content):
        self.href = href
        self.create_date = create_date
        self.creator = creator
        self.likes_num = likes_num
        self.content = content

class TopicEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Topic) or isinstance(obj, Post):
            return obj.__dict__
        return json.JSONDecoder.default(self, obj)    


def get_html(url):
    response = requests.get(url)
    return response.text

def get_topics(url):
    
    soup = BeautifulSoup(get_html(url), 'lxml')
    
    summary = re.match(r'Показано теми з \d+ по \d+ з (\d+)',soup.find('span', class_ = 'contentSummary').text)
    topics_num = int(summary.group(1))
    page_num = 1

    topics = []
    
    soup = BeautifulSoup(get_html(url), 'lxml')

    while topics_num > 0:            
        topics_list = soup.find('ol', class_ = 'discussionListItems').find_all('li')
        
        for item in topics_list:

            title_div = item.find('div', class_ = 'titleText')
            creator = title_div.find('a', class_ = 'username').get("href")
            a = title_div.find('h3', class_ = 'title').find('a')
            href = a.get('href')
            title = a.text
            create_date = title_div.find('span', class_ = 'DateTime').text

            stats_div = item.find('div', class_ = 'listBlock stats pairsJustified')
            posts_num = int(stats_div.find('dl', class_ = 'major').find('dd').text) + 1
            views_num = stats_div.find('dl', class_ = 'minor').find('dd').text

            last_info_div = item.find('div', class_ = 'listBlock lastPost')
            last_updater = last_info_div.find('a', class_ = 'username').get('href')
            last_update_date = last_info_div.find('span', class_ = 'DateTime').text

            topics.append(Topic(href, title, create_date, creator, posts_num, views_num, last_update_date, last_updater))
            topics_num -= 1
        
        page_num += 1
        soup = BeautifulSoup(get_html(url + 'page-' + str(page_num)), 'lxml')
    
    return topics

def get_topic_posts(url, posts_num):
    soup = BeautifulSoup(get_html(url), 'lxml')

    posts = []

    page_num = 1

    while posts_num > 0:

        post_items = soup.find('ol', class_ = 'messageList').find_all('li', id = re.compile('post.*'))
        
        for item in post_items:
            href = item.find('div', class_ = 'publicControls').find('a').get('href')
            content = str(item.find('div', class_ = 'messageContent').find('article').contents)

            private_controls_div = item.find('div', class_ = 'privateControls')
            create_date = private_controls_div.find('span', class_ = 'DateTime').text 
            creator = private_controls_div.find('a', class_ = 'username author').get('href')
            
            likes = item.find('ul', class_ = 'dark_postrating_outputlist')
            likes_num = 0
            if likes:
                likes_num = likes.find('li').find('strong').text
        
            posts.append(Post(href, create_date, creator, likes_num, content))
            posts_num -= 1
        
        page_num += 1
        soup = BeautifulSoup(get_html(url + 'page-' + str(page_num)), 'lxml')

    return posts


def main():
    
    main_url = 'http://forum.lvivport.com/'
    forum_href = 'forums/restoranna-kritika.91/'
    
    topics = get_topics(main_url + forum_href)
    
    with open('lviv-forum.json', 'w') as output:
        
        output.write("[\n")
        
        for topic in topics:
            posts = get_topic_posts(main_url + topic.href, topic.posts_num)
            topic.add_posts(posts)
            output.write(json.dumps(topic, cls = TopicEncoder, ensure_ascii= False, indent = 2))
            topic.clear_posts()
            output.write(",\n")
        
        output.write("]")    


if __name__ == "__main__":
    main()

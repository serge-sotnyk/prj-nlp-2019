import scrapy
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class LvivForumSpider(scrapy.Spider):
    name = "posts"
    base_url = 'http://forum.lvivport.com/'

    def start_requests(self):
        urls = [
            self.base_url + 'forums/muzika.8/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        result = []

        result.extend(self._parse_index(response))

        next_page = response.xpath('//link[@rel="next"]/@href').get()
        if next_page is not None:
            next_page = self.base_url + next_page
            result.append(scrapy.Request(next_page, callback=self.parse))

        return result

    def _parse_index(self, response):
        page = BeautifulSoup(response.body, 'html.parser')
        for t in page.find_all(attrs={"class": "PreviewTooltip"}):
            thread_page_url = self.base_url + t['href']
            yield scrapy.Request(url=thread_page_url, callback=self._parse_thread)

    def _parse_thread(self, response):
        page = BeautifulSoup(response.body, 'html.parser')
        thread_name = self._parse_thread_name(response.url)
        self.logger.info('Parse thread {}'.format(thread_name))
        self._save_page(thread_name, page)

        next_page = response.xpath('//link[@rel="next"]/@href').get()
        if next_page is not None:
            next_page = self.base_url + next_page
            yield scrapy.Request(next_page, callback=self._parse_thread)

    def _save_page(self, name, page):
        users = page.find_all(attrs={"class": "username"})
        posts = page.find_all(attrs={"class": "messageContent"})
        result = []
        for user, post in zip(users, posts):
            if user and post:
                result.append('<USER>{}</USER>\n'
                              '<POST>\n{}\n</POST>'
                              .format(self._clean_text(user.text),
                                      self._clean_text(post.text)))

        result = '\n'.join(result)
        with open('./forum/' + name, 'a+') as f:  # thread is parsed in several requests, I'll have to append to a file
            f.write(result + '\n')

    # todo add better cleaning
    def _clean_text(self, text):
        ad_text = '(adsbygoogle = window.adsbygoogle || []).push({});'
        text = text.replace(ad_text, '')
        return text.strip()

    def _parse_thread_name(self, url):
        path = urlparse(url).path
        for part in path.split('/'):
            if '.' in part:
                return part.split('.')[0]

import scrapy
from bs4 import BeautifulSoup


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
        self.logger.critical('Parse thread {}'.format(page.title.text))
        self._save_page(page.title.text, page)

        # as thread is not taken in one request, I'll have to add writes to a file
        # here can return next page of current thread. Maybe can pass page name / file name to callback
        next_page = response.xpath('//link[@rel="next"]/@href').get()
        if next_page is not None:
            next_page = self.base_url + next_page
            yield scrapy.Request(next_page, callback=self._parse_thread)

    # fix how posts and users are parsed, cleaned etc
    # use some identifiers instead of page names as file names
    def _save_page(self, name, page):
        users = page.find_all(attrs={"class": "username"})
        posts = page.find_all(attrs={"class": "messageContent"})
        result = []
        for user, post in zip(users, posts):
            result.append({"user": user.text, "post": post.text})
        with open(name, 'w') as f:
            # f.write(page_text)
            for r in result:
                f.write(r["user"].strip())
                f.write('\t')
                f.write(r["post"].strip()[0:50])
                f.write('\n')



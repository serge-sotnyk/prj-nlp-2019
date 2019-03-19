import scrapy
import re


class LvivForumSpider(scrapy.Spider):
    """
    Crawles "Велодоріжка"(http://forum.lvivport.com/forums/velodorizhka.92/) thread of
    http://forum.lvivport.com/
    """

    name = 'rowerspider'

    start_urls = ['http://forum.lvivport.com/forums/velodorizhka.92/']

    custom_settings = {
        'DOWNLOAD_DELAY': 1.0,
    }

    def parse(self, response):
        description = response.css('p#pageDescription').get()
        if description.find('Розділ для і про велосипедистів та усіх кому не байдужий ровер') >= 0:
            yield from self.parse_main_list(response)
        elif description.find("""Тема у розділі '<a href="forums/velodorizhka.92/">Велодоріжка</a>'""") >= 0:
            yield from self.parse_topic_page(response)
        else:
            print(f"Unknown page type at url: {response.request.url}")

    def parse_topic_page(self, response):
        # get links to other pages of the same topic
        next_pages = response.css('span.pageNavHeader+nav>a::attr(href)').getall()
        for url in next_pages:
            yield response.follow(url, callback=self.parse)
        # store scraped messages
        messages = response.css('li.message')
        for message in messages:
            author = message.css('a.username::text').get()
            article = message.css('article').get()
            permalink = message.css('a.hashPermalink::attr(href)').get()
            if author is not None:
                yield {
                    'author': author,
                    'permalink': permalink,
                    'article': article,
                }

    def parse_main_list(self, response):
        # get links to page-nnn
        next_pages = response.css('nav>a').getall()
        for page in next_pages:
            if page.find('class=""') >= 0:
                match = re.search(r'href=[\'"]?([^\'" >]+)', page)
                if match:
                    url = match.group(1)
                    yield response.follow(url, callback=self.parse)

        # get links to threads
        thread_links = response.css('a.PreviewTooltip::attr(href)').getall()
        for url in thread_links:
            yield response.follow(url, callback=self.parse)

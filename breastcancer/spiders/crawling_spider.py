import scrapy
import json
from scrapy import Selector
from urllib.parse import urlencode
import config

# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor

API_KEY = config.api_key

def get_proxy_url(url):
    payload = {'api_key':API_KEY, 'url':url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' +urlencode(payload)
    return proxy_url

class TopicSpider(scrapy.Spider):
    name = "TopicCrawl"
    # allowed_domains = ["community.breastcancer.org/forum/78"]
    start_urls = ["https://community.breastcancer.org/forum/78/"]

    # rules = (
    #     Rule(LinkExtractor(allow="topics")),
    # )

    def parse(self, response):
        for post in response.css('ul.rowgroup.topic-list li'):
            yield{
                'link': "https://community.breastcancer.org" + post.css('a').attrib['href']
            }

        next_page = response.css('a.next_page').attrib['href']
        # page 545 is down for some random reason
        if next_page == "/forum/78?page=545":
            next_page = "/forum/78?page=546"
        if next_page is not None:
            link = "https://community.breastcancer.org" + next_page
            yield response.follow(link, callback=self.parse)


class MainPostSpider(scrapy.Spider):
    name = "MainPostCrawl"

    def start_requests(self):
        urls = []
    
        with open('output.json', 'r') as f:
            data = json.load(f)
            for item in data:
                urls.append(item['link'])

        for url in urls:
            yield scrapy.Request(url=get_proxy_url(url), callback=self.parse)

    
    def parse(self, response):
        page = response.css("div.container")
        title = page.css('h1::text').get()
        # Removing the "Topic: " from each title
        topic = title[7:]

        org_post =  response.css("div.original-topic")
        text = str(org_post.css("div.user-post").get())
        specific_index = text.find("<span class=\"line\">")


        details = ""

        # The user has specific details about their condition attached to their post
        if specific_index != -1:
            temp_html_text = text[specific_index:]
            sel = Selector(text=temp_html_text)
            temp = sel.xpath('//text()').extract()
            temp = ' '.join(temp)
            temp = temp.split()
            details = ' '.join(temp)

        text = text[:specific_index]
        sel = Selector(text=text)
        temp = sel.xpath('//text()').extract()
        temp = ' '.join(temp)
        temp = temp.split()
        text = ' '.join(temp)

        text = text.replace(" Log in to post a reply", "")
        details = details.replace(" Log in to post a reply", "")

        start = text.index("wrote:")
        post_data = text[:start - 1]
        post = text[start + 7:]
        yield {
            'Title': topic,
            'Post-Data': post_data,
            "Post": post,
            'Details': details
        }
    

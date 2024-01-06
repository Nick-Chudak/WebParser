import scrapy


class ReutersarticlespiderSpider(scrapy.Spider):
    name = "reutersArticleSpider"
    allowed_domains = ["www.reuters.com"]
    start_urls = ["https://www.reuters.com/site-search/"]

    def parse(self, response):
        pass

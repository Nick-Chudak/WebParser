import scrapy


class ReutersspiderSpider(scrapy.Spider):
    name = "reutersspider"
    allowed_domains = ["reuters.com"]
    start_urls = ["https://www.reuters.com/"]

    def parse(self, response):
        print(dir(response))
        
        yield(response.url)

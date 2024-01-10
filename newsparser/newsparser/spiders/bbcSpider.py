import scrapy
from pathlib import Path

class BbcspiderSpider(scrapy.Spider):
    name = "bbcSpider"
    allowed_domains = ["www.bbc.com"]
    start_urls = ["https://www.bbc.com"]

    def parse(self, response):
        pass

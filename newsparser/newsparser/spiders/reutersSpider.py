import scrapy
import json

class ReutersSpider(scrapy.Spider):
    """
    A spider that crawls Reuters's list of article search results.
    """
    name = 'reuters'
    with open("newsparser/config/selectors_reuters.json") as selector_file:
        selectors = json.load(selector_file)
    
    def start_requests(self):
        pass

    def parse(self, response):
        pass

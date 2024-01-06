import scrapy
import os
from pathlib import Path
from urllib.parse import urlencode
import json

API_KEY = "3d9a1a8d-90dc-400f-8b40-b725eb54cab9"

def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


class ReutersspiderSpider(scrapy.Spider):
    name = "reuters"
    #allowed_domains = ["reuters.com"]
    with open("newsparser/config/selectors_reuters.json") as selector_file:
        selectors = json.load(selector_file)
    
    def __init__(self, search_extension = "", **kwargs):
        """
        Added the additional parameter to the Spider class
        """
        self.search_extension = search_extension.replace(" ", "+")
        super().__init__(**kwargs)


    def start_requests(self):
        # start_url = 'https://www.reuters.com/'
        start_url = "https://www.reuters.com/site-search/?query=" + self.search_extension
        yield scrapy.Request(url=get_proxy_url(start_url), callback=self.parse)


    def parse(self, response):
        # f = open("results.html", "w")
        # f.write(response.body)
        # f.close()
        # self.log(f"Saved file results.html")
        # print("----------------")
        Path('reuters.html').write_bytes(response.body)
        # titles = response.css("h3").getall()

        titles = [title for title in response.css(self.selectors["titles"]).getall()]
        urls = ["https://www.reuters.com" + url for url in response.css(self.selectors["urls"]).getall()]
        dates = [description for description in response.css(self.selectors["dates"]).getall()]
        topics = [metadata for metadata in response.css(self.selectors["topics"]).getall()]
        #Path("titles.txt").write_txt(titles)
        articles = []
        for title, url, date, topic in zip(titles, urls, dates, topics):
            article = {
                "title": title,
                "url": url,
                "date": date,
                "topic": topic,
            }
            articles.append(article)
        self.log(articles)

        with open("outfile", "w") as outfile:
            outfile.write("\n".join(articles))
            
        return articles
        #self.log(titles)
        #self.log(response.url)

        

        
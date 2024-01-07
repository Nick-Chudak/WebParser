import scrapy
import json
import os


def create_reuters_search_url(query):
   return f"https://www.reuters.com/site-search/?query={query.replace(' ', '+')}"

def create_scrapeops_url(url, js=False, wait=False):
    #key = os.getenv("3d9a1a8d-90dc-400f-8b40-b725eb54cab9")
    key = "3d9a1a8d-90dc-400f-8b40-b725eb54cab9"
    scraping_url = f"https://proxy.scrapeops.io/v1/?api_key={key}&url={url}"
    if js:
        scraping_url += "&render_js=true"
    if wait:
        scraping_url += f"&wait_for={wait}"
    return scraping_url

def get_urls_from_dict(list_of_dicts):
    urls = []
    for dict_with_url in list_of_dicts:
        if dict_with_url.get("url"):
            urls.append(dict_with_url.get("url"))
    return urls

def read_csv(csv_path: str):
    items = []
    with open(csv_path) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            items.append(row)
    return items



class ReutersSpider(scrapy.Spider):
    """
    A spider that crawls Reuters's list of article search results.
    """
    name = 'reutersSpider'
    
    http_user = "user"
    http_pass = "userpass"
    with open("newsparser/config/selectors_reuters.json") as selector_file:
        selectors = json.load(selector_file)
    
    def start_requests(self):
        start_urls = [
            create_scrapeops_url(create_reuters_search_url("ukraine war"), wait=False)
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        self.log(response.body)
        titles = [title for title in response.css(self.selectors["titles"]).getall()]
        urls = ["https://www.reuters.com" + url for url in response.css(self.selectors["urls"]).getall()]
        dates = [description for description in response.css(self.selectors["dates"]).getall()]
        topics = [metadata for metadata in response.css(self.selectors["topics"]).getall()]
        
        articles = []
        for title, url, date, topic in zip(titles, urls, dates, topics):
            article = {
                "title": title,
                "url": url,
                "date": date,
                "topic": topic,
            }
            articles.append(article)
        
        return articles

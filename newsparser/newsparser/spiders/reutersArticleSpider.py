import scrapy

def create_reuters_search_url(query):
    return f"https://www.reuters.com/site-search/?query={query.replace(' ', '+')}"

def create_scrapeops_url(url, js=False, wait=False):
    key = os.getenv("3d9a1a8d-90dc-400f-8b40-b725eb54cab9")
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

class ReutersarticlespiderSpider(scrapy.Spider):
    name = "reutersArticleSpider"
    allowed_domains = ["www.reuters.com"]
    start_urls = ["https://www.reuters.com/site-search/"]


    def start_requests(self):
        start_urls = get_urls_from_dict(read_csv(self.path_for_urls))
        for url in start_urls:
            yield scrapy.Request(url=create_scrapeops_url(url), callback=self.parse)
    
    def parse(self, response, **kwargs):
        title = clean(response.css(self.selectors["title"]).get(), remove_special=False)
        paragraphs = response.css(self.selectors["paragraphs"]).getall()
        text = " ".join([clean(paragraph) for paragraph in paragraphs])
        date = clean(response.css(self.selectors["date"]).get())
        author = clean(response.css(self.selectors["author"]).get())
        url = get_source_url_from_scraping_url(response.request.url)

        return {
            "title": title,
            "url": url,
            "date": date,
            "author": author,
            "text": text,
        }
   
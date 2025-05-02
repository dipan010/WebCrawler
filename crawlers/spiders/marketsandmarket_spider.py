import scrapy
from datetime import datetime
from crawlers.items import Item


class MarketsSpider(scrapy.Spider):
    name = "marketsandmarkets"
    allowed_domains = ["marketsandmarkets.com"]
    start_urls = [
        "https://www.marketsandmarkets.com/Market-Reports/supply-chain-management-market-190997554.html"
    ]

    def parse(self, response):
        item = Item()
        item["url"] = response.url
        item["title"] = response.css("h1::text").get()
        item["author"] = None  # No explicit author
        item["published"] = None  # No explicit publication date
        item["tags"] = response.css("meta[name='keywords']::attr(content)").get(default="").split(",")
        item["images"] = response.css("img::attr(src)").getall()
        item["content"] = response.css("div.content p::text, div.content span::text").getall()
        item["raw_html"] = response.text
        item["scraped_at"] = datetime.utcnow().isoformat()
        yield item
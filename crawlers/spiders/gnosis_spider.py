import scrapy
from datetime import datetime
from crawlers.items import Item

class GnosisFreightSpider(scrapy.Spider):
    name = "gnosisfreight"
    allowed_domains = ["gnosisfreight.com"]
    start_urls = ["https://www.gnosisfreight.com/"]

    custom_settings = {
        "PLAYWRIGHT_ENABLED": True,
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 60 * 1000,
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
    }

    def parse(self, response):
        links = response.css("aL:attr(href)").getall()
        for link in links:
            if link.startswith("/") and not any(x in link for x in["#", "mailto", "tel"]):
                yield response.follow(
                    link,
                    self.parse_article,
                    meta={"playwright": True}
                )
    
    def parse_article(self, response):
        item = Item()

        item["url"] = response.url
        item["title"] = response.css("h1::text, title::text").get()
        item["author"] = None
        item["published"] = None
        item["tags"] = []
        item["images"] = response.css("img::attr(src)").getall()
        item["content"] = response.css("main *::text, body *::text").getall()
        item["raw_html"] = response.text
        item["scraped_at"] = datetime.utcnow().isoformat()

        yield item
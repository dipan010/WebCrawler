import scrapy 
from datetime import datetime
from crawlers.items import Item

class LeadIQSpider(scrapy.Spider):
    name = "leadiq"
    allowed_domains = ["leadiq.com"]
    start_urls = ["https://leadiq.com/c/gnosis-freight/5fcf6529a856d346f831079f"]

    custom_settings = {
        "PLAYWRIGHT_ENABLED": True,
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 60 * 1000,
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
    }

    def parse(self, response):
        item = Item()
        item["url"] = response.url
        item["title"] = response.css("h1::text").get() or "Gnosis Freight - LeadIQ"
        item["author"] = None
        item["published"] = None
        item["tags"] = response.css("a::text").getall()  # fallback
        item["images"] = response.css("img::attr(src)").getall()
        item["content"] = response.css("body *::text").getall()
        item["raw_html"] = response.text
        item["scraped_at"] = datetime.utcnow().isoformat()
        yield item
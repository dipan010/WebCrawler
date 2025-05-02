import scrapy
from datetime import datetime
from crawlers.items import Item

class G2Spider(scrapy.Spider):
    name = "g2"
    allowed_domains = ["g2.com"]
    start_urls = ["https://www.g2.com/categories"]

    custom_settings = {
        "PLAYWRIGHT_ENABLED": True,
        "PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT": 60 * 1000,
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
    }

    def parse(self, response):
        listings = response.css("div.product-list div.product-list-item")
        for listing in listings:
            item = Item()
            item["url"] = response.url
            item["title"] = listing.css("h3 a::text").get()
            item["author"] = None
            item["published"] = None
            item["tags"] = listing.css("a.tag::text").getall()
            item["images"] = listing.css("img::attr(src)").getall()
            item["content"] = listing.css("div.text-truncate::text").getall()
            item["raw_html"] = listing.get()
            item["scraped_at"] = datetime.utcnow().isoformat()
            yield item

        #paginate if there's a 'next' button
            
        next_page = response.css("a[rel='next']::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback= self.parse, meta={"playwright": True})
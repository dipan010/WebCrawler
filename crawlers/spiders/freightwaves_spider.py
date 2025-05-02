import scrapy
from datetime import datetime
from crawlers.items import Item

class FreightWavesSpider(scrapy.Spider):
    name = "freightwaves"
    allowed_domains = ["freightwaves.com"]
    start_urls = ["https://www.freightwaves.com/news"]

    def parse(self, response):
        article_links = response.css('a::attr(href)').getall()
        for link in article_links:
            if link.startswith("/") and "/news/" in link:
                full_url = response.urljoin(link)
                yield scrapy.Request(full_url, callback=self.parse_article)

    def parse_article(self, response):
        item = Item()
        item["url"] = response.url
        item["title"] = response.css("h1::text").get()
        item["author"] = response.css('a.author::text').get()
        item["published"] = response.css("time::attr(datetime)").get()
        item["tags"] = response.css("a[rel='tag']::text").getall()
        item["images"] = response.css("article img::attr(src)").getall()
        item["content"] = response.css("article *::text").getall()
        item["raw_html"] = response.text
        item["scraped_at"] = datetime.utcnow().isoformat()
        yield item

import scrapy
from datetime import datetime
from crawlers.items import Item

class theLogicsticsSpider(scrapy.Spider):
    name = "theLogistics"
    allowed_domains = ["thelogisticsoflogistics.com"]
    start_urls = ["https://www.thelogisticsoflogistics.com"]

    def parse(self, response):
        article_links = response.css('a::attr(href)').getall() #collect all the links to the articles present on the homepage
        for link in article_links:
            yield response.follow(link, self.parse_article)

    def parse_article(self, response):
        item = Item()

        item["url"] = response.url
        item["title"] = response.css("h1.entry-title::text").get()
        item["author"] = response.css("span.author.vcard a::text").get()
        item["published"] = response.css("time.entry-date::attr(datetime)").get()
        item["tags"] = response.css("span.cat-links a::text").getall()
        item["images"] = response.css("div.entry-content img::attr(src)").getall()
        item["content"] = response.css("div.entry-content *::text").getall()
        item["raw_html"] = response.text
        item["scraped_at"] = datetime.utcnow().isoformat()
        item["source"] = "thelogistics"

        yield item
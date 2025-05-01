import scrapy
from datetime import datetime
from urllib.parse import urljoin

class theLogicsticsSpider(scrapy.Spider):
    name = "theLogistics"
    allowed_domains = ["thelogisticsoflogistics.com"]
    start_urls = ["https://www.thelogisticsoflogistics.com/blog"]

    def parse(self, response):
        article_links = response.css('h2.entry-title a::attr(href)').getall()

        for link in article_links:
            yield response.follow(link, self.parse_article)

        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        title = response.css('h1.entry-title::text').get()
        author = response.css('span.author.vcard a::text').get()
        published_date = response.css('time.entry-date::attr(datetime)').get()

        content = response.css('div.entry-content').get()
        images = response.css('div.entry-content img::attr(src)').getall()
        tags = response.css('span.cat-links a::text').getall()

        yield {
            "url": response.url,
            "title": title,
            "author": author,
            "published": published_date,
            "tags": tags,
            "images": images,
            "content": response.css('div.entry-content *::text').getall(),
            "raw_html": response.text,
            "scraped_at": datetime.utcnow().isoformat()
        }
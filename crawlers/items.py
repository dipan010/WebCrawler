import scrapy

class Item(scrapy.item):
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    published = scrapy.Field()
    tags = scrapy.Field()
    images = scrapy.Field()
    content = scrapy.Field()
    raw_html = scrapy.Field()
    scraped_at = scrapy.Field()
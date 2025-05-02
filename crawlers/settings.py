BOT_NAME = "crawlers"

SPIDER_MODULES = ["crawlers.spiders"]

ROBOTSTXT_OBEY = True #obeys robots.txt(ethical scraping)

DOWNLOAD_DELAY = 2
AUTOTHROTTLE_ENABLED = True

LOG_LEVEL = "INFO"
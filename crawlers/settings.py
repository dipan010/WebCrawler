BOT_NAME = "crawlers"

SPIDER_MODULES = ["crawlers.spiders"]

ROBOTSTXT_OBEY = True #obeys robots.txt(ethical scraping)

DOWNLOAD_DELAY = 10
AUTOTHROTTLE_ENABLED = True

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
PLAYWRIGHT_BROWSER_TYPE = "chromium"

LOG_LEVEL = "INFO"
import scrapy
# Quotes to Scrape - JavaScript Rendered Page
# Tech: Scrapy, Playwright (headless browser)
# Output: quotes and authors from JS-rendered content


class QuotesJsSpider(scrapy.Spider):
    name = "quotes_js"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/js"]

    def start_requests(self):
        yield scrapy.Request(
            url="https://quotes.toscrape.com/js",
            meta={"playwright": True},
            callback=self.parse
        )

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            yield {
                'quote': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first()
            }

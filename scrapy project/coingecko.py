import scrapy
import json
# CoinGecko Cryptocurrency Data Scraper
# Tech: Scrapy, JSON API
# Output: coins.csv (name, current price, 24h price change)


class CoingeckoSpider(scrapy.Spider):
    name = "coingecko"
    allowed_domains = ["api.coingecko.com"]
    start_urls = ["https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1"]

    def parse(self, response):
        all_currency = response.json()
        for coin in all_currency:
            name = coin['name']
            current_price = coin['current_price']
            price_change_percentage_24h = coin['price_change_percentage_24h']
            yield {'name':name,
                   'current_price':current_price,
                   'price_change_percentage_24h':price_change_percentage_24h}

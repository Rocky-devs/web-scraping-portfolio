import scrapy
# Douban Top 250 Movies Scraper
# Tech: Scrapy, CSS Selectors, Pagination
# Output: movies.csv (title, rating, director, rank, quote)
class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/top250?start=0&filter="]

    def parse(self, response):
        movies = response.css('ol.grid_view li')
        for movie in movies:
            title = movie.css('span.title::text').extract_first()
            rating = movie.css('span.rating_num::text').extract_first()
            director = movie.css('div.bd p::text').getall()[0].split('主演')[0].strip()
            rank = movie.css('div.pic em::text').extract_first()
            quote = movie.css('p.quote span::text').extract_first()
            yield {'title': title, 'rating': rating,'director': director, 'rank': rank, 'quote': quote}

        next_href = response.css('span.next a::attr(href)').get()
        if next_href:
            next_start = 'https://movie.douban.com/top250' + next_href
            yield scrapy.Request(url=next_start,callback=self.parse)



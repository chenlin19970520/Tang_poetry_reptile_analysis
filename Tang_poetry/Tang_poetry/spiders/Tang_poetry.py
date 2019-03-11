import scrapy  # 引入爬虫scrapy模块
from urllib.parse import unquote  # 引入转换decodeURI
from Tang_poetry.items import TangPoetryItem


class TangSpider(scrapy.Spider):
    name = 'Tang_poetry'
    start_urls = [
        'https://so.gushiwen.org/authors/Default.aspx?p=1&c=唐代'
    ]

    def parse(self, response):
        names = response.css(".left .sonspic .cont b::text").extract()
        contents = response.css(
            ".left .sonspic .cont p:last-of-type::text").extract()
        next_url = response.css(".pagesright .amore::attr(href)").extract()[0]
        next_url = unquote(next_url)
        if next_url is not None:
            yield response.follow(next_url, callback=self.parse)
        print(names)
        print(contents)

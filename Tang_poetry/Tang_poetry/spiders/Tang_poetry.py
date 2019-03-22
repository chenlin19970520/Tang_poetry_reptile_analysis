import scrapy  # 引入爬虫scrapy模块
from urllib.parse import unquote  # 引入转换decodeURI
from Tang_poetry.items import TangPoetryItem  #
# from pymongo import MongoClient #引入mongodb

class TangSpider(scrapy.Spider):
    name = 'Tang_poetry'
    start_urls = [
        'https://so.gushiwen.org/authors/Default.aspx?p=1&c=唐代'
    ]
    def parse(self, response):
        item = TangPoetryItem()
        user = response.xpath("//div[@class='sonspic']")
        for it in user:
            item['author']= it.xpath(".//div[@class='cont']//p//b//text()").extract()
            item['content']=it.xpath(".//div[@class='cont']//p[last()]//text()").extract()[0]
            yield item
        # names = response.css(".left .sonspic .cont b::text").extract()

        # contents = response.css(
        #     ".left .sonspic .cont p:last-of-type::text").extract()
            # db.post.insert({name:names,contents:contents})
        next_url = response.xpath("//a[@class='amore']//@href").extract()[0]
        print(next_url)
        next_url = unquote(next_url)
        if next_url is not None:
            yield response.follow(next_url, callback=self.parse)


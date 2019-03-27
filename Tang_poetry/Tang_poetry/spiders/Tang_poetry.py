import scrapy  # 引入爬虫scrapy模块
from urllib.parse import unquote  # 引入转换decodeURI
from Tang_poetry.items import TangPoetryItem  #
import re
# from pymongo import MongoClient #引入mongodb

class TangSpider(scrapy.Spider):
    name = 'Tang_poetry'
    start_urls = [
        'http://www16.zzu.edu.cn/qtss/zzjpoem1.dll/query'
    ]
    def parse(self, response):
        allInfo = response.xpath("//span//@href").extract()
        print(allInfo)
        for itInfo in allInfo:
            yield scrapy.Request(itInfo,self.parse_v)


    def parse_v(self,response):
        allPoetry = response.xpath("//span//@href").extract()
        print(allPoetry)
        for itPoetry in allPoetry:
            yield scrapy.Request(itPoetry,self.parse_p)
        next_text = response.xpath("//table//tr//td//p//a//text()").extract()[2]
        next_url = response.xpath("//table//tr//td//p//a//@href").extract()[2]
        if next_text == '下页':
            yield response.follow(next_url,self.parse_v)

    def parse_p(self,response):
        item = TangPoetryItem()
        title = response.xpath("//table//tr//td//p//font").extract()[2]
        author = response.xpath("//table//tr//td//p//font").extract()[3]
        works  = response.xpath("//table//tr//td//p//font").extract()[4]
        msg = '<br>|\xa0|<font.*?>|</font>|<u>|</u>'
        item['title'] = re.sub(msg,'',title)
        item['author'] = re.sub(msg,'',author)
        item['works'] = re.sub(msg,'',works)
        yield item
        # for it in user:
        #     item['author']= it.xpath(".//div[@class='cont']//p//b//text()").extract()
        #     item['content']=it.xpath(".//div[@class='cont']//p[last()]//text()").extract()[0]
        #     works_url = it.xpath(".//div[@class='cont']//p[last()]//a//@href").extract()[0]
        #     if works_url is not None:
        #         request = scrapy.Request(works_url,self.parse_work)
        #         request.meta['work'] = item
        #         yield request
            # print(works_url)
            # return

            # yield item
        # names = response.css(".left .sonspic .cont b::text").extract()

        # contents = response.css(
        #     ".left .sonspic .cont p:last-of-type::text").extract()
            # db.post.insert({name:names,contents:contents})
        # next_url = response.xpath("//a[@class='amore']//@href").extract()[0]
        # print(next_url)
        # next_url = unquote(next_url)
        # if next_url is not None:
        #     yield response.follow(next_url, callback=self.parse)
    # def parse_work(self,response):
    #     item.response.meta['work']
        


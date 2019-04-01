import scrapy  
from urllib.parse import unquote  
from Tang_poetry.items import TangPoetryItem  
import re

class TangSpider(scrapy.Spider):
    name = 'Tang_poetry'
    start_urls = [
        'http://www16.zzu.edu.cn/qtss/zzjpoem1.dll/query'
    ]
    def parse(self, response):
        allInfo = response.xpath("//span//@href").extract()
        for itInfo in allInfo:
            yield scrapy.Request(itInfo,self.parse_v)

    def parse_v(self,response):
        allPoetry = response.xpath("//span//@href").extract()
        for itPoetry in allPoetry:
            yield scrapy.Request(itPoetry,self.parse_p)
        textAll = response.xpath("//table//tr//td//p//a//text()").extract()
        urlAll = response.xpath("//table//tr//td//p//a//@href").extract()
        next_text = textAll[len(textAll)-2]
        next_url = urlAll[len(urlAll)-2]
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
        


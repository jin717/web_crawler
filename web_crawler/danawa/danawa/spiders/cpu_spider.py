import scrapy
from scrapy.selector import Selector
from selenium import webdriver
import time
from danawa.items import DanawaCpuItem
import datetime as d


class cpu_spider(scrapy.Spider):
    name = 'danawa_cpu'
    allowed_domain = ['shop.danawa.com']
    start_urls = [
        'http://shop.danawa.com/main/?controller=goods&methods=index&productRegisterAreaGroupSeq=20&serviceSectionSeq=594',
    ]

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.driver = webdriver.Chrome("C:/Users/jin/chromedriver")

    def parse(self, response):
        browser = self.driver
        browser.get(response.url)
        time.sleep(5)

        div = browser.find_element_by_xpath('//*[@id="productListContainer"]/div').get_attribute('outerHTML')
        selector = Selector(text=div)
        rows = selector.xpath("//li[@class='prod_item']")

        for row in rows:
            item  = DanawaCpuItem()
            item['name'] = row.xpath(".//div[@class='head_info']/a/strong/text()")[0].extract()
            item['price'] = ''.join(row.xpath("//li[@class='prod_item']//span[@class='num']/text()")[0].extract().split(','))
            item['reg_date'] = row.xpath(".//dl[@class='meta_item mt_date']/dd/text()")[0].extract()
            item['crawled_date'] = d.datetime.now()
            yield item


        self.driver.close()

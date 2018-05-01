# coding:utf-8

import scrapy
from AQI.items import AqiItem


class AqiSpider(scrapy.Spider):
    name = 'aqi'
    allowed_domains = ['aqistudy.cn']
    base_url = "https://www.aqistudy.cn/historydata/"
    start_urls = [base_url]

    def parse(self, response):
        city_link_list = response.xpath("//ul[@class='unstyled']/div/li/a/@href").extract()[10:11]

        for link in city_link_list:
            yield scrapy.Request(self.base_url + link, callback=self.parse_month)

    def parse_month(self, response):
        month_link_list = response.xpath("//ul[@class='unstyled1']/li/a/@href").extract()[10:12]

        for link in month_link_list:
            yield scrapy.Request(self.start_urls + link, callback=self.parse_day)

    def parse_day(self, response):
        node_list = response.xpath("//div[@class='row']//tbody/tr")
        node_list.pop()

        for node in node_list:
            item = AqiItem()
            item["date"] = node.xpath("./td[1]//text()").extract_first()
            item["aqi"] = node.xpath("./td[2]//text()").extract_first()
            item["level"] = node.xpath("./td[3]//text()").extract_first()
            item["pm2_5"] = node.xpath("./td[4]//text()").extract_first()
            item["pm10"] = node.xpath("./td[5]//text()").extract_first()
            item["so2"] = node.xpath("./td[6]//text()").extract_first()
            item["co"] = node.xpath("./td[7]//text()").extract_first()
            item["no2"] = node.xpath("./td[8]//text()").extract_first()
            item["o3"] = node.xpath("./td[9]//text()").extract_first()

            yield item
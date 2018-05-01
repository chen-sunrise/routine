# -*- coding: utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spider import CrawlSpider, Rule
from Tencent.items import TencentItem, PositionItem

import logging

class TencentCrawlSpider(CrawlSpider):
    name = 'tencent_crawl'
    allowed_domains = ['hr.tencent.com']
    # 1.程序的入口，scrapy发送start_urls的请求，并返回响应
    # 这个响应只会传给rules进行提取链接
    start_urls = ["https://hr.tencent.com/position.php?&start=0"]

    rules = (
        # start_urls里的response到这里:
        # 1. 通过LinkExtractor提取链接，并通过Rule发送请求
        # 2. 通过Rule发送的请求返回的响应，会交给callback进行解析，并继续跟进提取
        Rule(LinkExtractor(allow=r'position\.php\?&start=\d+'), callback='parse_item', follow= True),
        Rule(LinkExtractor(allow=r"position_detail\.php\?id=\d+"), callback='parse_position', follow=False)
    )

    def parse_item(self, response):
        logging.warning('响应的url地址：' + response.url)
        logging.info('响应的url地址：' + response.url)
        logging.debug('响应的url地址：' + response.url)
        # logging.log(logging.WARNING, "响应的url地址:" + response.url)
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")

        for node in node_list:
            item = TencentItem()
            item['position_name'] = node.xpath("./td[1]/a/text()").extract_first()
            item['position_link'] = node.xpath("./td[1]/a/@href").extract_first()
            item['position_type'] = node.xpath("./td[2]/text()").extract_first()
            item['people_number'] = node.xpath("./td[3]/text()").extract_first()
            item['work_location'] = node.xpath("./td[4]/text()").extract_first()
            item['publish_times'] = node.xpath("./td[5]/text()").extract_first()

            yield item

    def prase_position(self, response):
        # item = response.meta['content']
        item = PositionItem()
        item['position_link'] = response.url
        item['position_zhize'] = '; '.join(response.xpath("//ul[@class='squareli']")[0].xpath("./li/text()").extract())
        item["position_yaoqiu"] = "; ".join(response.xpath("//ul[@class='squareli']")[1].xpath("./li/text()").extract())

        yield item
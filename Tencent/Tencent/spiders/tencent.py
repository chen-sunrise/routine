# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem
from Tencent.items import PositionItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    start_urls = ["https://hr.tencent.com/position.php?start=" + str(page) for page in range(0, 4018, 10)]

    def parse(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")

        for node in node_list:
            item = TencentItem()
            item['position_name'] = node.xpath("./td[1]/a/text()").extract_first()
            # 职位详情页链接
            item['position_link'] = "https://hr.tencent.com/" + node.xpath("./td[1]/a/@href").extract_first()
            item['position_type'] = node.xpath("./td[2]/text()").extract_first()
            item['people_number'] = node.xpath("./td[3]/text()").extract_first()
            item['work_location'] = node.xpath("./td[4]/text()").extract_first()
            item['publish_times'] = node.xpath("./td[5]/text()").extract_first()

            yield item
            yield scrapy.Request(item['position_link'], callback=self.parse_page)

    def parse_page(self, response):
        # item = response.meta['content']
        item = PositionItem()
        item['position_link'] = response.url
        item['position_zhize'] = '; '.join(response.xpath("//ul[@class='squareli']")[0].xpath("./li/text()").extract())
        item["position_yaoqiu"] = "; ".join(response.xpath("//ul[@class='squareli']")[1].xpath("./li/text()").extract())

        yield item

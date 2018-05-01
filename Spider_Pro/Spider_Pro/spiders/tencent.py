# -*- coding: utf-8 -*-
import scrapy
from Spider_Pro.items import SpiderProItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['hr.tencent.com']
    page = 0
    base_url = "https://hr.tencent.com/position.php?start="
    # start_urls = [base_url + str(page)]
    # 事先构建好start_urls列表，引擎会全部构建请求入请求对列，下交给下载器，下载器会根据并发量进行处理
    # 需要一定的硬件环境性能
    start_urls = [base_url + str(page) for page in range(0, 3991, 10)]

    def parse(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")

        for node in node_list:
            item = SpiderProItem()
            item['position_name'] = node.xpath("./td[1]/a/text()").extract_first()
            item['position_link'] = "https://hr.tencent.com/" + node.xpath("./td[1]/a/@href").extract_first()
            item['position_type'] = node.xpath("./td[2]/text()").extract_first()
            item['people_number'] = node.xpath("./td[3]/text()").extract_first()
            item['work_location'] = node.xpath("./td[4]/text()").extract_first()
            item['publish_times'] = node.xpath("./td[5]/text()").extract_first()
            yield item

        """
                # 判断当前页面是否到最后一页，如果没到最后一页，就继续发送下一页的请求
                if not response.xpath("//a[@class='noactive' and @id='next']").extract_first():
                    next_link = "https://hr.tencent.com/" + response.xpath("//a[@id='next']/@href").extract_first()
                    yield scrapy.Request(next_link, callback = self.parse)
                """

        """
        # 设置页面抓取的限制，通过自增偏移量控制多页抓取
        if self.page < 3990:
            self.page += 10
            # 构建scrapy的Request()请求对象：参数1表示请求的url地址，参数2表示该请求发送后，返回的响应文件由指定的回调函数解析
            yield scrapy.Request(self.base_url + str(self.page), callback = self.parse)
        """



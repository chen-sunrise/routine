# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderProItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 职位名
    position_name = scrapy.Field()
    # 职位详情链接
    position_link = scrapy.Field()
    # 职位类型
    position_type = scrapy.Field()
    # 招聘人数
    people_number = scrapy.Field()
    # 工作地点
    work_location = scrapy.Field()
    # 发布时间
    publish_times = scrapy.Field()



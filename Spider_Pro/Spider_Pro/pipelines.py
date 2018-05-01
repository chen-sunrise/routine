# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class SpiderProPipeline(object):
    def open_spider(self, spider):
        self.f = open("tencent.csv", 'w')


    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.f.write(content)
        return item

    def close_spider(self, spider):
        self.f.close()
        # JsonToCsv()


'''def JsonToCsv():
    json_file = open('tencent.json', 'r')
    csv_file = open('tencent.csv', 'w')
    # 读取json文件的字符串，并返回python数据类型
    item_list = json.load(json_file)

    csv_write = csv.writer(csv_file)
    # sheet_head = csv_write[0]

    sheet_head = item_list[0].keys()
    sheet_data = [item.values() for item in item_list]
    csv_write.writerow(sheet_head)
    csv_write.writerows(sheet_data)

    # print csv_write
    csv_file.close()
    json_file.close()'''
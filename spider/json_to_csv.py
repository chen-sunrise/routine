# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import csv
import json

def JsonToCsv():
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
    json_file.close()

if __name__ == '__main__':
    JsonToCsv()
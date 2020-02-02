# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

from scrapy.exporters import JsonItemExporter


class JobsspiderPipeline(object):
    def __init__(self):
        self.file = codecs.open('job_infos.txt', 'w', encoding='UTF-8')

    def process_item(self, item, spider):
        """
        对爬取的数据进行存储管理
        :param item:
        :param spider:
        :return:
        """
        line = item.get("name", "null") + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        """
        当spider关闭的时候 关闭file
        :param spider:
        :return:
        """
        self.file.close()


# class JsonExportPipline(object):
#     # 调用scrapy自带的json_export导出json文件
#     def __init__(self):
#         self.file = open('job_info.json', 'wb')
#         self.exporter = JsonItemExporter(self.file, encoding='UTF-8', ensure_ascii=False)
#         self.exporter.start_exporting()
#
#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()
#
#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item

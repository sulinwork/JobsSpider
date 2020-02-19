# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import os, shutil, time
from JobsSpider.settings import job_file_dir


class JobsspiderPipeline(object):
    def __init__(self):
        job_file_name = time.strftime("%Y%m%d%H%M%S", time.localtime())+".txt"
        file_dir = job_file_name
        self.file = codecs.open(file_dir, 'w', encoding='UTF-8')
        self.file_dir = file_dir

    def process_item(self, item, spider):
        """
        对爬取的数据进行存储管理
        :param item:
        :param spider:
        :return:
        """
        # 字段有int类型会报错
        # line = "#".join(dict(item).values()) + "\n"
        line = "#".join('%s' % value for value in dict(item).values()) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        """
        当spider关闭的时候 关闭file
        :param spider:
        :return:
        """
        self.file.close()
        shutil.move(self.file_dir, job_file_dir)

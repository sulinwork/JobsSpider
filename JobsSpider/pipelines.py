# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import os, shutil, time
from JobsSpider.settings import job_file_dir
from JobsSpider.spiders.common import saveFileUpdateRecordFile


class JobsspiderPipeline(object):
    def __init__(self):
        job_file_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".txt"
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
        # line = "#".join(+dict(item).values()) + "\n"
        line = item['key'] + "#" + item['name'] + "#" + item['city'] \
               + "#" + item['year'] + "#" + item['edu'] + "#" + item['number'] \
               + "#" + item['time'] + "#" + item['salary'] + "#" + item['job_url'] + "#" + item['job_info'] \
               + "#" + item['company'] + "#" + item['company_field'] + "#" + item['company_size'] + "#" \
               + item['company_type'] + "\n"
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


class JobsManyFileOutput(object):
    def __init__(self):
        # 初始化一个字典
        file_dict = {}
        self.file_dict = file_dict
        self.base_path = None
        pass

    def process_item(self, item, spider):
        # 判断当前item的key是否存在字典中
        if self.file_dict.get(item['key']):
            # 存在则直接取出文件继续写入即可
            file = self.file_dict.get(item['key'])
        else:
            # 创建一个file 并放入字典
            base_path = 'file/'
            if not os.path.exists(base_path):
                os.makedirs(base_path)
            job_file_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".txt"
            file_dir = base_path + item['key'] + "_" + job_file_name
            file = codecs.open(file_dir, 'w', encoding='UTF-8')
            self.file_dict[item['key']] = file
            self.base_path = base_path

        line = item['key'] + "#" + item['name'] + "#" + item['city'] \
               + "#" + str(item['year']) + "#" + str(item['edu']) + "#" + str(item['number']) \
               + "#" + item['time'] + "#" + item['salary'] + "#" + item['job_url'] + "#" + item['job_info'] \
               + "#" + item['company'] + "#" + item['company_field'] + "#" + str(item['company_size']) + "#" \
               + item['company_type'] + "\n"
        file.write(line)

    def close_spider(self, spider):
        for file in self.file_dict.values():
            file.close()

        if not os.path.exists(job_file_dir):
            os.mkdir(job_file_dir)
        # 文件移动
        for file_name in os.listdir('file/'):
            shutil.move(os.path.join(self.base_path, file_name), job_file_dir)
        saveFileUpdateRecordFile()

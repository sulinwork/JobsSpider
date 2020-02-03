# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobInfoItem(scrapy.Item):
    # 岗位关键字
    key = scrapy.Field()
    # 岗位名称
    name = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 工作年限
    year = scrapy.Field()
    # 学历要求
    edu = scrapy.Field()
    # 招聘人数
    number = scrapy.Field()
    # 发布时间
    time = scrapy.Field()
    # 薪资
    salary = scrapy.Field()
    # 岗位信息url
    job_url = scrapy.Field()
    # 职位信息
    job_info = scrapy.Field()
    # 公司
    company = scrapy.Field()
    # 企业领域
    company_field = scrapy.Field()
    # 企业人数
    company_size = scrapy.Field()
    # 企业类型
    company_type = scrapy.Field()

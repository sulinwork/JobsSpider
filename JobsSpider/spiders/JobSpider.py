# -*- coding: utf-8 -*-
import scrapy


class JobspiderSpider(scrapy.Spider):
    name = 'JobSpider'
    allowed_domains = ['www.51job.com']
    start_urls = ['https://www.51job.com']

    def parse(self, response):
        pass

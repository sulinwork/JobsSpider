# -*- coding: utf-8 -*-
import scrapy
import re


class JobspiderSpider(scrapy.Spider):
    name = 'JobSpider'
    allowed_domains = ['www.51job.com']
    start_urls = ['https://www.51job.com']

    def parse(self, response):
        # 主页的时候抓取热门城市 确定爬取的城市岗位信息
        if response.url == 'https://www.51job.com':
            li_selector = response.xpath("//div[@class='hcity']/div[1]/a")
            for li in li_selector:
                city_name = li.xpath("text()")[0].extract()
                city_url = li.xpath("@href")[0].extract()
                city_code_regex = ".*com[/](.*)[/]"
                city_code_match = re.match(city_code_regex, city_url)
                if city_code_match:
                    city_code = city_code_match.group(1)
                    print("name:", city_name, ",code:", city_code)
                    # 可以往url采集器里面继续扔想要采集的路径
        else:
            print("开始爬取数据")

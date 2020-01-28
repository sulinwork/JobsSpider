# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request


class JobspiderSpider(scrapy.Spider):
    name = 'JobSpider'
    allowed_domains = ['www.51job.com', "search.51job.com", "jobs.51job.com"]
    start_urls = ['https://www.51job.com']

    list_start_url = "https://search.51job.com/list/00000,000000,0000,00,9,99,java,2,{0}.html"

    def parse(self, response):
        # xpath 语法选择
        # li_selector = response.xpath("//div[@class='hcity']/div[1]/a")
        # for li in li_selector:
        #     city_name = li.xpath("text()")[0].extract()
        #     city_url = li.xpath("@href")[0].extract()
        #     city_code_regex = ".*com[/](.*)[/]"
        #     city_code_match = re.match(city_code_regex, city_url)
        #     if city_code_match:
        #         city_code = city_code_match.group(1)
        #         print("name:", city_name, ",code:", city_code)
        #         # 可以往url采集器里面继续扔想要采集的路径

        # css选择器
        # a_list = response.css("div.hcity>div.li>a")
        # for a in a_list:
        #     city_url = a.css("::attr(href)").extract_first("")
        #     city_name = a.css("::text").extract_first("")
        #     city_code_match = re.match(".*com/(.*)/", city_url)
        #     if city_code_match:
        #         city_code = city_code_match.group(1)
        #         print("name:", city_name, ",code:", city_code)
        #         # 可以往url采集器里面继续扔想要采集的路径
        list_url = self.list_start_url.format(1)
        yield Request(url=list_url, callback=self.parse_job_list)

    def parse_job_list(self, response):
        """
        解析岗位列表的数据
        :param response:
        :return:
        """
        # 抓取数据list 确定详情页面
        detail_urls = response.css("div.el>p.t1>span>a::attr(href)").extract()
        for detail_url in detail_urls:
            yield Request(url=detail_url, callback=self.parse_detail)

        # 抓取页码
        # next_url = response.css("a#rtNext::attr(href)").extract()
        # if next_url:
        #     yield Request(url=next_url, callback=self.parse_job_list)
        # else:
        #     print("no have next page")

    def parse_detail(self, response):
        """
        解析岗位详细信息
        :param response:
        :return:
        """
        job_name = response.css("div.tHeader.tHjob > div > div.cn > h1::text").extract_first("")
        company_name = response.css("div.tHeader.tHjob > div > div.cn>p.cname>a::text").extract_first("")
        job_type = response.css("div.tHeader.tHjob > div > div.cn>p.msg::attr(title)").extract_first("")
        job_types = job_type.split("|")
        if len(job_types) == 5:
            print(job_type)
            # 工作城市
            city = job_types[0].strip()
            # 学历要求
            edu = job_types[2].strip()
            # 招聘人数 -1表示若干
            number_re = re.match(".*?([0-9]+).*", job_types[3].strip())
            if number_re:
                number = number_re.group(1)
            else:
                number = -1
            # 发布时间
            time_re = re.match("(^[0-9]{2}-[0-9]{2}).*", job_types[4].strip())
            if time_re:
                time = time_re.group(1)
            else:
                time = ""
                print(job_types[3].strip())
            print(city, edu, number, time)

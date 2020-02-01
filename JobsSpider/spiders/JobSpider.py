# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from JobsSpider.items import JobInfo


class JobspiderSpider(scrapy.Spider):
    name = 'JobSpider'
    allowed_domains = ['www.51job.com', "search.51job.com", "jobs.51job.com"]
    start_urls = ['https://search.51job.com/list/00000,000000,0000,00,9,99,java,2,1.html']

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
        """
        解析岗位列表的数据
        :param response:
        :return:
        """
        # 抓取数据list 确定详情页面
        detail_urls = response.css("div.el>p.t1>span>a::attr(href)").extract()
        for detail_url in detail_urls:
            # 可能会遇到相对路径 可以转化成绝对路径
            url = parse.urljoin(response.url, detail_url)
            # 将爬取的详情url 添加到采集器里  并制定回调函数名称  可以携带自定义参数：mata={}
            yield Request(url=url, callback=self.parse_detail, meta={})

        # 抓取页码
        # next_url = response.css("a#rtNext::attr(href)").extract()
        # if next_url:
        #     yield Request(url=next_url, callback=self.parse)
        # else:
        #     print("no have next page")

    def parse_detail(self, response):
        # 实例化对象 像字典一样传值
        job_info = JobInfo()
        # 获取传入的参数
        # param = response.meta.get("key", "默认值")
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

        job_info["name"] = job_name
        print(city, edu, number, time)
        # 将封装的item对象 传入pipelines 统一做存储管理
        yield job_info

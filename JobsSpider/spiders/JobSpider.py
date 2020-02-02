# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse
from JobsSpider.items import JobInfo
from JobsSpider.settings import job_keys, job_time_type
from JobsSpider.spiders.common import compareJobKeyAndName


class JobspiderSpider(scrapy.Spider):
    name = 'JobSpider'
    allowed_domains = ['www.51job.com', "search.51job.com", "jobs.51job.com"]
    start_urls = ['https://www.51job.com']

    url_template = "https://search.51job.com/list/00000,000000,0000,00,9,99,{0},2,1.html?ord_field=1"

    def parse(self, response):
        """
        拼接需要爬取的关键字url
        :param response:
        :return:
        """
        for job_key in job_keys:
            yield Request(url=self.url_template.format(job_key), meta={'job_key': job_key}, callback=self.parse_list)

    def parse_list(self, response):
        """
        解析岗位列表的数据
        :param response:
        :return:
        """
        # 抓取数据list 确定详情页面
        details = response.css("div.el")
        # 获取关键字
        job_key = response.meta['job_key']
        for detail in details:
            # 判断是获取昨天的还是全部
            if job_time_type == "update":
                time = details.css("span.t5::text").extract_first("")
                time = datetime.datetime.strptime(time, "%m-%d")
                curr_time = datetime.datetime.now().strftime("%m-%d")
                curr_time = datetime.datetime.strptime(curr_time, "%m-%d")
                if (curr_time - time).days != 1:
                    continue
            # 获取名称 过滤掉不符合的岗位
            name = detail.css("p.t1>span>a::text").extract_first("")
            if compareJobKeyAndName(job_key.upper(), name.upper())[1] == 0:
                continue
            # 获取url
            detail_url = detail.css("p.t1>span>a::attr(href)").extract_first("")
            # 可能会遇到相对路径 可以转化成绝对路径
            # url = parse.urljoin(response.url, detail_url)
            # 将爬取的详情url 添加到采集器里  并制定回调函数名称  可以携带自定义参数：mata={}
            yield Request(url=detail_url, meta={'job_key': job_key}, callback=self.parse_detail)

        # 抓取页码
        # next_url = response.css("a#rtNext::attr(href)").extract()
        # if next_url:
        #     yield Request(url=next_url, callback=self.parse)
        # else:
        #     print("no have next page")

    def parse_detail(self, response):
        """
        解析岗位的具体信息
        :param response:
        :return:
        """
        # 实例化对象 像字典一样传值
        job_info = JobInfo()
        # 获取关键字
        job_key = response.meta['job_key']
        job_info["key"] = job_key
        # 获取名称
        name = response.css("div.tHeader.tHjob > div > div.cn > h1::text").extract_first("")
        job_info["name"] = name
        company = response.css("div.tHeader.tHjob > div > div.cn>p.cname>a::text").extract_first("")
        job_info["company"] = company
        job_type = response.css("div.tHeader.tHjob > div > div.cn>p.msg::attr(title)").extract_first("")
        # 提取工作城市
        city_re = re.match("^([\u4e00-\u9fa5]*).*[-,|].*", job_type)
        if city_re:
            city = city_re.group(1)
        else:
            city = ""
        job_info["city"] = city
        # 提取工作年限要求
        year_re = re.match(".*?([0-9,-]+年)经验.*|.*(在校生/应届生).*", job_type)
        if year_re:
            for group in year_re.groups():
                if group:
                    year = group
                    break
        else:
            year = "无"
        job_info["year"] = year
        # 学历要求
        edu_re = re.match(".*(大专|本科|硕士|博士).*", job_type)
        if edu_re:
            edu = edu_re.group(1)
        else:
            edu = "无"
        job_info["edu"] = edu

        # 招聘人数
        number_re = re.match(".*招([0-9]+)人.*", job_type)
        if number_re:
            number = number_re.group(1)
        else:
            number = -1
        job_info["number"] = number

        # 发布时间
        time_re = re.match(".*?([0-9]+-[0-9]+)发布.*", job_type)
        if time_re:
            time = time_re.group(1)
        else:
            time = ""
        job_info["time"] = time

        # 爬取薪资
        salary = response.css("div.tHeader.tHjob > div > div.cn > strong::text").extract_first("")
        print(salary)
        # yield job_info

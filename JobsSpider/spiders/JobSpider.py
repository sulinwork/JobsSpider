# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
import codecs
import json
import os
from scrapy.http import Request
from JobsSpider.items import JobInfoItem
from JobsSpider.settings import job_keys
from JobsSpider.spiders.common import compareJobKeyAndName


class JobspiderSpider(scrapy.Spider):
    name = 'JobSpider'
    allowed_domains = ['www.51job.com', "search.51job.com", "jobs.51job.com"]
    start_urls = ['https://www.51job.com']

    url_template = "https://search.51job.com/list/00000,000000,0000,00,9,99,{0},2,1.html?ord_field=1"

    def __init__(self):
        path = os.path.dirname(os.path.dirname(__file__)) + "/record.txt"
        if not os.path.exists(path):
            with codecs.open(path, 'w', encoding="UTF-8") as f:
                f.close()
        try:
            self.record = json.load(codecs.open(path, "r", encoding="UTF-8"))
        except BaseException:
            self.record = {}

    def parse(self, response):
        """
        拼接需要爬取的关键字url
        :param response:
        :return:
        """
        for job_key in job_keys.keys():
            yield Request(url=self.url_template.format(job_key), meta={'job_key': job_key}, callback=self.parse_list)

    def parse_list(self, response):
        """
        解析岗位列表的数据
        :param response:
        :return:
        """
        # 抓取数据list 确定详情页面
        details = response.css("div#resultList>div.el")
        # 获取关键字
        job_key = response.meta['job_key']
        for detail in details[1:]:
            # 判断是获取昨天的还是全部
            if job_keys.get(job_key) == "update":
                time_str = detail.css("span.t5::text").extract_first("")
                curr_time = datetime.datetime.strptime(time_str, "%m-%d")
                record_time = datetime.datetime.strptime(self.record[job_key], "%m-%d")
                now_time = datetime.datetime.strptime(datetime.datetime.now().strftime("%m-%d"), "%m-%d")
                if (curr_time - record_time).days <= 0:
                    return
                elif (curr_time - now_time).days == 0:
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
        next_url = response.css("a#rtNext::attr(href)").extract_first("")
        if next_url:
            yield Request(url=next_url, meta={'job_key': job_key}, callback=self.parse_list)
        else:
            print("no have next page")

    def parse_detail(self, response):
        """
        解析岗位的具体信息
        :param response:
        :return:
        """
        # 实例化对象 像字典一样传值
        job_info_item = JobInfoItem()
        # 获取关键字
        job_key = response.meta['job_key']
        job_info_item["key"] = job_key
        # 获取名称
        name = response.css("div.tHeader.tHjob > div > div.cn > h1::text").extract_first("")
        job_info_item["name"] = name
        company = response.css("div.tHeader.tHjob > div > div.cn>p.cname>a::text").extract_first("")
        job_info_item["company"] = company
        job_type = response.css("div.tHeader.tHjob > div > div.cn>p.msg::attr(title)").extract_first("")
        # 提取工作城市
        city_re = re.match("^([\u4e00-\u9fa5]*).*[-,|].*", job_type)
        if city_re:
            city = city_re.group(1)
        else:
            city = ""
        job_info_item["city"] = city
        # 提取工作年限要求
        year_re = re.match(".*?([0-9,-]+年)经验.*|.*(在校生/应届生).*", job_type)
        if year_re:
            for group in year_re.groups():
                if group:
                    year = group
                    break
        else:
            year = "无"
        job_info_item["year"] = year
        # 学历要求
        edu_re = re.match(".*(大专|本科|硕士|博士).*", job_type)
        if edu_re:
            edu = edu_re.group(1)
        else:
            edu = "无"
        job_info_item["edu"] = edu

        # 招聘人数
        number_re = re.match(".*招([0-9]+)人.*", job_type)
        if number_re:
            number = number_re.group(1)
        else:
            number = -1
        job_info_item["number"] = number

        # 发布时间
        time_re = re.match(".*?([0-9]+-[0-9]+)发布.*", job_type)
        if time_re:
            time = time_re.group(1)
        else:
            time = ""
        job_info_item["time"] = time

        # 爬取薪资 需要做统一处理
        salary = response.css("div.tHeader.tHjob > div > div.cn > strong::text").extract_first("")
        job_info_item['salary'] = salary
        # 岗位信息url
        job_info_item["job_url"] = response.url

        # 职位信息

        p_list = response.css("div.bmsg.job_msg.inbox>p::text").extract()
        # if len(p_list) == 0:
        #     p_list = response.css("div.bmsg.job_msg.inbox>div")
        #     job_info = ""
        #     for p in p_list:
        #         div_class_name = p.css("::attr(class)").extract()
        #         if len(div_class_name) == 0:
        #             job_info = job_info + "|" + p.css("::text").extract_first("")
        #     if len(job_info) > 0:
        #         job_info = job_info[1:]
        #     print(job_info)
        # else:
        job_info = "|".join(p_list)
        job_info_item['job_info'] = job_info
        # 企业领域
        company_fields = response.css("div.com_tag > p:nth-child(3)>a::text").extract()
        company_field = "|".join(company_fields)
        job_info_item['company_field'] = company_field
        # 企业人数
        company_size = response.css("div.com_tag > p:nth-child(2)::text").extract_first("")
        job_info_item['company_size'] = company_size
        # 企业类型
        company_type = response.css("div.com_tag > p:nth-child(1)::text").extract_first("")
        job_info_item['company_type'] = company_type
        yield job_info_item

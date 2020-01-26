# 可调式
from scrapy.cmdline import execute

import sys
import os

# 得到当前文件的父目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy", "crawl", "JobSpider"])

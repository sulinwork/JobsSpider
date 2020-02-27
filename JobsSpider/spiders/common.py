from JobsSpider.settings import job_keys
import datetime
import codecs
import json


def compareJobKeyAndName(key, name):
    """
    比较岗位和关键字 做过滤
    :param key:
    :param name:
    :return:
    """
    lstr1 = len(key)
    lstr2 = len(name)
    record = [[0 for i in range(lstr2 + 1)] for j in range(lstr1 + 1)]
    # 开辟列表空间 为什么要多一位呢?主要是不多一位的话,会存在边界问题
    # 多了一位以后就不存在超界问题
    maxNum = 0  # 最长匹配长度
    p = 0  # 匹配的起始位
    for i in range(lstr1):
        for j in range(lstr2):
            if key[i] == name[j]:
                # 相同则累加
                record[i + 1][j + 1] = record[i][j] + 1
                if record[i + 1][j + 1] > maxNum:
                    # 获取最大匹配长度
                    maxNum = record[i + 1][j + 1]
                    # 记录最大匹配长度的终止位置
                    p = i + 1
    return key[p - maxNum:p], maxNum


def saveFileUpdateRecordFile():
    record_dict = job_keys.copy()
    for k in job_keys.keys():
        if job_keys[k] == "new":
            record_dict[k] = datetime.datetime.now().strftime("%m-%d")
        if job_keys[k] == "update":
            curr_time = getYesterday().strftime("%m-%d")
            record_dict[k] = curr_time

    with codecs.open("../record.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(record_dict, ensure_ascii=False))

def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday


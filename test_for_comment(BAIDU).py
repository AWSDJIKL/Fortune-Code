import pandas as pd
import datetime
from aip import AipNlp
import codecs
import os
import numpy as np
import time
import math
import threading
import random

APP_ID = "23865993"
API_KEY = 'cDdctPToAxqpdbEXkfRERR1j'
SECRET_KEY = 'jAh9ss2fpwpPEjErMGVpwW03nVMtlC2G'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


def get_sentiments(text, dates):
    global result
    while True:
        try:
            # print(text)
            result = client.sentimentClassify(text)
            # print("result", result)
            sitems = result['items'][0]  # 情感分析
            # print(sitems)
            positive = sitems['positive_prob']  # 积极概率
            confidence = sitems['confidence']  # 置信度
            sentiment = sitems['sentiment']  # 0表示消极，1表示中性，2表示积极
            # tagitems = client.commentTag(text, {'type': 9})  # 评论观点
            # propertys=tagitems['prop']#属性
            # adj=tagitems['adj']#描述词
            output = '{}\t{}\t{}\t{}\n'.format(dates, positive, confidence, sentiment)
            with open("comment/summarize/sf_0.csv", "a", encoding="utf-8") as f:
                f.write(output)
            return output
        except Exception as e:
            print("error")
            print("result", result)


# def get_content():
#     data = pd.DataFrame(pd.read_excel('eastmoney.xlsx', sheet_name=0))
#     data.columns = ['Dates', 'viewpoints']  # 重设表头
#     data = data.sort_values(by=['Dates'])  # 按日期排列
#     vdata = data[data.Dates >= startdate]  # 提取对应日期的数据
#     newvdata = vdata.groupby('Dates').agg(lambda x: list(x))  # 按日期分组，把同一天的评论并到一起
#     return newvdata

def get_comment(file_path, file_name):
    # data = pd.DataFrame(pd.read_csv(path + 'SF_allcomment.csv'))
    # data.columns = ['用户名', '评论时间', '评论内容', '点赞数']
    # data = data.sort_values(by=['评论时间'])
    # vdata = data[data['评论时间'] >= startdate]
    # newdata = vdata.groupby('评论时间').agg(lambda x: list(x))
    # return newdata

    # 获取当前时间
    start_time = datetime.datetime.now()
    print(start_time)
    # 获取评论文件的目录
    # 创建一个dataframe存放数据
    data = pd.DataFrame()
    # 读取对应评论文件
    data = pd.read_csv(os.path.join(file_path, file_name), header=0)
    # data.columns = ['用户名', '评论时间', '评论内容', '点赞数']
    type_dict = {'用户名': str, '评论时间': np.datetime64, '评论内容': str, '点赞数': int}
    data = data.astype(type_dict)
    print("评论文件读取成功")
    print("评论总数为：", len(data))
    # print(data)
    return data


if __name__ == '__main__':
    startdate = datetime.date(2011, 3, 5).strftime('%Y/%m/%d')
    enddate = datetime.date(2021, 3, 21).strftime('%Y/%m/%d')
    path = 'comment/summarize'  # 该股票评论的文件夹路径
    comment_file_name = '顺丰控股吧_0.csv'  # 该股票评论的文件名
    viewdata = get_comment(path, comment_file_name)
    viewdata = viewdata.drop(index=(viewdata.loc[(viewdata["评论内容"].isna())].index))
    comment_count = viewdata.shape[0]
    print("评论总数：", comment_count)
    for i in range(viewdata.shape[0]):
        print('正在处理第{}条,还剩{}条'.format(i, viewdata.shape[0] - i))
        dates = viewdata['评论时间'][i]
        get_sentiments(viewdata['评论内容'][i], dates)
        time.sleep(1)
    print("done")

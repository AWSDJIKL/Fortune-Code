# -*- coding: utf-8 -*-
'''
将各个股吧的评论汇总到对应的csv文件中
'''
# @Time : 2021/3/25 11:36 
# @Author : LINYANZHEN
# @File : SummarizeComment.py

import numpy as np
import pandas as pd
import os
import csv
from snownlp import SnowNLP
import datetime


def get_post_file_path(path):
    # 获取评论文件的目录
    # path = 'stock_comment//格林美吧' #该股票评论的文件夹路径
    file_list = []  # 存放该股票评论的各文件的名称
    # os.chdir(r'D://PycharmProjects//codeofrich')
    for root, dirs, files in os.walk(path):
        for file in files:
            # print(os.path.join(root,file))
            file_list.append(os.path.join(root, file))
            # for file in os.walk(path):
    # if file.endswith('.txt'):
    #     file_list.append(path+file)
    print("该目录下存在评论文件个数：", len(file_list))
    return file_list


def read_post_file(file_list):
    # 创建一个dataframe存放数据
    data = pd.DataFrame()
    # 遍历各文件的路径开始读取并获取data
    print("正在读取文件")
    for file in file_list:
        new_data = pd.read_table(file, header=None)
        data = data.append(new_data)
        # print(data)
    print("读取文件完成")

    # 赋予dataframe列名并输出检查
    data.columns = ['用户名', '评论时间', '评论内容', '点赞数']
    # print(data['评论内容'])
    print(len(data))
    return data


def data_to_csv(data, path):
    # 创建一个新txt文件存放获取的所有评论以及分数
    with open(path, 'w', encoding='utf-8', newline="")as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['用户名', '评论时间', '评论内容', '点赞数'])
        for i in data.values:
            # print(i)
            csv_writer.writerow(i)
    print("新数据csv完成")


def csv_to_data(path):
    data = pd.read_csv(path, header=0)
    data_types_dict = {'用户名': str, '评论时间': np.datetime64, '评论内容': str, '点赞数': int}
    data = data.astype(data_types_dict)
    print(data.dtypes)
    # print(data["评论时间"])
    data = data.sort_values(by="评论时间")
    data=data.drop(index=(data.loc[(data["评论内容"].isna())].index))
    # print(data["评论时间"])
    data_to_csv(data, path)
    # time=pd.to_datetime(time, format="%Y-%m-%d %H:%M:%S")


def main():
    input_path = "stock_comment"
    output_path = "comment/summarize"
    for dir in os.listdir(input_path):
        # 遍历每个吧的目录
        file_list = get_post_file_path(os.path.join(input_path, dir))
        # print(len(file_list))
        data = read_post_file(file_list)
        data_to_csv(data, os.path.join(output_path, dir + ".csv"))


def sort_csv():
    path = "comment/summarize"
    for file in os.listdir(path):
        csv_to_data(os.path.join(path, file))


if __name__ == '__main__':
    # main()
    sort_csv()

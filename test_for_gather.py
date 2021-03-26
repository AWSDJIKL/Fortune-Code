# editor:pakchungy
# date:2021-03-19
import numpy as np
import pandas as pd
import os
from snownlp import SnowNLP
import datetime
import csv

# 获取当前时间
now = datetime.datetime.now()
print(now)


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


def data_to_csv(data, file_name):
    # 创建一个新txt文件存放获取的所有评论以及分数
    new_path = "comment//summarize//"
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    with open(new_path + file_name + '.csv', 'w', encoding='utf-8', newline="")as f:
        for i in data.values:
            # print(i)
            csv_writer = csv.writer(f)
            # csv_writer.writerow = (['用户名', '评论时间', '评论内容', '点赞数', '分数'])
            csv_writer.writerow(i)
    print("新数据csv完成")


if __name__ == '__main__':
    path = "stock_comment"
    for root, dirs, files in os.walk(path):
        # 遍历每个吧的目录
        for dir in dirs:
            file_list = get_post_file_path(os.path.join(root, dir))

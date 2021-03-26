# -*- coding: utf-8 -*-
'''
保存暂时弃用的代码
'''
# @Time : 2021/3/22 9:23 
# @Author : LINYANZHEN
# @File : test.py
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import math
from snownlp import SnowNLP
import os
import math
import pandas
import numpy as np
import csv
import datetime
import matplotlib.pyplot as plt

# 不是所有“点击查看全部”都能点，只有那些有剩余评论且剩余评论不为0的才能点
# browser, check_all_elements = find_elements_by_xpath(browser,
#                                                      "//span[@class=\"more_num\"][text()][text()!=\"0\"]/../a",
#                                                      post_url)
# # 把所有“点击查看全部”全都点一次
# for i in range(len(check_all_elements)):
#     print(i)
#     # 点过一次“点击查看全部”后，页面元素会更新，需要重新获取
#     browser, e = find_element_by_xpath(browser, "//span[@class=\"more_num\"][text()][text()!=\"0\"]/../a",
#                                        post_url)
#     e.click()
#     # 要等2秒让页面加载，
#     time.sleep(2)
# # 隔一段时间再去获取评论，需要给时间让浏览器加载元素
# time.sleep(5)
# # 获取一级评论
# browser, comment_elements = find_elements_by_xpath(browser,
#                                                    "//div[@id=\"comment_all_content\"]/div[@id=\"zwlist\"]/div",
#                                                    post_url)
# for i in range(len(comment_elements)):
#     print("第{}条评论————————————————————".format(i + 1))
#     now_level1_item = "//div[@id=\"comment_all_content\"]/div[@id=\"zwlist\"]/div[{}]/div[1]".format(i + 1)
#     # 作者
#     browser, author_element = find_element_by_xpath(browser, now_level1_item + "/div[1]/a", post_url)
#     # 发表时间
#     browser, publish_time_element = find_element_by_xpath(browser, now_level1_item + "/div[2]", post_url)
#     # 评论内容
#     browser, comment_content_element = find_element_by_xpath(browser, now_level1_item + "/div[3]/div[1]", post_url)
#     # 用js脚本修改标签的属性，让全文显示出来
#     js = "var divset=document.getElementsByTagName(\"" + str(
#         comment_content_element.tag_name) + "\");for (var i = 0; i<divset.length;i++) {divset[i].style.display='block';};"
#     browser.execute_script(js)
#     # 等待3秒让内容加载出来
#     time.sleep(3)
#     # 重新获取评论正文
#     browser, comment_content_element = find_element_by_xpath(browser, now_level1_item + "/div[3]/div[1]", post_url)
#     # 获取该评论的点赞数
#     browser, like_element = find_element_by_xpath(browser, now_level1_item + "/div[4]/div[1]/span[5]/span",
#                                                   post_url)
#     author = author_element.text
#     publish_time = publish_time_element.text
#     comment_content = comment_content_element.text
#     like = int(like_element.text) if like_element.text != "点赞" else 0  # 如果是里面的内容是点赞，说明没人赞
#     print(author)
#     print(publish_time)
#     print(comment_content)
#     print(like)
#     level2_comment = []
#
#     # 获取二级评论
#     # 可能有多页二级评论
#     level2_list = now_level1_item + "/div[5]/div[2]"
#     # 先看看有没有二级评论
#     browser, level2_list_element = find_element_by_xpath(browser, level2_list, post_url)
#     try:
#         level2_list_element = browser.find_element_by_xpath(
#             now_level1_item + "/div[5]/div[2][@style=\"display:none;\"]")
#
#     except Exception as e:
#         print(e)
#     print(level2_list_element.is_displayed())
#     style = level2_list_element.get_property("style")
#     # 若有，看看有多少页
#
#     # 每页都获取
#     # browser, unfold_elements = find_elements_by_xpath(browser, "", post_url)
#
#     # browser, comment_elements = find_elements_by_xpath(browser,now_level1_item + "/div[5]/div[2]/div[class=\"level2_item\"]",post_url)
#     # for i in range(len(comment_elements)):
#     #     pass
# browser.quit()


# def quantilizeSentiments(data,date):
#     pos=neg=0
#     print(len(data[date]))
#     for comment in data[date]:
#         try:#受到snownlp中算法限制，这里可能会因为出现了snownlp中没有的词而报错，所以添加了try-except语句
#             nlp = SnowNLP(comment['comment'])
#             sentimentScore = nlp.sentiments
#         except:
#             print(traceback.format_exc())
#             continue
#         if(sentimentScore>0.6):
#             fans=SQL.selectFansByUserId(comment['user_id'])
#             pos+=1+math.log(comment['like_count']+fans[0][0]+1,2)
#         if(sentimentScore<0.4):
#             fans=SQL.selectFansByUserId(comment['user_id'])
#             neg+=1+math.log(comment['like_count']+fans[0][0]+1,2)
#     print("负："+str(neg)+"  正："+str(pos))
#     return (pos/(pos+neg+0.0001)-0.5)*math.log(len(data[date])+1,2)

# df = pandas.DataFrame([[1, 2, 3], [4, 5, 6]])
# df.columns = ["a", "b", "c"]
# b = df["b"]
# for i in range(len(b)):
#     b[i] = 0
# print(df)

# path = "comment/analyzed/stock_GLMcomments_analyzed.csv"
path = "comment/analyzed/stock_SFcomments_analyzed.csv"
# new_path = "comment/analyzed/stock_GLMcomments_analyzed_sort.csv"
new_path = "comment/analyzed/stock_SFcomments_analyzed_sort.csv"
data = pandas.read_csv(path)
# data.columns = ['用户名', '评论时间', '评论内容', '点赞数', "snow评分"]
time = data["评论时间"]
for i in range(len(time)):
    time[i] = time[i][:10]
# print(time)
time = set(data["评论时间"].tolist())
# print(time)
df = pandas.DataFrame(columns=["date", "sum"])
count = 0
for t in time:
    d = data[data["评论时间"] == t]
    sum = 0
    pos = 0
    neg = 0
    for i in d.values:
        if i[4] == 1:
            # pos += 1 + math.log(i[3] + 1, 2)
            pos += i[3] + 1
        else:
            # neg += 1 + math.log(i[3] + 1, 2)
            neg += i[3] + 1
    # sum = (pos / (pos + neg + 0.0001) - 0.5) * math.log(len(d.values) + 1, 2)
    sum = np.log(1.0 * (1 + pos) / (1 + neg))
    #     sum += (i[3] + 1) * i[4]
    # sum /= len(d.values)
    df.loc[count] = {"date": t, "sum": sum}
    count += 1
print(df)
df = df.sort_values(by="date")
print(df)
# 创建一个新txt文件存放获取的所有评论以及分数
with open(new_path, 'w', encoding='utf-8', newline="")as f:
    csv_writer = csv.writer(f)
    # csv_writer.writerow(['用户名', '评论时间', '评论内容', '点赞数'])
    for i in df.values:
        # print(i)
        csv_writer.writerow(i)

data = pandas.read_csv(new_path, header=None)
data.columns = ["date", "sum"]
datestart = "2019-11-30"
dateend = "2021-03-12"

datestart = datetime.datetime.strptime(datestart, '%Y-%m-%d')
dateend = datetime.datetime.strptime(dateend, '%Y-%m-%d')
date_list = []
date_list.append(datestart.strftime('%Y-%m-%d'))
while datestart < dateend:
    # 日期叠加一天
    datestart += datetime.timedelta(days=+1)
    # 日期转字符串存入列表
    date_list.append(datestart.strftime('%Y-%m-%d'))
score_list = []
for d in date_list:
    if d in data["date"].tolist():
        score_list.append(data[data["date"] == d]["sum"])
    else:
        score_list.append(score_list[-1])
plt.plot(date_list, score_list, "b")
plt.show()

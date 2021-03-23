# -*- coding: utf-8 -*-
'''
爬取股吧所有热门个人股的所有帖子和评论
'''
# @Time : 2021/3/19 15:46
# @Author : LINYANZHEN
# @File : GetComment.py

import re
import requests
import math
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType


# def get_url_txt(url):
#     '''
#     使用request获取指定网址里的内容
#
#     :param url: 网址
#     :return: 网页内容
#     '''
#
#     # 在请求中加入headers，伪装成浏览器访问
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
#         'Host': 'sso.1234567.com.cn',
#         "Cookie": "OCSSID=4df0bjva6j7ejussu8al3eqo03"
#     }
#     res = requests.get(url, headers)
#     res.encoding = "utf-8"
#     return res.text
#
#
# def get_stock_all_post_url(home_url):
#     # 所有帖子的网址
#     all_post_url = []
#     url_text = get_url_txt(home_url)
#     r = re.compile("<a href=\"/.*title")
#     # 遍历所有页面，获取所有帖子
#     # “股票代码_|所有帖子总数|一页显示的帖子数量|当前是第几页”
#     pagernums = re.compile("(?<=data-pager=\"list,).*(?=\">)").findall(url_text)[0].split("|")
#     pages = math.ceil(int(pagernums[1]) / int(pagernums[2]))
#     for page in range(pages):
#         # 拼接出每一页的url
#         page_url = home_url[:-5] + "_" + str(page + 1) + ".html"
#         page_text = get_url_txt(page_url)
#         # 获取一页的帖子
#         for s in r.findall(page_text):
#             if "><em class=" not in s:  # 把不属于帖子的内容去掉
#                 if "/news" in s:
#                     all_post_url.append("http://caifuhao.eastmoney.com" + s[9:-7])
#                 else:
#                     all_post_url.append("http:" + s[9:-7])
#     return all_post_url
##################################################################
# 使用request只能获取静态网页内容，对于js动态加载的部分很难获取，因此抛弃
# 转用selenium驱动浏览器获取完整内容
def get_url_html(browser, url):
    '''
    获取指定页面的html源码

    :param browser: 浏览器对象
    :param url: 页面网址
    :return: 源码
    '''
    while True:
        try:
            browser.get(url)
            print(url + "————访问成功")
            return browser
        except:
            # 代理失效了，更换代理
            print("代理失效了，更换代理")
            browser = change_browser_proxy(browser)
        # 重新尝试
        print("重新尝试")


def get_proxy_ip(num):
    '''
    从隧道代理池中获取IP

    :return: ip:port的列表
    '''
    tunnel_ip_url = "http://http.tiqu.letecs.com/getip3?num={}&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=4&sb=0&pb=45&mr=1&regions=".format(
        num)
    r = requests.get(tunnel_ip_url)
    ip_port_list = r.text.split("\n")
    return ip_port_list


def change_browser_proxy(browser):
    '''
    为浏览器更换新的代理IP

    :param browser: 原来的浏览器
    :return: 新的浏览器
    '''
    # 先把原来的浏览器关了
    browser.quit()
    # 从隧道代理ip池中获取一个新的代理
    new_proxy = get_proxy_ip(1)[0]
    print("新的代理：{}".format(new_proxy))
    try:
        browser = get_new_browser(new_proxy)
        # 测试代理是否可用
        test_url = "http://httpbin.org/ip"
        browser.get(test_url)
        # print(browser.find_element_by_xpath("//pre").text)
        print("代理可用")
    except:
        print("代理失效")
    return browser


def get_new_browser(proxy=None):
    '''
    生成一个新的浏览器对象

    :param proxy: 代理设置，默认不使用
    :return: 新的浏览器对象
    '''
    # 设定浏览器参数，使用无界面浏览器
    chrom_options = Options()
    chrom_options.add_argument("--headless")
    chrom_options.add_argument("--disable-gpu")
    if proxy:
        chrom_options.add_argument("--proxy-server=http://" + proxy)
    # 指定浏览器驱动路径
    exe_path = "chromedriver.exe"
    # 创建一个浏览器对象
    browser = webdriver.Chrome(executable_path=exe_path, chrome_options=chrom_options)
    return browser


def find_elements_by_xpath(browser, xpath, url):
    '''
    根据xpath寻找元素

    :param browser: 浏览器
    :param xpath: xpath
    :param url: 元素所在的页面网址，找不到的时候更换代理刷新再找一次
    :return: 符合条件的元素列表
    '''
    n = 10
    while n > 0:
        try:
            elements = browser.find_elements_by_xpath(xpath)
            return browser, elements
        except:
            # 出现了位置错误
            print(browser.page_source)
            # 更换代理，再试一次
            browser = change_browser_proxy(browser)
            browser = get_url_html(browser, url)
            n -= 1
    return browser, None


def find_element_by_xpath(browser, xpath, url):
    '''
    根据xpath寻找元素

    :param browser: 浏览器
    :param xpath: xpath
    :param url: 元素所在的页面网址，找不到的时候更换代理刷新再找一次
    :return: 符合条件的元素
    '''
    n = 10
    while n > 0:
        try:
            element = browser.find_element_by_xpath(xpath)
            return browser, element
        except Exception as e:
            # 出现了未知错误
            print(e)
            # print(browser.page_source)
            # 更换代理，再试一次
            browser = change_browser_proxy(browser)
            browser = get_url_html(browser, url)
            n -= 1
    return browser, None


def get_stock_all_post_url(home_url, stock_name, star_date=None, end_date=None):
    '''
    获取一支股票的所有帖子的网址

    :param home_url: 该股票的股吧首页
    :param stock_name: 股票的股吧名字（用于检查是否被封IP）
    :param star_date: 起始时间（默认没有，则获取到最旧的帖子）
    :param end_date: 终止时间（默认没有，则获取到最新的帖子）
    :return: 所有帖子的url
    '''
    browser = get_new_browser()
    # 从第一页开始爬取，记录当前爬取的帖子的年份
    now_year = datetime.now().year

    browser = get_url_html(browser, home_url)
    # 检测一下有没有被封IP
    # now_stock_name = browser.find_element_by_xpath("//span[@id=\"stockname\"]/a")
    browser, now_stock_name = find_element_by_xpath(browser, "//span[@id=\"stockname\"]/a", home_url)
    # 一直换代理
    while now_stock_name.text != stock_name:
        print("ip被封，跳转到：" + now_stock_name.text)
        # 更换代理
        browser = change_browser_proxy(browser)
        # 重新获取页面
        browser = get_url_html(browser, home_url)
        # 重新检测一下有没有被封IP
        # now_stock_name = browser.find_element_by_xpath("//span[@id=\"stockname\"]/a")
        browser, now_stock_name = find_element_by_xpath(browser, "//span[@id=\"stockname\"]/a", home_url)
    # 获取总页数
    browser, pages = find_element_by_xpath(browser, "//span[@class=\"sumpage\"]", home_url)
    pages = int(pages.text)
    print("总页数：{}".format(pages))
    abandon_post_num = 0
    all_post_url = []
    # 遍历所有页面获取该支股票所有的帖子的url
    for page in range(pages):
        # 跳转到指定页面
        print("正在获取第{}页的帖子网址".format(page + 1))
        # 按发帖时间排序
        now_page_url = home_url[:-5] + ",f_" + str(page + 1) + ".html"
        browser = get_url_html(browser, now_page_url)
        # 检测一下有没有被封IP
        # now_stock_name = browser.find_element_by_xpath("//span[@id=\"stockname\"]/a")
        browser, now_stock_name = find_element_by_xpath(browser, "//span[@id=\"stockname\"]/a", now_page_url)
        # 一直换代理
        while now_stock_name.text != stock_name:
            print("ip被封，跳转到：" + now_stock_name.text)
            # 更换代理
            browser = change_browser_proxy(browser)
            # 重新获取页面
            browser = get_url_html(browser, now_page_url)
            # 重新检测
            # now_stock_name = browser.find_element_by_xpath("//span[@id=\"stockname\"]/a")
            browser, now_stock_name = find_element_by_xpath(browser, "//span[@id=\"stockname\"]/a", now_page_url)
        # 帖子的url
        # url_element_list = browser.find_elements_by_xpath("//a[@href][@title][not(@target)]")
        browser, url_element_list = find_elements_by_xpath(browser, "//a[@href][@title][not(@target)]", now_page_url)
        # 帖子作者
        # author_element_list = browser.find_elements_by_xpath(
        #     "//a[@href][@title][not(@target)]/../following-sibling::span[1]")
        browser, author_element_list = find_elements_by_xpath(browser,
                                                              "//a[@href][@title][not(@target)]/../following-sibling::span[1]",
                                                              now_page_url)
        # 帖子的最后更新时间
        # date_list = browser.find_elements_by_xpath("//a[@href][@title][not(@target)]/../following-sibling::span[2]")
        browser, date_list = find_elements_by_xpath(browser,
                                                    "//a[@href][@title][not(@target)]/../following-sibling::span[2]",
                                                    now_page_url)
        print("     该页共{}个帖子".format(len(url_element_list)))
        # 记录上一个帖子的月份，用于年份更新
        last_post_month = int(date_list[0].text[:2])
        print("附近帖子最后更新时间：{}".format(datetime(now_year, int(date_list[0].text[:2]), int(date_list[0].text[3:5]))))
        for url_element, author_element, date in zip(url_element_list, author_element_list, date_list):
            # 获取帖子最后更新时间
            try:
                post_date = datetime(now_year, int(date.text[:2]), int(date.text[3:5]))
            except:
                # 帖子被隐藏，放弃
                abandon_post_num += 1
                continue
            post_date = datetime(now_year, int(date.text[:2]), int(date.text[3:5]))
            # 附近帖子的月份发生变化,查看帖子的年份进行更新
            # 有可能是反爬虫机制：在中间插入一些别的月份的帖子进行干扰
            if last_post_month != post_date.month:
                try:
                    post_date = get_post_time(url_element.get_property("href"))
                except:
                    # 大概率帖子被删了，放弃这个帖子
                    abandon_post_num += 1
                    continue
                now_year = post_date.year
            last_post_month = post_date.month
            # 晚于要求的终止时间，跳过
            if end_date and post_date > end_date:
                continue
            # 早于要求的起始时间，收集完成，退出
            elif star_date and post_date < star_date:
                all_post_num = len(all_post_url)
                all_post_url.append("一共获取了{}个帖子，途中抛弃了{}个帖子".format(all_post_num, abandon_post_num))
                return all_post_url
            else:
                # 获取帖子的url
                post_url = url_element.get_property("href")
                post_title = url_element.text
                post_author = author_element.text
                all_post_url.append("{}\t{}\t{}\t{}".format(post_date, post_url, post_title, post_author))
    browser.quit()
    all_post_num = len(all_post_url)
    all_post_url.append("一共获取了{}个帖子，途中抛弃了{}个帖子".format(all_post_num, abandon_post_num))
    return all_post_url


def get_post_text(post_home_url, save_path):
    '''
    获取帖子里的内容

    :param post_home_url: 帖子的首页
    :param save_path: 内容的保存路径
    :return:
    '''
    browser = get_new_browser()
    browser = get_url_html(browser, post_home_url)
    # 先确定帖子的发帖时间
    post_time = get_post_time(post_home_url)
    if not post_time:
        # 获取时间失败，大概率帖子被删，放弃
        return None
    if "caifuhao" in post_home_url:
        # 是财富号的内容
        return None
    elif "fangtan" in post_home_url or "gssz" in post_home_url:
        # 是访谈
        return None
    # 一般帖子
    # 3种模式，没有评论的，有评论但只够1页的，有多页评论的
    # 先判断是哪种模式
    # 确定有多少评论
    browser, comment_num_element = find_element_by_xpath(browser, "//span[@class=\"tc1 replyCount\"]", post_home_url)

    comment_num = int(comment_num_element.text)
    all_comment = []
    if comment_num > 0:
        # 有评论，看看有多少页
        browser, sumpage_element = find_element_by_xpath(browser, "//div[@class=\"zwhpager\"]/span", post_home_url)
        sumpage = sumpage_element.text
        if sumpage == "1":
            # 只有1页
            print("一共1页评论")
            browser, comment = get_post_comment(browser, post_home_url)
            all_comment.extend(comment)
        else:
            # 有多页，循环爬取
            sumpage = int(re.compile("(?<=共)\d*(?=页)").findall(sumpage_element.text)[0])
            print("一共{}页评论".format(sumpage))
            for page in range(sumpage):
                print("正在爬取第{}页评论".format(page + 1))
                page_url = post_home_url[:-5] + "_" + str(page + 1) + ".html"
                browser, comment = get_post_comment(browser, page_url)
                all_comment.extend(comment)

    # 最后爬取一定有的主楼内容
    browser, post_content = get_post_content(browser, post_home_url)
    # 最后汇总输出到文件中
    with open(os.path.join(save_path), "w", encoding='utf-8') as file:
        file.write(post_content + "\n")
        for comment in all_comment:
            file.writelines(comment + "\n")
    browser.quit()
    return


def get_post_time(post_url):
    '''
    获取帖子的发帖时间

    :param post_url: 帖子的首页
    :return: 发帖时间
    '''
    browser = get_new_browser()
    browser = get_url_html(browser, post_url)
    try:
        if "//caifuhao." in post_url:
            # 是财富号的内容
            browser, time = find_element_by_xpath(browser, "//div[@class=\"article-meta\"]/span", post_url)
            time = datetime(int(time.text[0:4]), int(time.text[5:7]), int(time.text[8:10]))
        elif "gssz" in post_url or "fangtan" in post_url:
            # 是访谈
            browser, time = find_element_by_xpath(browser, "//span[@class=\"ft_time\"]", post_url)
            time = datetime(int(time.text[3:7]), int(time.text[8:10]), int(time.text[11:13]))
        else:
            # 是一般帖子
            browser, time = find_element_by_xpath(browser, "//div[@class=\"zwfbtime\"]", post_url)
            time = datetime(int(time.text[4:8]), int(time.text[9:11]), int(time.text[12:14]))
        browser.quit()
        return time
    except:
        print(browser.page_source)
        # 大概率帖子被删了
        browser.quit()
        return None


def get_post_content(browser, post_url):
    '''
    获取帖子主楼的内容

    :param browser: 浏览器
    :param post_url: 帖子的首页
    :return: 浏览器，主楼内容（作者，发表时间，内容，点赞数）
    '''
    browser = get_url_html(browser, post_url)
    result = ""
    if "//caifuhao." in post_url:
        # 是财富号的内容
        browser, author = find_element_by_xpath(browser, "//a[@class=\"auth\"]", post_url)
        browser, publish_time = find_element_by_xpath(browser, "//div[@class=\"article-meta\"]/span", post_url)
        browser, title = find_element_by_xpath(browser, "//h1[@class=\"article-title\"]", post_url)
        browser, content = find_element_by_xpath(browser, "//div[@class=\"article-body\"]", post_url)
        author = author.text
        publish_time = publish_time.text
        title = title.text
        content = content.text.replace("\n", "").replace("\r", "").replace("\t", "")
        result = "{}\t{}\t{}\t{}".format(author, publish_time, title, content)
    elif "gssz" in post_url or "fangtan" in post_url:
        # 是访谈
        browser, author = find_element_by_xpath(browser, "//span[@class=\"ft_author\"]", post_url)
        browser, publish_time = find_element_by_xpath(browser, "//span[@class=\"ft_time\"]", post_url)
        browser, title = find_element_by_xpath(browser, "//div[@class=\"news_txt fl\"]", post_url)
        browser, content = find_element_by_xpath(browser, "//div[@class=\"news_text\"]", post_url)
        author = author.text
        publish_time = publish_time.text
        title = title.text
        content = content.text.replace("\n", "").replace("\r", "").replace("\t", "")
        result = "{}\t{}\t{}\t{}".format(author, publish_time, title, content)
    else:
        # 是一般帖子
        browser, author = find_element_by_xpath(browser, "//div[@id=\"zwconttbn\"]/strong/a/font", post_url)
        browser, publish_time = find_element_by_xpath(browser, "//div[@class=\"zwfbtime\"]", post_url)
        # browser, title = find_element_by_xpath(browser, "//div[@id=\"zwconttbt\"]", post_url)
        browser, content = find_element_by_xpath(browser, "//div[@id=\"zwconbody\" or @class=\"zwcontentmain\"]",
                                                 post_url)
        browser, like_num = find_element_by_xpath(browser, "//div[@id=\"zwcontent\"]/div[3]/div[1]/span", post_url)
        author = author.text
        publish_time = publish_time.text[4:23]
        # title = title.text
        content = content.text.replace("\n", "").replace("\r", "").replace("\t", "")
        like_num = int(like_num.text) if like_num.text != "点赞" else 0  # 如果是里面的内容是点赞，说明没人赞
        # result = "{}\t{}\t{}\t{}".format(author, publish_time, title, content)
        result = "{}\t{}\t{}\t{}".format(author, publish_time, content, like_num)
    return browser, result


def get_post_comment(browser, post_url):
    '''
    获取帖子的全部评论（目前仅能获取一级评论）

    :param browser: 浏览器
    :param post_url: 帖子首页
    :return: 浏览器，所有评论（作者，发表时间，内容，点赞数）
    '''
    browser = get_url_html(browser, post_url)
    result = []
    # 获取一级评论
    browser, comment_elements = find_elements_by_xpath(browser,
                                                       "//div[@id=\"comment_all_content\"]/div[@id=\"zwlist\"]/div",
                                                       post_url)
    for i in range(len(comment_elements)):
        print("第{}条评论————————————————————".format(i + 1))
        now_level1_item = "//div[@id=\"comment_all_content\"]/div[@id=\"zwlist\"]/div[{}]/div[1]".format(i + 1)
        # 作者
        browser, author_element = find_element_by_xpath(browser, now_level1_item + "/div[1]/a", post_url)
        # 发表时间
        browser, publish_time_element = find_element_by_xpath(browser, now_level1_item + "/div[2]", post_url)
        # 评论内容
        browser, comment_content_element = find_element_by_xpath(browser, now_level1_item + "/div[3]/div[1]", post_url)
        # 用js脚本修改标签的属性，让全文显示出来
        js = "var divset=document.getElementsByTagName(\"" + str(
            comment_content_element.tag_name) + "\");for (var i = 0; i<divset.length;i++) {divset[i].style.display='block';};"
        browser.execute_script(js)
        # 等待3秒让内容加载出来
        time.sleep(3)
        # 重新获取评论正文
        browser, comment_content_element = find_element_by_xpath(browser, now_level1_item + "/div[3]/div[1]", post_url)
        print(comment_content_element.text)
        if comment_content_element.text == "抱歉！内容已删除":
            # 评论已被删除，跳过
            continue

        # 获取该评论的点赞数
        browser, like_element = find_element_by_xpath(browser, now_level1_item + "/div[4]/div[1]/span[5]/span",
                                                      post_url)
        author = author_element.text
        publish_time = publish_time_element.text[4:23]
        comment_content = comment_content_element.text.replace("\n", "").replace("\r", "").replace("\t", "")
        like = int(like_element.text) if like_element.text != "点赞" else 0  # 如果是里面的内容是点赞，说明没人赞
        result.append("{}\t{}\t{}\t{}".format(author, publish_time, comment_content, like))
    return browser, result


def get_url_main():
    '''
    获取帖子网址的主函数

    :return:
    '''
    with open("stock_list.txt", "r", encoding='utf-8') as file:
        lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i][:-1]
    stock_name_list = lines[::2]
    stock_url_list = lines[1::2]
    for stock_url, stock_name in zip(stock_url_list, stock_name_list):
        all_post_url = get_stock_all_post_url(stock_url, stock_name, datetime(2019, 11, 30), datetime(2020, 10, 31))
        print("共收集到{}个帖子url".format(len(all_post_url)))
        # # 记录下来
        save_path = "stock_post_url"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        with open(os.path.join(save_path, stock_name + "_post_url.txt"), "w", encoding='utf-8') as file:
            for post_url in all_post_url:
                # print(post_url)
                file.write(post_url + "\n")
    print("done")


def get_post_text_main():
    '''
    获取帖子内容的主函数

    :return:
    '''
    post_url_file_list = []
    for filename in os.listdir("stock_post_url"):
        if "_post_url" in filename:
            post_url_file_list.append(os.path.join("stock_post_url", filename))
    for post_url_file in post_url_file_list:
        with open(post_url_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
            count = 0
            for line in lines[:-1]:  # 最后一行是总结信息
                line = line.split("\t")
                post_url = line[1].strip()
                # print(post_url)
                file_name = str(count) + ".txt"
                save_path = os.path.join("stock_comment", os.path.split(post_url_file)[1][:-13])
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                file_path = os.path.join(save_path, file_name)
                get_post_text(post_url, file_path)
                count += 1


if __name__ == '__main__':
    # get_url_main()
    get_post_text_main()

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
exe_path = "chromedriver.exe"
chrom_options = Options()
chrom_options.add_argument("--headless")
chrom_options.add_argument("--disable-gpu")
browser = webdriver.Chrome(executable_path=exe_path, chrome_options=chrom_options)
browser1 = webdriver.Chrome(executable_path=exe_path, chrome_options=chrom_options)
browser2 = webdriver.Chrome(executable_path=exe_path, chrome_options=chrom_options)
browser.quit()
browser1.quit()
browser2.quit()

# -*- coding: utf-8 -*-
"""通过文件最后修改时间计算指定时间内模块文件夹中文件的变化率"""
__author__ = 'Huang Lun'
import requests
from bs4 import BeautifulSoup

# 伪装浏览器
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                  '/58.0.3029.110 Safari/537.36',
    }


def get_news_list(headers):
    """爬取虎扑的NBA新闻"""
    url = 'https://voice.hupu.com/nba'  # 需要爬的网站

    # 请求虎扑网，获取其text文本
    html_data = requests.get(url, headers=headers).text

    # 用bs4对获取的内容进行解析
    soup = BeautifulSoup(html_data, 'html5lib')

    # 从解析文件中通过select选择器定位指定的元素，返回一个列表
    news_titles = soup.select('div.list-hd > h4 > a')

    # 对返回的列表进行遍历
    datas = {}
    for news_title in news_titles[:5]:
        # 提取标题和链接信息
        title = news_title.get_text()
        link = news_title.get('href')
        datas[title] = link
    return datas  # 返回结果


def save_data(headers):
    """把新闻存入数据库"""
    datas = get_news_list(headers)  # 获取新闻来源
    for title in datas.keys():
        print(title)
        html_data = requests.get(datas[title], headers).text  # 获取text文本
        soup = BeautifulSoup(html_data, 'html5lib')  # 用bs4对获取的内容进行解析
        source = soup.find('span', class_='comeFrom').a.get_text()  # 获取来源
        print(source)

        # 获取正文
        body = soup.find_all('p')
        for p in body:
            if p.string:
                print(p.string.strip())
        pub_time = soup.find('a', class_='time').span.get_text().strip()  # 获取发布时间
        print(pub_time)
        editor = soup.find('span', id='editor_baidu').get_text().split('：')[-1][:-1]  # 获取编辑
        print(editor)
        # s = Source(name=source)
        # n = News(
        #     title=title,
        #    body=body,
        #    pub_time=pub_time,
        #    source=s,
        #    editor=editor
        # )
        # print(n)

save_data(headers)

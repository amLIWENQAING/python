#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import re

baseURL = "http://xwxmovie.cn/"
headers = {
    'Host': 'xwxmovie.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/64.0.3282.167 Safari/537.36"'
}


def browser_get():
    browser = webdriver.Chrome()
    browser.get(baseURL)
    html_text = browser.page_source
    page_count = get_page_count(html_text)
    get_page_data(html_text)


# 得到总页数
def get_page_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    page_count = soup.find('span', attrs={'class': 'pages'})
    return int(page_count.get_text()[-4:-2])


def get_page_data(html):
    items = re.findall(re.compile('<div id="post-.*?class="post-.*?style="position:.*?>'
                                  '.*?<div class="pinbin-image">(.*?)</div>'
                                  '.*?<div class="pinbin-category">(.*?)</div>'
                                  '.*?<div class="pinbin-copy">(.*?)</div>'
                                  '.*?</div>', re.S), html)
    for item in items:
        if item[0].strip():
            soup = BeautifulSoup(item[0].strip(), 'html.parser')
            img = soup.find('img', attrs={'class': 'attachment-detail-image wp-post-image'})
            # 图片
            print("海报：" + img.get('src'))
        if item[1].strip():
            soup = BeautifulSoup(item[1].strip(), 'html.parser')
            categorys = soup.find_all('a')
            for category in categorys:
                print(category.get_text())
        if item[2].strip():
            soup = BeautifulSoup(item[2].strip(), 'html.parser')
            title = soup.find('a', attrs={'class': 'front-link'})
            print("电影名：" + title.get_text())
            print("链接地址：" + title.get('href'))
            date = soup.find('p', attrs={'class': 'pinbin-date'})
            print("日期：" + date.get_text())
            brief = soup.find_all('p')
            print("简介：" + brief[1].string)

if __name__ == '__main__':
    browser_get()


# 作者：阿尤小红
# 链接：https://juejin.im/post/5aab774ef265da2389257914
# 来源：掘金
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
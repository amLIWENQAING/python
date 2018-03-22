# -*- coding:utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup

headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87'
}
i = 1
for x in range(1, 20):
    url = "https://www.zhihu.com/question/22856657/answers/created?page="+str(x)
    r = requests.get(url, headers=headers)
    # a = r.content.decode("utf-8")

    match = re.findall('data-original=.*?jpg', r.text)
    if match:
        match = list(set(match))
        # 输出匹配的内容到控制台
        for x in match:
            try:
                urlpic = re.findall('https:.*?jpg', x)
                print("图片地址：" + urlpic[0])
                pic = requests.get(urlpic[0], timeout=1000)
                print("图片正在下载")
            except requests.exceptions.ConnectionError:
                print('【错误】当前图片无法下载')
                continue
            d = './images/' + 'keyword' + '_' + str(i) + '.jpg'
            fp = open(d, 'wb')
            fp.write(pic.content)
            fp.close()
            i += 1
            print("图片下载完毕")

    else:
        # 输出html代码到控制台
        print('暂无')
print("共下载"+str(i)+"张图片")
print("程序执行完毕")
# print(r.text)

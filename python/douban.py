# -*- coding:utf-8 -*-

import requests
import json
import pymysql

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en",
    "Connection": "keep-alive",
    "Host""": "movie.douban.com",
    "Referer": "https://movie.douban.com/tag/",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
}
# 打开数据库连接
db = pymysql.connect("localhost", "root", "root", "douban", charset="utf8")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()


start = 0
while True:
    url = "https://movie.douban.com/j/new_search_subjects?sort= &range=7,8&tags=%E7%94%B5%E5%BD%B1&start="+str(start)
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)["data"]
    print(data)
    for x in data:
        print("电影名：", x["title"])
        print("评分：", x["rate"])
        print("导演：", ','.join(x["directors"]))
        print("演员：", ','.join(x["casts"]))
        print("豆瓣地址：", x["url"])
        title = x["title"]
        rate = x["rate"]
        directors = ','.join(x["directors"])
        casts = ','.join(x["casts"])
        url = x["url"]
        try:
            # 执行sql语句
            cursor.execute("INSERT INTO movies (title,rate,directors,casts,URL) VALUES (%s,%s,%s,%s,%s)",
                           (title, rate, directors, casts, url))

        except:
            # 如果发生错误则回滚
            db.rollback()
    if len(data) == 0:
        break
    start += 20


# 提交到数据库执行
db.commit()
# 关闭数据库连接
db.close()
print("程序执行完毕")
# print(r.text)

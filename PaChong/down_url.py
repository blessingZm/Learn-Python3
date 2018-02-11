# -*- coding: utf-8 -*-
'''
获取湖北省自动气象站综合显示分析系统的所有链接网址
'''
from selenium import webdriver
from bs4 import BeautifulSoup as B_S
import requests
url = r'http://10.104.235.2/hbzd/'
url_fir = 'gjdsz'
headers = {"Host":	"10.104.235.2",
            "User-Agent":   "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0)",
            "Accept	":  "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language":  "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding":  "gzip, deflate",
            "Cookie	":   "JSESSIONID=481C7EA86CC1E48A5481A2E926B54DD3",
            "Connection":   "keep-alive"
           }
res = requests.get(url+url_fir,headers = headers,timeout = 5)
res.raise_for_status()
soup = B_S(res.text, 'lxml')
my_soup = soup.find_all(id = "product")[0].find_all('a')
print(my_soup)
link_href = {}
for text in my_soup:
    if len(text.attrs) < 2:
        link_href[text.string] = text.get('href')
print(link_href)
links = [url+v for v in link_href.values()]
print(links)
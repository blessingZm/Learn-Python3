# -*- coding: utf-8 -*-
#Created on Sat Jun  3 23:46:44 2017
#@author: ZM
'''
##下载当前时间的各负氧离子站数据
'''
import datetime
import requests
import openpyxl
from bs4 import BeautifulSoup as B_S
def end_Time():
    a = datetime.datetime.today().timetuple()
    b = [str(i) for i in a[0:5]]
    for j in range(1,5):
        if int(b[j])<10:
            b[j] = '0'+b[j]
    b.append('00')
    b[4] = str(int(b[4])//10*10)
    endtime = '-'.join(b[0:3])+'%20'+':'.join(b[3:6])
    return endtime

file='station.xlsx'
wb=openpyxl.load_workbook(file)
my_sheet=wb.get_sheet_by_name('湖北_负离子站')
n=len(my_sheet['a'])
stcd=[val.value for val in my_sheet['a']]
stnm=[val.value for val in my_sheet['b']]
data={}
for i in range(n):
    url='http://172.20.10.88:8181/AnionChart/Default.aspx?stcd=%s&\
stnm=%s&endTime=%s' % (stcd[i],stnm[i],end_Time())
    try:
        res=requests.get(url)
        res.raise_for_status()
    except requests.HTTPError:
        pass
    else:
        soup=B_S(res.text,'lxml')
        try:
            my_soup=soup.find_all(id="UpdatePanel1")[0].find_all('tr')[1]
        except IndexError:
            print(stnm[i]+'无数据')
        else:      
            data[stnm[i]]=[]
            for j in my_soup.find_all('td'):
                data[stnm[i]].append(j.string)          
# -*- coding: utf-8 -*-
#Created on Thu Jun  1 22:59:24 2017
#@author: ZM
"""
elenium webdriver
根据输入的开始、结束时间批量下载负氧离子数据
"""


import openpyxl
import time
from selenium import webdriver

def down_data(url):
    fp=webdriver.FirefoxProfile(r'C:\Users\ZM\AppData\Roaming\Mozilla\Firefox\Profiles\2jxjz7a8.my_profile')
    browser=webdriver.Firefox(fp)
    browser.get(url)
   
    starttimeElem = browser.find_element_by_id('startIP')
    starttimeElem.click()
    starttimeElem.clear()
    starttimeElem.send_keys(startTime)
    
    endtimeElem = browser.find_element_by_id('endIP')
    endtimeElem.click()
    endtimeElem.clear()
    endtimeElem.send_keys(endTime)
    
    linkElem = browser.find_element_by_id('exportBtn')
    linkElem.click()
    time.sleep(3)
    browser.quit()

def istime_and_timecomp(starttime, endtime):
    try:
        istime_start=time.strptime(starttime,  '%Y-%m-%d %H:%M:%S')
        istime_end=time.strptime(endtime,  '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return False
    else:
        one_condition=istime_start[5] == 0 and istime_end[5] == 0
        two_condition=istime_start[4] % 10 == 0 and istime_end[4] % 10 == 0
        three_condition=endtime > starttime
        if one_condition and two_condition and three_condition:
            return True
        else:
            return False
    
file = 'station.xlsx'
wb = openpyxl.load_workbook(file)
my_sheet = wb.get_sheet_by_name('湖北_负离子站')
n = len(my_sheet['a'])
stcd = [val.value for val in my_sheet['a']]
stnm = [val.value for val in my_sheet['b']]
print('\t\t\t请输入要下载的时间段')
print('\t时间秒为0,分为10的倍数,格式为YY-MM-DD HH:MM:SS:')
startTime = input('请输入开始日期、时间：')
endTime = input('请输入结束日期、时间：')
while True:
    if istime_and_timecomp(startTime,endTime):
        end_Time = endTime.replace(' ', '%20')
        for i in range(n):
            url = 'http://172.20.10.88:8181/AnionChart/Default.aspx?stcd=%s&\
stnm=%s&endTime=%s' % (stcd[i], stnm[i], end_Time)
            down_data(url)
        break
    else:
        print('时间输入错误,请重新输入：')
        startTime = input('请输入开始日期、时间：')
        endTime = input('请输入结束日期、时间：')

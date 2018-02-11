#利用重要报统计雷暴日数
import os
# 本机暂无文件
path_f = r'G:\zm\python\重要报文件'
'''
##改名
for i in range(2014,2018):
    path = path_f + '\\' + str(i)
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            file = os.path.join(root, filename)
            new_file=file.split(('.'))[0]+'.txt'
            os.rename(file,new_file)
'''
##统计雷暴日数

a = '94917'
for i in range(2014, 2018):
    count = 0
    path = path_f + '\\' + str(i)
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            file = os.path.join(root, filename)
            with open(file) as f:
                for line in f.readlines():
                    if a in line:
                        count += 1
    print(i, count)

"""
给飞科整理逆温层的数据
"""
import os
from liCF.the_index import the_index


path = r'G:\各数据文件\高空\测风秒数据'
files = os.listdir(path)
with open('111.txt', 'w') as w:
    for file in files:

        date = file.split('_')[4][0:8]
        time = file.split('_')[4][8:10]
        w.write(date + ' ' + time + ' ')

        dataTime = []
        dataT = []
        dataH = []


        with open(os.path.join(path, file), 'r') as f:
            for i in range(1000):
                d = f.readline()
                if 'ZCZC SECOND' in d:
                    break

            for i in range(1000):
                d = f.readline().split(' ')
                if d[1] != '/////':
                    dataTime.append(d[0])
                    dataT.append(d[1])
                    dataH.append(d[11])
                if int(d[11]) > 1500:
                    break

        dataT = [float(d) for d in dataT]
        index = the_index(dataT)
        if index:
            if 'U' in index[0]:
                for i in range(4):
                    if i < len(index):
                        indexNum = int(index[i].split('-')[-1])
                        w.write(str(dataTime[indexNum]) + \
                                ' ' + str(dataT[indexNum]) + \
                                ' ' + str(dataH[indexNum]) + ' ')
            elif 'D' in index[0] and len(index) > 1:
                for i in range(1, 5):
                    if i < len(index):
                        indexNum = int(index[i].split('-')[-1])
                        w.write(str(dataTime[indexNum]) + \
                                ' ' + str(dataT[indexNum]) + \
                                ' ' + str(dataH[indexNum]) + ' ')
        w.write('\n')

# !usr/bin/python3
# -*- coding: utf-8 -*-
"""
下载暴雨灾害论文相关(2010年以后）并存入数据库
包括：
    PaperRegis  发表的年份、卷号、期号、页码,
    PubTime 刊登日期,
    PaperAutor 作者,
    PaperName 论文名,
    Abstrct 摘要,
    PdfUrl  全文下载地址,
    PaperUrl 所在的暴雨灾害官网地址
存储数据库名:qxzz.db，表名：byzh
"""

import requests
from bs4 import BeautifulSoup
import re
import sqlite3
import time

paperUrl = 'http://www.byzh.org/CN/volumn/volumn_1141.shtml'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3", "Accept-Encoding": "gzip, deflate"
           }


def creat_table(table_name='byzh'):
    global db_name
    create_table_command = """
        CREATE TABLE IF NOT EXISTS {} (
        PaperRegis  VARCHAR(40),
        PubTime CHAR(10),
        PaperAutor TEXT,
        PaperName TEXT,
        Abstrct TEXT,
        PdfUrl  VARCHAR(255),
        PaperUrl VARCHAR(255)
        );""".format(table_name)
    con = sqlite3.connect(db_name)
    print(" '{}' ".format(db_name) + '....连接成功')
    # 创建命令执行游标
    cur = con.cursor()
    cur.execute(create_table_command)
    print(" '{}' ".format(table_name) + '....创建成功')


def get_papers(url):
    base_url = 'http://www.byzh.org/CN'
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    # 提取上一个链接
    privious_url = soup.find(src="../../images/btn_previous.gif").parent['href']
    privious_url = base_url + '/volumn/' + privious_url
    # 提取期刊号、刊出日期
    regis_num_and_pub_time = soup.find('span', class_='style36').text.split()
    regis_num = ' '.join(regis_num_and_pub_time[: 3])
    pub_time = regis_num_and_pub_time[3].split('：')[-1]
    # 提取作者、论文名、发表日期页码
    paper = [re.sub('\s', '', m.text) for m in soup.find_all(class_="J_VM")]
    del_num = paper.index('论文')
    # del_num = paper.index('目次')
    paper = paper[del_num + 1:]
    paper = [paper[n * 6: (n + 1) * 6] for n in range(0, int(len(paper) / 6))]

    paper_autor, paper_name, paper_regis = [], [], []
    for p in paper:
        paper_autor.append(p[1])
        paper_name.append(p[3])
        paper_regis.append(p[4].split('[')[0])
    # 获取摘要、全文pdf链接
    zhaiyao_url = [base_url + j['href'].replace('..', '') for j in soup.find_all('a', class_="J_VM")]
    pdf_url = [base_url + k['href'].replace('..', '') for k in soup.find_all(href=re.compile('download'))]
    return privious_url, pub_time, regis_num, paper_autor, paper_name, paper_regis, zhaiyao_url, pdf_url


def get_zhaiyao_text(zhaiyao_url):
    res = requests.get(zhaiyao_url, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    try:
        abstract_text = soup.find('td', class_='J_zhaiyao').text.replace('摘要', '')
    except Exception as ze:
        print(ze)
        abstract_text = '{}'.format(zhaiyao_url)
    return abstract_text


if __name__ == '__main__':
    startTime = '2010-01-01'
    db_name = 'qxzz.db'
    tableName = 'byzh'
    creat_table(tableName)

    db = sqlite3.connect(db_name)
    cursor = db.cursor()

    while True:
        try:
            previousUrl, pubTime, regisNum, paperAutor, paperName, paperRegis, zhaiyaoUrl, pdfUrl = get_papers(paperUrl)
        except Exception as e:
            bufUrl = paperUrl.split('_')
            paperUrl = bufUrl[0] + '_' + str(int(bufUrl[1].split('.')[0]) - 1) + '.shtml'
            print(paperUrl)
            continue
        else:
            if pubTime < startTime:
                break
            else:
                try:
                    for i in range(len(paperRegis)):
                        abstractText = get_zhaiyao_text(zhaiyaoUrl[i])
                        abstractText = re.sub("\'", '"', abstractText)
                        data = """('{}', '{}', '{}', '{}', '{}', '{}', '{}')""".\
                            format(paperRegis[i], pubTime, paperAutor[i],
                                   paperName[i], abstractText, pdfUrl[i], paperUrl)
                        insert_command = """insert into {} values {}""".format(tableName, data)
                        try:
                            # 利用数据库命令插入数据
                            cursor.execute(insert_command)
                        except Exception as e:
                            print(data, e, sep='   ')
                            pass
                except Exception as e:
                    print(e)
                    bufUrl = paperUrl.split('_')
                    paperUrl = bufUrl[0] + '_' + str(int(bufUrl[1].split('.')[0]) - 1) + '.shtml'
                    print(paperUrl)
                    continue
                # 事务提交
                db.commit()
                print('{} 的论文资料写入成功'.format(regisNum))
            print('等待下载前一页.......')
            time.sleep(5)
            paperUrl = previousUrl

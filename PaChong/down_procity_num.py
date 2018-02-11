"""
从业务内网数据接口清单的城市代码标识表下载全国各地的行政代码
"""

import requests
from bs4 import BeautifulSoup
import pymysql


def create_db(dbname, tablename):
    dab = pymysql.connect(host='localhost', user='zm57461', password='zm57461',
                         port=3306, charset='utf8')
    cursor = dab.cursor()
    try:
        cursor.execute('drop database {}'.format(dbname))
        print('旧库' + " '{}' ".format(dbname) + '....删除成功')
    except Exception as e:
        print(e)
    else:
        cursor.execute('create database {}'.format(dbname))
        print(" '{}' ".format(dbname) + '....创建成功')

    cursor.execute('use {}'.format(dbname))

    create_table_command = """
    CREATE TABLE IF NOT EXISTS {} (
    id  int(10) not NULL,
    address char(255),
    primary key (id))
    """.format(tablename)

    # cursor.execute('drop table if exists {}'.format(tablename))
    cursor.execute(create_table_command)
    print(" '{}' ".format(tablename) + '....创建成功')

    cursor.close()
    dab.close()


if __name__ == '__main__':
    dbName = 'Adminis_coding'
    tableName = 'coding'

    url = 'http://10.104.89.55/cimissapiweb/page/apipages/table/V_ACODE.jsp'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Cookie": "JSESSIONID=FEDFE09A6824DC9F87FF70EB89DDE911; hbqxj=20111210"
    }
    cookie = {
        "JSESSIONID": "FEDFE09A6824DC9F87FF70EB89DDE911",
        "hbqxj": "20111210"
    }
    res = requests.get(url, headers=headers, cookies=cookie)
    soup = BeautifulSoup(res.text, 'lxml')
    td = soup.find_all('td')
    allList = []
    for t in td:
        if t.text.split() and '显示详细信息' not in t.text.split():
            allList.append(t.text.split())
    create_db(dbName, tableName)
    db = pymysql.connect(host='localhost', user='zm57461', password='zm57461',
                         db='{}'.format(dbName), port=3306, charset='gbk')
    curSor = db.cursor()
    count = 0
    for i in range(len(allList) // 2):
        data = "({},'{}')".format(allList[i * 2 + 1][0], allList[i * 2][0])
        insert_command = """insert into {} values {}""".format(tableName, data)
        try:
            curSor.execute(insert_command)
            count += 1
        except curSor.Error:
            db.rollback()
    db.commit()
    print('共插入{}条数据'.format(count))
    curSor.close()
    db.close()

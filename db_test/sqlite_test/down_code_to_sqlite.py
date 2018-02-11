"""
从业务内网数据接口清单的城市代码标识表下载全国各地的行政代码并存入sqlite数据库
"""

import requests
from bs4 import BeautifulSoup
import sqlite3


if __name__ == '__main__':
    dbName = 'Adminis_coding.db'
    tableName = 'coding'
    create_table_command = """
    CREATE TABLE IF NOT EXISTS {} (
    id  int(10) primary key not NULL,
    address char(255)
    );""".format(tableName)

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

    # 连接数据库，若数据库不存在，则创建该数据库
    try:
        db = sqlite3.connect(dbName)
        print(" '{}' ".format(dbName) + '....连接成功')
    except Exception as e:
        print(e)
    else:
        # 创建命令执行游标
        cursor = db.cursor()
        try:
            # 利用数据库命令创建表
            cursor.execute(create_table_command)
            print(" '{}' ".format(tableName) + '....创建成功')
        except Exception as e:
            print(e)
        else:
            count = 0
            for i in range(len(allList) // 2):
                data = "({},'{}')".format(allList[i * 2 + 1][0], allList[i * 2][0])
                insert_command = """insert into {} values {}""".format(tableName, data)
                try:
                    # 利用数据库命令插入数据
                    cursor.execute(insert_command)
                except Exception as e:
                    print(data, e, sep='   ')
                else:
                    count += 1
            # 事务提交
            db.commit()
            print('共插入{}条数据'.format(count))
        cursor.close()
        db.close()

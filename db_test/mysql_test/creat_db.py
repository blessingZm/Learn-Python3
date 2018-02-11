import pymysql


# 创建名字为dbname的数据库
def creat_db(host, user, password, dbname):
    db = pymysql.connect(host=host, user=user, password=password,
                         port=3306)
    cursor = db.cursor()
    try:
        # 执行创建数据库命令
        cursor.execute('create database {}'.format(dbname))
        print('\'{}\'- - - - your database create successfully!'.format(dbname))
    except Exception:
        # 若数据库已存在，则会创建失败
        print('\'{}\'- - - - your database is exist!'.format(dbname))
    cursor.execute('show databases')
    rows = cursor.fetchall()
    print(rows)
    db.close()

creat_db('localhost', 'zm57461', 'zm57461', 'test')

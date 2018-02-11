import pymysql


db = pymysql.connect(host='localhost', user='zm57461', password='zm57461',
                     db='test', port=3306, charset='utf8')
cursor = db.cursor()
# insertCommand = "insert into trade (name, account, saving) values "
# sqlData = "('DM', '13131351', 1000)"
selectCommand = 'select id from trade where saving > 100'
cursor.execute(selectCommand)
print(cursor.fetchall())
cursor.close()
db.close()

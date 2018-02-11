from collections import Counter
import sqlite3
import jieba
import matplotlib .pyplot as plt
from wordcloud import WordCloud
import os


dbName = 'qxzz.db'
tableName = 'byzh'
db = sqlite3.connect(dbName)
cursor = db.cursor()

selectCommand = "select PaperName from {} where PaperAutor is not ''".format(tableName)
cursor.execute(selectCommand)
paperNameS = [name[0] for name in cursor.fetchall()]
# print(paperNameS, len(paperNameS), sep='\n')
paperNameS = ''.join(paperNameS)
# 设置停用词
stopWords = [word.strip() for word in open('stopword.txt', 'r')]
# 全模式
# seqListSyntype = jieba.cut(paperNameS, cut_all=True)
# 精确模式,同时去除停用词
seqListExact = [word for word in jieba.cut(paperNameS, cut_all=False) if word not in stopWords and len(word) > 1]
# 搜索引擎模式
# seqList = jieba.cut_for_search(paperNameS)
# print(seqListExact)

# 统计词频
datas = dict(Counter(seqListExact))
datas = sorted(datas.items(), key=lambda d: d[1])
print(datas, len(datas), sep='\n')

# 绘制词云
font = os.path.join(os.path.dirname(__file__), 'simsun.ttc')
myWordCloud = WordCloud(font_path=font, max_font_size=60).generate(' '.join(seqListExact))
plt.imshow(myWordCloud)
plt.axis('off')
plt.show()

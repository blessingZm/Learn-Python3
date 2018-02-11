import requests
from bs4 import BeautifulSoup
from urllib import request
import urllib
import time

def get_everyone_url(firsturl):
    res = requests.get(firsturl)
    soup = BeautifulSoup(res.content, 'lxml')
    boxs = soup.find_all('div', class_='img')
    endurls = []
    for box in boxs:
        endurl = box.find('a')['href']
        endurls.append(endurl)
    return endurls


# 从个人网址中两次解析，最终得到以文件名为key，以图片地址为value的字典
# 注意：最后图片地址需要加上图片基本地址：http://www.xiaohuar.com
def get_imgurl(endurl):
    # 从原始网址找到的个人网址
    res = requests.get(endurl)
    soup = BeautifulSoup(res.content, 'lxml')
    imgcontents = soup.find_all('div', class_='p-tmb')
    # 解析得到大图网址
    try:
        imgurl = imgcontents[0].find('a')['href'] + '#p1'
    except IndexError:
        pass
    # 从大图网址解析
    else:
        resultres = requests.get(imgurl)
        resultsoup = BeautifulSoup(resultres.content, 'lxml')
        # 得到人名
        namesoup = resultsoup.find('div', class_='pic_midd_warp')
        name = namesoup.find_all('a')[-1].text
        # 得到图片位置
        imgjpgs = resultsoup.find_all('div', class_='inner')
        i = 0
        imgdict = {}
        for img in imgjpgs:
            # 得到确定图片地址
            imglink = img.find('a')['href']
            # 图片名称用人名+序号
            imgname = name + '-' + str(i) + '.jpg'
            imgdict[imgname] = imglink
            i += 1
        return imgdict


# 下载图片
def down_image(filename, myurl):
    try:
        req = urllib.request.Request(myurl, headers=headers)
    except urllib.error.HTTPError:
        pass
    else:
        respon = urllib.request.urlopen(req)
        get_img = respon.read()
        with open(filename, 'wb') as fp:
            fp.write(get_img)
    return


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/47.0.2526.80 Safari/537.36'
    }
    imgBaseUrl = 'http://www.xiaohuar.com'
    urls = ["http://www.xiaohuar.com/list-1-{}.html".format(i)
            for i in range(1, 3)]
    allXhUrls = []
    for url in urls:
        endUrls = get_everyone_url(url)
        allXhUrls.append(endUrls)

    for u in allXhUrls:
        for everyUrl in u:
            imgDicts = get_imgurl(everyUrl)
            if imgDicts:
                for file, link in imgDicts.items():
                    imgLink = imgBaseUrl + link
                    down_image(".\\xh\\{}".format(file), imgLink)
                    time.sleep(1)
                time.sleep(3)


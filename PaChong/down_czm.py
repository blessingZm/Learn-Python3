import os
import requests
from urllib.request import urlretrieve
import time
import urllib
import random



def get_imgname(starturl):
    imglists = []
    res = requests.get(starturl, headers=headers, cookies=cookies, timeout=10).text.split('\"')
    for link in res:
        if '.jpg' in link:
            imglists.append(link)
    return imglists


# startUrls = ['http://photo.weibo.com/photos/get_all?uid=1858902482&album_id=3561906062066809&count=30&page={}&type=3'
#              .format(i + 1) for i in range(24, 38)]
# imgPath = '.\\czm'

# startUrls = ['http://photo.weibo.com/photos/get_all?uid=1843875727&album_id=3560921868595187&count=30' \
#              '&page={}&type=3&__rnd={}'.format(i + 1, random.randint(1510147000000, 1510149000000)) for i in range(10, 13)]
# imgPath = '.\\grz'

# startUrls = ['http://photo.weibo.com/photos/get_all?uid=3116872295&album_id=3660405166763040&count=30' \
#              '&page={}&type=3&__rnd={}'.format(i + 1, random.randint(1510147000000, 1510149000000))
#              for i in range(5, 15)]
# imgPath = '.\\hwn'

startUrls = ['http://photo.weibo.com/photos/get_all?uid=1942828717&album_id=3561610078467588&count=30' \
             '&page={}&type=3&__rnd={}'.format(i + 1, random.randint(1510312000000, 1510315000000)) for i
             in range(60, 65)]
imgPath = '.\\xqm'

imgBaseUrl = 'http://wx3.sinaimg.cn/large/'
headers = {
    "Host": "photo.weibo.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cookie": "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFls8bXCB5fl7e3pUo2L63C5JpX5KMhUgL.FoepS0B0Sozpeh52dJLoI7_bdsH0McLV9fvAdBtt; "
              "UOR=www.hao123.com,weibo.com,spr_qdhz_bd_baidusmt_weibo_s; "
              "SINAGLOBAL=3398522027797.7847.1503031560911; "
              "ULV=1510312503668:7:2:2:2871036999026.4062.1510312503666:1510146975118; "
              "SCF=Al57h7DdZx26VsJftb0XDd0-68rNa3iKRLWzuBhrLZzbZDyCtD4jYI9ePW-nbjAIn0ETZHATbv3ZpABLVaOBbS4.; "
              "SUHB=0M2F8KQFmCzlUM; ALF=1541848498; un=18707209861; "
              "SUB=_2A253AfpjDeRhGeVP7FYS9izNyzyIHXVUd2yrrDV8PUNbmtBeLWbwkW-XGsyYaNFom9bGpcLwMG3Hda6liw..; "
              "SSOLoginState=1510312499; httpsupgrade_ab=SSL; _s_tentry=-; "
              "Apache=2871036999026.4062.1510312503666; USRANIME=usrmdinst_43; "
              "WBStorage=82ca67f06fa80da0|undefined",
    "Cache-Control": "max-age=0"
}
cookies = {
    "SINAGLOBAL":	"4193160347688.4595.1500797105437",
    "ULV":	"1501129703794:3:3:3:252538536….1501129703790:1500980148217",
    "SCF":	"AtHoM-bt0Wkqwx8qPc2LTwEvXB-N0…ImyRLTySZgO82yZPgn6IfCqqiBU.",
    "SUBP":	 "0033WrSXqPxfM725Ws9jqgMF55529…eK57Ws4DqcjTqJpLMNSDdJUkwJXt",
    "SUHB": "0P1M_ApnmWH0xm",
    "un":	"18707209861",
    "wvr":	"6",
    "UOR":	",,www.hao123.com",
    "ALF":	"1532665714",
    "SUB":	"_2A250ffBnDeRhGeVP7FYS9izNyzy…f5YxqcbgoyA2gZyZRwR0Lk8AHA..",
    "login_sid_t": 	"98d6efced1f9038f21b7cca2d5ee1af5",
    "_s_tentry":	"-",
    "Apache	": "252538536508.90723.1501129703790",
    "SSOLoginState	": "1501129714",
}

os.makedirs(imgPath, exist_ok=True)
i = int(startUrls[0].split('page=')[-1].split('&')[0])
for startUrl in startUrls:
    # 取得当前页的所有图片名
    imgLists = get_imgname(startUrl)
    print('已取得第{}页的所有图片链接！'.format(i))
    time.sleep(3)
    for index, img in enumerate(imgLists):
        # 设置保存的图片名，取得图片的真实地址：基础地址+获得的图片名
        filename = str(i) + '-' + str(index) + '.jpg'
        realUrl = imgBaseUrl + img
        # 下载图片
        try:
            urlretrieve(realUrl, os.path.join(imgPath, filename))
        except:
            pass
        time.sleep(2)
    print('第{}页的所有图片下载完成...'.format(i))
    i += 1
    time.sleep(3)

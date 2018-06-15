#! usr/bin/env python
# 省级FTP  A、J、Y文件下载
import ftplib
from ftplib import FTP
import os
from FTPsome import FTP_AJ_getusers
import time


# 获取所有子目录
def getpaths(user, pswd):
    resultList = []
    paths = []
    try:
        ftp.login(user= user, passwd= pswd)
    except ftplib.all_errors:
        print('FTP连接失败!')
    else:
        print(ftp.getwelcome())
        ftp.dir(bathPath, resultList.append)
        for buf in resultList:
            # 判断是否为目录
            if buf.startswith('drw') and not buf.endswith('.'):
                paths.append(buf.split(' ')[-1])
    return paths


# 复制ftp目录中的文件（仅为文件，不包括文件夹）到本地目录
def savefile(localpath, ftppath):
    ftp.cwd(ftppath)
    files = ftp.nlst(ftppath)
    # 这里可以选择下载的月份
    # file.split('.')[0].endswith('{}'.format(month))
    for file in files:
        if os.path.exists(os.path.join(localPath, file)):
            if ftp.size(file) <= os.path.getsize(os.path.join(localPath, file)):
                continue
            else:
                os.remove(os.path.join(localPath, file))
        with open(os.path.join(localpath, file), 'wb') as f:
            ftp.retrbinary("RETR" + file, f.write, blocksize= 8192)
    print(ftppath + '目录下的所有文件复制成功!')


if __name__ == '__main__':
    # ftp地址、端口、连接延时
    host = '10.104.233.1'
    port = 21
    timeOut = -999
    # 需要下载的数据年份
    years = range(2018, 2019)

    # 登录名、密码
    for userCity, userName, passWord in FTP_AJ_getusers.get_users():
        # 根据登录的用户创建相应地市的本地城市目录
        localCityPath = 'G:\\各数据文件\\1地面数据\\全省月报表_省局下发\\{}'.format(userCity)
        os.makedirs(localCityPath, exist_ok=True)
        print("开始下载{} 的A文件....".format(userCity))
        # 创建ftp连接
        ftp = FTP()
        ftp.connect(host= host, port= port, timeout=timeOut)
        for year in years:
            # bathPath:最初远程目录，分别下载bathPath和subPaths(所有子目录）下的文件
            bathPath = '/{}/'.format(year)
            # 本地年份目录
            localPath = os.path.join(localCityPath, str(year))
            os.makedirs(localPath, exist_ok=True)
            # 获取子目录
            subPaths = [bathPath + path + '/'
                        for path in getpaths(userName, passWord)]
            # 复制子目录中的txt文件(A文件）
            for ftpPath in subPaths:
                try:
                    savefile(localPath, ftpPath)
                except ftplib.error_perm:
                    pass
            # 复制根目录中的txt文件（Y文件）
            try:
                savefile(localPath, bathPath)
            except ftplib.error_perm:
                pass
            print('{} {}年的数据复制完成'.format(userCity, year))
            print('*********************************')
        ftp.quit()
        time.sleep(5)

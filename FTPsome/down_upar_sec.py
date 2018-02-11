# 从国家内网FTP下载高空秒数据文件

from ftplib import FTP
import os

ftp = FTP()
IP = '10.1.64.235'
port = 21
ftp.connect(IP, port)
ftp.login()
base_path = '/UPAR_WEA_CHN_MUL_FTM_SEC/datasets/'
local_base_path = 'G:\\各数据文件\\高空'
end_paths = [str(i) + '/' for i in range(2009, 2010)]
print(end_paths)

for end_path in end_paths:
    path = base_path + end_path
    local_path = (local_base_path + path).replace('/', '\\')
    os.makedirs(local_path, exist_ok=True)
    ftp.cwd(path)
    filename = ftp.nlst(path)
    bufsize = 100000
    for file in filename:
        if file.endswith('tar') and file.split('.')[0] >= '20090714':
            local_file = os.path.join(local_path, file)
            fp = open(local_file, 'wb')
            ftp.retrbinary('RETR '+file, fp.write, bufsize)
ftp.set_debuglevel(0)
ftp.quit()

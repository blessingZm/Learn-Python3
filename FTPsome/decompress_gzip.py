"""
gzip文件批量解压缩,并删除原始压缩文件
文件复制：
import shutil
shutil.copy(file, intent_path)
"""

import gzip
import os


def decompress(path, in_filename, out_filename):
    infile = os.path.join(path, in_filename)
    outfile = os.path.join(path, out_filename)
    with gzip.open(infile, 'rb') as in_f:
        file_content = in_f.read()
    with open(outfile, 'wb') as out_f:
        out_f.write(file_content)
    os.remove(infile)

# base_path = r'G:\各数据文件\高空\UPAR_WEA_CHN_MUL_FTM_SEC\datasets'
base_path = r'G:\python\uper_hb'
for roots, paths, files in os.walk(base_path):
    for in_file in files:
        if in_file.endswith('.gz'):
            # 改变输出的文件名
            file_buf = in_file.split('-')
            out_file = '-'.join(file_buf[1:3]).replace('.gz', '')
            decompress(roots, in_file, out_file)

"""
从原始文件目录拷贝需要的文件到相应目录
"""

import os
import shutil


uperPath = r'G:\各数据文件\高空\UPAR_WEA_CHN_MUL_FTM_SEC\datasets'
years = range(2014, 2017)

stations = ['57461', '57494', '57447']
finalPath = r'G:\python\uper_hb'

for station in stations:
    endPath = os.path.join(finalPath, station)
    os.makedirs(endPath, exist_ok = True)
    for year in years:
        origiPath = os.path.join(uperPath, str(year))
        for root, dir, files in os.walk(origiPath):
            for file in files:
                if station in file:
                    shutil.copy(os.path.join(root, file), os.path.join(endPath, file))

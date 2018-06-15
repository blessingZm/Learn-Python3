"""
统计风向相符率及各风向频率
"""

import os
import re
import pandas as pd
import numpy as np
from datetime import datetime


APATH = r'.\新旧站AJ'
OLDSTR = 'a\d+-\d+-9.txt'
NEWSTR = 'a\d+-\d+.txt'
HOURS = ['21', '22', '23'] + [str(i).zfill(2) for i in range(21)]
wind_direc = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
              'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'C']


class GetWdatas:
    def __init__(self, wd_num=2):
        self.wd_num = wd_num

    # 提取风向风速数据，并将风向转为16方位
    def parse_afile_wd(self, afile):
        year_month = afile.split('-')[1][:6]
        with open(afile, 'r') as f:
            while True:
                buf = f.readline()
                if 'FN' in buf:
                    break
            if self.wd_num != 2:
                while True:
                    buf = f.readline()
                    if '=' in buf:
                        break
            day = 1
            # 设置一天的起始行
            day_start = 0
            while True:
                day_start += 1
                buf = f.readline().strip()
                for i, b in enumerate(buf.split()):
                    hour_loc = (day_start - 1) * 6 + i
                    date = year_month + str(day).zfill(2) + HOURS[hour_loc].zfill(2)
                    if '=' in b or '.' in b:
                        b = b[:-1]
                        day_start = 0
                        day += 1
                    try:
                        ws = int(b[3:]) / 10
                    except ValueError:
                        wd = np.nan
                        ws = np.nan
                        wd_direct = np.nan
                    else:
                        if ws <= 0.2:
                            wd = np.nan
                            wd_direct = 'C'
                        else:
                            wd = int(b[:3])
                            wd_loc = int((wd + 11.25) // 22.5)
                            if wd_loc > 15:
                                wd_direct = 'N'
                            else:
                                wd_direct = wind_direc[wd_loc]
                    yield [date, wd, wd_direct, ws]
                if '=' in buf:
                    break

    def get_results(self, files):
        results = []
        for file in files:
            for x in self.parse_afile_wd(os.path.join(APATH, file)):
                results.append(x)
        w_datas = pd.DataFrame(results,
                               columns=['date', 'wd', 'wd_direct', 'ws'])
        w_datas.index = map(lambda xx: datetime.strptime(xx, '%Y%m%d%H'),
                            w_datas['date'])
        return w_datas.loc[:, ['wd', 'wd_direct', 'ws']]


# 统计风向相符率
def wd_conincidence_rate(old_datas, new_datas, group_name):
    # 风向差值绝对值
    datas = abs(old_datas['wd'] - new_datas['wd'])
    datas.index = old_datas.index
    grouped = datas.groupby(group_name)
    return grouped.agg(lambda x: x[x <= 22.5].count() / x.count() * 100)


# 月平均风向频率
def wd_frequency_month(wd_datas):
    grouped = wd_datas.groupby(['wd_direct', wd_datas.index.month])
    wd_counts = grouped['wd_direct'].count().unstack()
    wd_fres = wd_counts.apply(lambda x: x / x.sum() * 100)
    return wd_fres.loc[wind_direc, :]


# 各风向频率
def wd_frequency_direct(wd_datas):
    grouped = wd_datas.groupby('wd_direct')
    wd_counts = grouped['wd_direct'].count()
    wd_fres = pd.DataFrame(wd_counts / wd_counts.sum() * 100)
    return wd_fres.loc[wind_direc, :]


if __name__ == "__main__":
    oldFiles = [afile for afile in os.listdir(APATH) if
                re.match(OLDSTR, afile.lower())]
    newFiles = [afile for afile in os.listdir(APATH) if re.match(NEWSTR,
                afile.lower())]
    # 分别提取2分钟风、10分钟风
    wd2_datas = GetWdatas(wd_num=2)
    w10_datas = GetWdatas(wd_num=10)

    oldDatas2 = wd2_datas.get_results(oldFiles)
    newDatas2 = wd2_datas.get_results(newFiles)
    # 2分钟风向相符率
    wd2_month_rate = wd_conincidence_rate(
            oldDatas2, newDatas2, newDatas2.index.month)
    wd2_year_month_rate = wd_conincidence_rate(
            oldDatas2, newDatas2,
            [newDatas2.index.year, newDatas2.index.month]).unstack()
    # 10分钟风向相符率
    oldDatas10 = w10_datas.get_results(oldFiles)
    newDatas10 = w10_datas.get_results(newFiles)
    wd10_month_rate = wd_conincidence_rate(
            oldDatas10, newDatas10, newDatas10.index.month)
    wd10_year_month_rate = wd_conincidence_rate(
            oldDatas10, newDatas10,
            [newDatas10.index.year, newDatas10.index.month]).unstack()
    # 月平均风向频率差值
    wd_frequency_dif = wd_frequency_month(newDatas2) - wd_frequency_month(oldDatas2)
    # 各风向平均频率
    old_fres = wd_frequency_direct(oldDatas2)
    new_fres = wd_frequency_direct(newDatas2)

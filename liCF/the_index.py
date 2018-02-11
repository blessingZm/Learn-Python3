# -*- coding=utf-8 -*-
"""
寻找一组数据的各阶段峰值
包括高峰和低峰
"""


def the_index(data):
    # 每个顶点的index， D（Down）,U(Up)
    apex_index = []

    # 趋势-1(Down), 0, 1(Up)
    qs = 0

    # 偏离值和偏离百分比
    plz_p = 0.01

    # 当前值
    min_index = max_index = 0

    for index, num in enumerate(data):

        min_dqz = data[min_index]
        max_dqz = data[max_index]

        min_plz = min_dqz * plz_p
        max_plz = max_dqz * plz_p

        if (num - min_dqz) > 0:

            if (num - min_dqz - min_plz) > 0:
                if qs != 1:
                    apex_index.append('U-%s' % min_index)
                    max_index = index
                    max_dqz = num
                    # print('U-%s' % min_index)
                qs = 1

        # 下降
        if (num - max_dqz) < 0:
            if (num - max_dqz) < -max_plz:
                if qs != -1:
                    apex_index.append('D-%s' % max_index)
                    min_index = index
                    min_dqz = num
                    # print('D-%s' % max_index)
                qs = -1

        if num > max_dqz:
            max_index = index

        if num < min_dqz:
            min_index = index
    return apex_index

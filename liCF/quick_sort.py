# -*- coding: utf-8 -*-
"""
Created on Tue May 30 10:33:40 2017

@author: ZM

快速排序（从小到大）
需要从大到小时仅需要修改（1）和（2）处的大小判断
low初始为0，hight初始为len（data）-1 （因列表下标从0开始）
"""

def quick_sort(data, low, hight):

    i = low
    j = hight
    if i >= j:
        return data
    x = data[i]
    while not j <= i:
        # （1）
        while i < j and data[j] >= x:
            j -= 1
        data[i] = data[j]
        # （2）
        while i < j and data[i] < x:
            i += 1
        data[j]  = data[i]
    data[i] = x
    quick_sort(data, low, i-1)
    quick_sort(data, i+1, hight)
    return data

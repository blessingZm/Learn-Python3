# -*- coding: utf-8 -*-
"""
Created on Wed May 23 16:49:44 2018

@author: ZM
"""

import os
import xlrd
import pandas as pd


# 从excel文件中获取结果，包括单选、多选、判断三个List
def get_result(file):
    single_datas, multipul_datas, decide_datas = [], [], []
    wb = xlrd.open_workbook(file)
    ws = wb.sheet_by_index(0)
    for row in range(4, 23, 2):
        for col in range(1, 11):
            single_datas.append(ws.cell_value(row, col).upper())
    
    for row in range(25, 44, 2):
        for col in range(1, 11):
            multipul_datas.append(ws.cell_value(row, col).upper())
    
    for row in range(46, 65, 2):
        for col in range(1, 11):
            decide_datas.append(ws.cell_value(row, col).upper())
            
    return single_datas, multipul_datas, decide_datas


# 比较两个同长的List，同位置元素相同的个数，即统计正确个数
def compare_list(exam_list, answer_list):
    result = list(map(lambda x, y: 1 if x == y else 0, 
                      exam_list, answer_list))
    return sum(result)
    

if __name__ == "__main__":
    baseScore = [0.4, 0.8, 0.3]
    examPath = r".\考生结果"
    answerFile = r"答案.xlsx"
    # 存放所有人的成绩
    results = {}
    # 取出答案
    answers = get_result(answerFile)
    for file in os.listdir(examPath):
        # 考生信息
        examName = file.split('.')[0]
        # 考生的做题结果
        exams = get_result(os.path.join(examPath, file))
        # 统计分数
        scores = 0
        for i in range(len(baseScore)):
            scores += compare_list(exams[i], answers[i]) * baseScore[i]
        results[examName] = round(scores, 1)
    pdResult = pd.Series(results)
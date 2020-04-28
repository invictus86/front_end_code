#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from ekt_sfe import Ektsfe
#
# net = "192.168.1.47"
#
# specan = Ektsfe(net)
#
# specan.set_digitaltv_input_load(r"D:\TSGEN\SDTV\DVB_25Hz\720_576i\LIVE\FACT_4M.GTS")

# import json
#
# list_data = [1, 2, 3, 4]
# json_data = json.dump(list_data)
# print json_data


import numpy as np
from scipy.stats import chi2
from scipy.stats import t
from scipy.stats import f
from scipy.stats import norm

# chi square distribution
percents = [0.995, 0.990, 0.975, 0.950, 0.900, 0.100, 0.050, 0.025, 0.010, 0.005]
print np.array([chi2.isf(percents, df=i) for i in range(1, 47)])
# t distribution
percents = [0.100, 0.050, 0.025, 0.010, 0.005, 0.001, 0.0005]
print np.array([t.isf(percents, df=i) for i in range(1, 46)])
# F distribution
alpha = 0.05
print np.array([f.isf(alpha, df1, df2) for df1 in range(1, 11) for df2 in range(1, 46)]).reshape(10, -1).T
# normal distribution
print norm.ppf(np.arange(0, 0.99, 0.001).reshape(-1, 10))



# def write_json(jlist):
#     # 将bx列表写入json文件
#     with open('data/bx_list.json', 'w') as f_obj:
#         json.dump(jlist, f_obj)
#
#
# def read_json():
#     # 读取存储于json文件中的列表
#     with open('data/bx_list.json', 'r') as f_obj:
#         jlist = json.load(f_obj)
#     return jlist
#


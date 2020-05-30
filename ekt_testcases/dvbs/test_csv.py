#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 读取CSV文件
# 常用编码为UTF-8、UTF-16、GBK、GB 2312、GB 18030，
# 文件编码解码格式应对应，不然会出现乱码
import pandas as pd
from ekt_lib.ekt_utils import read_json_file

# load_dict = read_json_file("../../ekt_json/dvbs_dynamic_range_awng_min_level_resuming_measurement.json")
# list_data = load_dict.get("test_parame_result")
# print list_data
# list_required_data = []
# for i in list_data:
#     count = 0
#     for j in i[2]:
#         if count == 0:
#             list_required_data.append([i[0][1], i[1][0], j[0][0], j[1]])
#         else:
#             list_required_data.append(["", "", j[0][0], j[1]])
#         count = count + 1
# pd_data = pd.DataFrame(list_required_data, columns=['symbol_rate', 'frequency', 'code_rate', 'level'])
# pd_data.to_csv("../../ekt_test_report/1.csv", index=None)


# load_dict = read_json_file("../../ekt_json/dvbs2_dynamic_range_awng_min_level_resuming_measurement.json")
# list_data = load_dict.get("test_parame_result")
# print list_data
# list_required_data = []
# for i in list_data:
#     count = 0
#     for j in i[2]:
#         if count == 0:
#             list_required_data.append([i[0][1], i[1][0], j[0], j[1][0], j[2]])
#         else:
#             list_required_data.append(["", "", j[0], j[1][0], j[2]])
#         count = count + 1
# pd_data = pd.DataFrame(list_required_data, columns=['symbol_rate', 'frequency', 'modulation', 'code_rate', 'level'])
# pd_data.to_csv("../../ekt_test_report/1.csv", index=None)


load_dict = read_json_file("../../ekt_json/dvbs_signal_acquisition_frequency_range.json")
list_data = load_dict.get("test_parame_result")
list_required_data = []
for i in list_data:
    count = 0
    for j in i[3]:
        if count == 0:
            list_required_data.append([i[1], i[2][0], i[2][1], j[0], j[1]])
        else:
            list_required_data.append(["", "", "", j[0], j[1]])
        count = count + 1
pd_data = pd.DataFrame(list_required_data, columns=['symbol_rate', 'frequency', 'sfu_frequency', 'code_rate', 'level'])
pd_data.to_csv("../../ekt_test_report/dvbs_signal_acquisition_frequency_range.csv", index=None)

# print(os.listdir('E:/data'))
# a.to_csv('E:/data/m.csv', sep=';', index=False)
# print(os.listdir('E:/data'))

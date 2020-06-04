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


# load_dict = read_json_file("../../ekt_json/dvbt2_57_performance_gaussian_channel_resuming_measurement.json")
# list_data = load_dict.get("test_parame_result")
# print list_data
# list_required_data = []
# for i in list_data:
#     count = 0
#     for j in i[1]:
#         if count == 0:
#             list_required_data.append([i[0][0], j[0], j[1], j[2], j[3]])
#         else:
#             list_required_data.append(["", j[0], j[1], j[2], j[3]])
#         count = count + 1
# pd_data = pd.DataFrame(list_required_data, columns=['frequency', 'modulation', 'code_rate', 'spec', 'noise'])
# pd_data.to_csv("../../ekt_test_report/1.csv", index=None)


# load_dict = read_json_file("../../ekt_json/dvbt_13_verification_signal_strength_indicator_ssi.json")
# list_data = load_dict.get("test_parame_result")
# print list_data
# list_required_data = []
# for i in list_data:
#     count = 0
#     for j in i[1]:
#         if count == 0:
#             list_required_data.append([i[0][0], i[0][1], i[0][2], i[0][3], i[0][4], j[0], j[1]])
#         else:
#             list_required_data.append(["", "", "", "", "", j[0], j[1]])
#         count = count + 1
# pd_data = pd.DataFrame(list_required_data,
#                        columns=['modulation', 'code_rate', 'guard', 'bandwidth', 'frequency', 'level', 'strength'])
# pd_data.to_csv("../../ekt_test_report/1.csv", index=None)


# load_dict = read_json_file("../../ekt_json/dvbt_20_performance_0db_echo_channel.json")
# list_data = load_dict.get("test_parame_result")
# # print list_data
# list_required_data = []
# for i in list_data:
#     count = 0
#     for j in i[4]:
#         if count == 0:
#             list_required_data.append([i[0], i[3], j[0], j[1], j[2], j[3], j[4], j[5]])
#         else:
#             list_required_data.append(["", "", j[0], j[1], j[2], j[3], j[4], j[5]])
#         count = count + 1
# pd_data = pd.DataFrame(list_required_data,
#                        columns=['frequency', 'bandwidth', 'pilot','modulation',  'code_rate', 'guard',  'spec_noise',
#                                 'noise'])
# pd_data.to_csv("../../ekt_test_report/dvbt_20_performance_0db_echo_channel.csv", index=None)



# load_dict = read_json_file("../../ekt_json/dvbt_22_minimun_signal_level_0db.json")
# list_data = load_dict.get("test_parame_result")
# list_required_data = []
# for i in list_data:
#     for j in i[4]:
#         count_j = 0
#         for k in j[5]:
#             print k
#             if count_j == 0:
#                 list_required_data.append([i[0], i[3], j[0], j[1], j[2], j[3], j[4], k[0], k[1]])
#             else:
#                 list_required_data.append(["", "", "", "", "", "", "", k[0], k[1]])
#             count_j = count_j + 1
# pd_data = pd.DataFrame(list_required_data,
#                        columns=['frequency', 'bandwidth', 'pilot', 'modulation', 'code_rate', 'guard', 'spec_level','fading',
#                                 'level'])
# pd_data.to_csv("../../ekt_test_report/1.csv", index=None)

# load_dict = read_json_file("../../ekt_json/dvbt_31_performance_SFN_more_than_one.json")
# list_data = load_dict.get("test_parame_result")
# list_required_data = []
# for i in list_data:
#     count = 0
#     for j in i[5]:
#         if count == 0:
#             list_required_data.append([i[0], i[1], i[2], i[3], i[4], j[0], j[1], j[2], j[3], j[4], j[5], j[6]])
#         else:
#             list_required_data.append(["", "", "", "", "", j[0], j[1], j[2], j[3], j[4], j[5], j[6]])
#         count = count + 1
# pd_data = pd.DataFrame(list_required_data,
#                        columns=['fft_mode', 'modulation', 'code_rate', 'guard', 'spec', 'mian_att', 'mian_delay',
#                                 'pre_att', 'pre_delay', 'post_att', 'post_delay', 'noise_cn'])
# pd_data.to_csv("../../ekt_test_report/1.csv", index=None)


# load_dict = read_json_file("../../ekt_json/dvbt_32_performance_SFN_inside_guard.json")
# list_data = load_dict.get("test_parame_result")
# list_required_data = []
# for i in list_data:
#     # count = 0
#     for j in i[9]:
#         count_j = 0
#         # list_data_j = []
#         for k in j[3]:
#             # if count_j == 0:
#             # list_data_j.append([k[0], k[1]])
#             # count_j = count_j + 1
#             if count_j == 0:
#                 list_required_data.append(
#                     [i[0], i[3], i[4], i[5], i[6], i[7], i[8], j[0], j[1], j[2], k[0], k[1]])
#             else:
#                 list_required_data.append(
#                     ['', '', '', '', '', '', '', j[0], j[1], j[2], k[0], k[1]])
#             count_j = count_j + 1
# pd_data = pd.DataFrame(list_required_data,
#                        columns=['frequency', 'bandwidth', 'fft_mode', 'modulation', 'code_rate', 'guard', 'spec',
#                                 'mian_att', 'mian_delay',
#                                 'pre_delay', 'pre_att', 'noise_cn'])
# pd_data.to_csv("../../ekt_test_report/1.csv", index=None)

# load_dict = read_json_file( "../../ekt_json/dvbt_33_performance_SFN_outside_guard.json")
# list_data = load_dict.get("test_parame_result")
# list_required_data = []
# for i in list_data:
#     count = 0
#     for j in i[8]:
#         try:
#             # print i
#             if count == 0:
#                 list_required_data.append([i[0], i[3], i[4], i[5], i[6], i[7], j[0], j[1], j[2], j[3]])
#             else:
#                 list_required_data.append(['', '', '', '', '', '', j[0], j[1], j[2], j[3]])
#         except:
#             print i
#             print j
#     count = count + 1
# pd_data = pd.DataFrame(list_required_data,
#                        columns=['frequency', 'bandwidth', 'fft_mode', 'modulation', 'code_rate', 'guard',
#                                 'mian_att', 'mian_delay', 'pre_delay', 'pre_att'])
# pd_data.to_csv("../../ekt_test_report/1.csv", index=None)


load_dict = read_json_file("../../ekt_json/dvbc_1_dynamic_range_awng_max_level.json")
list_data = load_dict.get("test_parame_result")
# print list_data
list_required_data = []
for i in list_data:
    count = 0
    for j in i[3]:
        if count == 0:
            list_required_data.append([i[0], i[1][1], i[2], j[0][0], j[1]])
        else:
            list_required_data.append(['', '', '', j[0][0], j[1]])
        count = count + 1
pd_data = pd.DataFrame(list_required_data, columns=['modulation', 'symbol_rate', 'CN', 'frequency', 'mosic_result'])
pd_data.to_csv("../../ekt_test_report/1.csv", index=None)
# print(os.listdir('E:/data'))
# a.to_csv('E:/data/m.csv', sep=';', index=False)
# print(os.listdir('E:/data'))
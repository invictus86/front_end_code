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

start_data = -60.12
end_data = -90.12

print round((start_data + end_data) / 2, 1)




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


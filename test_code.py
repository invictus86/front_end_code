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

# start_data = -60.12
# end_data = -90.12
#
# print round((start_data + end_data) / 2, 1)

# start_num = -76.6
# end_num = -76.7
# print start_num - end_num
# print 0.1
# print type(start_num-end_num)
# print type(0.1)
# if start_num-end_num == 0.1:
#     print 111
# else:
#     print 222
# assert start_num - end_num == 0.1

import ekt_net
import json
# net = ekt_net.EktNetClient('192.168.1.24', 9999)
# frequency = net.send_rec(json.dumps({"cmd": "get_frequency_data"}))
# symbol_rate = net.send_rec(json.dumps({"cmd": "get_symbol_rate_data"}))
# print frequency
# print symbol_rate
# def read_ekt_config_data(file_path):
#     with open(file_path, 'r') as f:
#         dict_data = json.load(f, "utf-8")
#         return dict_data
#
# dict_data = read_ekt_config_data("./ekt_config.json")
# DVBS_S2_FREQUENCY_LEVEL_OFFSET = dict_data.get("DVBS_S2_FREQUENCY_LEVEL_OFFSET")
#
# net = ekt_net.EktNetClient('192.168.1.24', 9999)
# net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": str(DVBS_S2_FREQUENCY_LEVEL_OFFSET[0][0])}))

import ekt_cfg
from ekt_stb_tester import stb_tester_detect_motion
for _ in range(3):
    stb_tester_detect_motion(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                           ["tests/front_end_test/testcases.py::test_continuous_button"],
                                           "auto_front_end_test", "DSD4614iALM")


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


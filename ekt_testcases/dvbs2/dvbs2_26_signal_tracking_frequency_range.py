#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import datetime
import os, sys

parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parentdir)
from ekt_lib import ekt_net, ekt_cfg
from ekt_lib.ekt_sfu import Ektsfu
from pathlib2 import Path
from ekt_lib.ekt_stb_tester import stb_tester_execute_testcase
from ekt_lib.threshold_algorithm_SFU import mosaic_algorithm
from ekt_lib.ekt_utils import write_test_result, read_ekt_config_data, find_level_offset_by_frequency, write_json_file, read_json_file, \
    dvbs2_26_signal_tracking_frequency_range_json_to_csv

MODULATION_8PSK = "S8"

LEVEL_OFFSET_950 = find_level_offset_by_frequency("DVBS_S2_FREQUENCY_LEVEL_OFFSET", 950)
LEVEL_50_950 = str("%.2f" % ((-50) - LEVEL_OFFSET_950))
LEVEL_OFFSET_1550 = find_level_offset_by_frequency("DVBS_S2_FREQUENCY_LEVEL_OFFSET", 1550)
LEVEL_50_1550 = str("%.2f" % ((-50) - LEVEL_OFFSET_1550))
LEVEL_OFFSET_2150 = find_level_offset_by_frequency("DVBS_S2_FREQUENCY_LEVEL_OFFSET", 2150)
LEVEL_50_2150 = str("%.2f" % ((-50) - LEVEL_OFFSET_2150))

SYMBOL_RATE_FREQUENCY_5M = ["5.000000e6", "05000",
                            [["950", "952", LEVEL_50_950, LEVEL_OFFSET_950],
                             ["1550", "1552", LEVEL_50_1550, LEVEL_OFFSET_1550],
                             ["2150", "2148", LEVEL_50_2150, LEVEL_OFFSET_2150]]]
SYMBOL_RATE_FREQUENCY_27_5M = ["27.500000e6", "27500",
                               [["950", "952", LEVEL_50_950, LEVEL_OFFSET_950],
                                ["1550", "1552", LEVEL_50_1550, LEVEL_OFFSET_1550],
                                ["2150", "2148", LEVEL_50_2150, LEVEL_OFFSET_2150]]]
SYMBOL_RATE_FREQUENCY_45M = ["45.000000e6", "45000",
                             [["950", "952", LEVEL_50_950, LEVEL_OFFSET_950],
                              ["1550", "1552", LEVEL_50_1550, LEVEL_OFFSET_1550],
                              ["2150", "2148", LEVEL_50_2150, LEVEL_OFFSET_2150]]]

dict_config_data = {
    "SYMBOL_RATE_FREQUENCY": [SYMBOL_RATE_FREQUENCY_5M, SYMBOL_RATE_FREQUENCY_27_5M, SYMBOL_RATE_FREQUENCY_45M]}

my_file = Path("../../ekt_json/dvbs2_26_signal_tracking_frequency_range.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    list_test_parame_result = []

    dict_data = read_ekt_config_data("../../ekt_lib/ekt_config.json")
    DVBS2_8PSK_CODE_RATE_CN = dict_data.get("DVBS2_8PSK_CODE_RATE_CN")

    for SYMBOL_RATE_FREQUENCY in dict_config_data.get("SYMBOL_RATE_FREQUENCY"):
        for FREQUENCY_OFFSET in SYMBOL_RATE_FREQUENCY[2]:
            list_test_result = []
            for code_rate_cn in DVBS2_8PSK_CODE_RATE_CN:
                list_test_result.append([code_rate_cn, None])
            list_test_parame_result.append([SYMBOL_RATE_FREQUENCY[0], SYMBOL_RATE_FREQUENCY[1], FREQUENCY_OFFSET, list_test_result])
    dict_test_parame_result["test_parame_result"] = list_test_parame_result

    write_json_file("../../ekt_json/dvbs2_26_signal_tracking_frequency_range.json", dict_test_parame_result)

if __name__ == '__main__':
    """
    测试流程:
    ①重置设备
    ②选择 TSPLAYER
    ③播放流文件
    ④设置code_rate,modulation,symbol_rate,frequency,input_signal_level
    ⑤机顶盒应用中进行锁台并确认锁台成功  （针对stb-tester发送post请求运行testcase,由于每款机顶盒界面、锁台操作不同,
    是否需要对testcase与PC端做参数交互？）
    ⑤依次修改可变参数,判断机顶盒画面是否含有马赛克并记录结果
    """
    load_dict = read_json_file("../../ekt_json/dvbs2_26_signal_tracking_frequency_range.json")
    sfu_ip = "192.168.1.50"
    specan = Ektsfu(sfu_ip)
    specan.preset_instrument()
    specan = Ektsfu(sfu_ip)
    specan.set_modulation_modulation_source("DTV")
    specan = Ektsfu(sfu_ip)
    specan.set_modulation_modulation_standard_dvt("DVS2")
    specan = Ektsfu(sfu_ip)
    specan.set_player_timing_openfile(r"E:\333\DIVER.GTS")
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_input_source_dvbs2("TSPLayer")
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_coding_constellation_dvbs2(MODULATION_8PSK)
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_rf("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_noise_noise_noise("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_modulator("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_baseband("OFF")

    for LOCK_PARAMETER in load_dict.get("test_parame_result"):
        loop_lock_mark = False
        for check_list in LOCK_PARAMETER[3]:
            if check_list[1] == None:
                loop_lock_mark = True
                break
        if loop_lock_mark == True:
            pass
        else:
            continue
        FREQUENCY_OFFSET = LOCK_PARAMETER[2]
        SYMBOL_RATE_FREQUENCY = [LOCK_PARAMETER[0], LOCK_PARAMETER[1]]

        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_symbolrate_dvbs2(SYMBOL_RATE_FREQUENCY[0])
        specan = Ektsfu(sfu_ip)
        specan.set_frequency_frequency_frequency(FREQUENCY_OFFSET[0] + "MHz")
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_offset(str(FREQUENCY_OFFSET[3]))
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_level("dBm", FREQUENCY_OFFSET[2])

        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": FREQUENCY_OFFSET[0]}))
        time.sleep(1)
        del net
        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(
            json.dumps({"cmd": "set_symbol_rate_data", "symbol_rate": str(SYMBOL_RATE_FREQUENCY[1])}))
        time.sleep(1)
        del net

        """
        触发stb-tester进行频率和符号率设置
        """
        stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                    ["tests/front_end_test/testcases.py::test_continuous_button"],
                                    "auto_front_end_test", "DSD4614iALM")
        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
        if lock_state == "1":
            pass
        elif lock_state == "0":
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              (
                                      "dvbs2_signal_tracking_frequency_range: current_time:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, {}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          FREQUENCY_OFFSET[1], SYMBOL_RATE_FREQUENCY[1], FREQUENCY_OFFSET[2],
                                          "Lock fail") + "\n"))
            continue
        else:
            write_test_result("../../ekt_log/test_result_sfu.txt", ("Lock state err" + "\n"))
            continue
        for PARAMETER in LOCK_PARAMETER[3]:
            if PARAMETER[1] == None:
                pass
            else:
                continue
            code_rate_cn = PARAMETER[0]

            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_coding_coderate_dvbs2(code_rate_cn[0])

            mosaic_algorithm(sfu_ip, FREQUENCY_OFFSET[2], "-50")
            specan = Ektsfu(sfu_ip)
            specan.set_frequency_frequency_frequency(FREQUENCY_OFFSET[1] + "MHz")
            time.sleep(3)
            start_data_result, mosaic_result = mosaic_algorithm(sfu_ip, FREQUENCY_OFFSET[2], "-50")
            print (
                "dvbs2_signal_tracking_frequency_range: current_time:{}, coderate:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, Mosaic results:{}".format(
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn[0],
                    FREQUENCY_OFFSET[1], SYMBOL_RATE_FREQUENCY[1], FREQUENCY_OFFSET[2],
                    start_data_result.get("detect_mosic_result")))
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              "dvbs2_signal_tracking_frequency_range: current_time:{}, coderate:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, Mosaic results:{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn[0],
                                  FREQUENCY_OFFSET[1], SYMBOL_RATE_FREQUENCY[1], FREQUENCY_OFFSET[2],
                                  start_data_result.get("detect_mosic_result")) + "\n")

            PARAMETER[1] = mosaic_result
            write_json_file("../../ekt_json/dvbs2_26_signal_tracking_frequency_range.json", load_dict)
            dvbs2_26_signal_tracking_frequency_range_json_to_csv("../../ekt_json/dvbs2_26_signal_tracking_frequency_range.json",
                                                                    "../../ekt_test_report/dvbs2_26_signal_tracking_frequency_range.csv")

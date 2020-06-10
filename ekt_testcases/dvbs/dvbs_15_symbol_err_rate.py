#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import datetime
import os, sys

parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parentdir)
from ekt_lib import ekt_net, ekt_cfg
from ekt_lib.ekt_sfe import Ektsfe
from pathlib2 import Path
from ekt_lib.ekt_stb_tester import stb_tester_execute_testcase
from ekt_lib.threshold_algorithm_SFE import mosaic_algorithm
from ekt_lib.ekt_utils import write_test_result, read_ekt_config_data, find_level_offset_by_frequency, write_json_file, read_json_file, \
    dvbs_symbol_err_rate_json_to_csv

CODE_RATE_LIST = ["R1_2", "R2_3", "R3_4", "R5_6", "R7_8"]

MODULATION_QPSK = "S4"
FREQUENCY_1550 = "1550"
LEVEL_OFFSET = find_level_offset_by_frequency("DVBS_S2_FREQUENCY_LEVEL_OFFSET", int(FREQUENCY_1550))
LEVEL_50 = str("%.2f" % ((-50) - LEVEL_OFFSET))

SYMBOL_RATE_5M = ["5.000000e6", "05002"]
SYMBOL_RATE_5M_ = ["5.000000e6", "04998"]
SYMBOL_RATE_27_5M = ["27.500000e6", "27503"]
SYMBOL_RATE_27_5M_ = ["27.500000e6", "27497"]
SYMBOL_RATE_45M = ["45.000000e6", "44995"]
SYMBOL_RATE_45M_ = ["45.000000e6", "45005"]

dict_config_data = {
    "SYMBOL_RATE": [SYMBOL_RATE_5M, SYMBOL_RATE_5M_, SYMBOL_RATE_27_5M, SYMBOL_RATE_27_5M_, SYMBOL_RATE_45M,
                    SYMBOL_RATE_45M_]}

my_file = Path("../../ekt_json/dvbs_symbol_err_rate.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    list_test_parame_result = []

    # dict_data = read_ekt_config_data("../../ekt_lib/ekt_config.json")
    # DVBS_S2_FREQUENCY_LEVEL_OFFSET = dict_data.get("DVBS_S2_FREQUENCY_LEVEL_OFFSET")
    # DVBS_QPSK_CODE_RATE_CN = dict_data.get("DVBS_QPSK_CODE_RATE_CN")

    for SYMBOL_RATE in dict_config_data.get("SYMBOL_RATE"):
        list_test_result = []
        for code_rate_cn in CODE_RATE_LIST:
            list_test_result.append([code_rate_cn, None])

        list_test_parame_result.append([SYMBOL_RATE, list_test_result])
    dict_test_parame_result["test_parame_result"] = list_test_parame_result

    write_json_file("../../ekt_json/dvbs_symbol_err_rate.json", dict_test_parame_result)

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
    load_dict = read_json_file("../../ekt_json/dvbs_symbol_err_rate.json")
    sfe_ip = "192.168.1.47"
    specan = Ektsfe(sfe_ip)
    specan.clean_reset()
    specan = Ektsfe(sfe_ip)
    specan.preset_instrument()
    specan = Ektsfe(sfe_ip)
    specan.set_digitaltv_input_source("TSPL")
    specan = Ektsfe(sfe_ip)
    specan.set_digitaltv_input_load(r"D:\TSGEN\SDTV\DVB_25Hz\720_576i\LIVE\DIVER.GTS")

    # dict_data = read_ekt_config_data("../../ekt_lib/ekt_config.json")

    specan = Ektsfe(sfe_ip)
    specan.set_frequency_frequency_frequency(FREQUENCY_1550 + "MHz")
    specan = Ektsfe(sfe_ip)
    specan.set_level_level_level(LEVEL_50 + " dBm")
    # for SYMBOL_RATE in dict_config_data.get("SYMBOL_RATE"):
    for PARAMETER in load_dict.get("test_parame_result"):
        loop_lock_mark = False
        for check_list in PARAMETER[1]:
            if check_list[1] == None:
                loop_lock_mark = True
                break
        if loop_lock_mark == True:
            pass
        else:
            continue

        SYMBOL_RATE = PARAMETER[0]

        specan = Ektsfe(sfe_ip)
        specan.set_digitaltv_coding_symbolrate(SYMBOL_RATE[0])

        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": FREQUENCY_1550}))
        time.sleep(1)
        del net
        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(json.dumps({"cmd": "set_symbol_rate_data", "symbol_rate": str(SYMBOL_RATE[1])}))
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
            write_test_result("../../ekt_log/test_result_sfe.txt",
                              (
                                      "dvbs_symbol_err_rate: current_time:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, {}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          FREQUENCY_1550, str(SYMBOL_RATE[1]), LEVEL_50, "Lock fail") + "\n"))
            continue
        else:
            write_test_result("../../ekt_log/test_result_sfe.txt", ("Lock state err" + "\n"))
            continue
        for code_rate_cn in PARAMETER[1]:
            if code_rate_cn[1] == None:
                pass
            else:
                continue

            specan = Ektsfe(sfe_ip)
            specan.set_digitaltv_coding_coderate(code_rate_cn[0])

            start_data_result, mosaic_result = mosaic_algorithm(sfe_ip, LEVEL_50, "-50")
            print (
                "dvbs_symbol_err_rate: current_time:{}, coderate:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, Mosaic results:{}".format(
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn[0],
                    FREQUENCY_1550, str(SYMBOL_RATE[1]), LEVEL_50, start_data_result.get("detect_mosic_result")))
            write_test_result("../../ekt_log/test_result_sfe.txt",
                              "dvbs_symbol_err_rate: current_time:{}, coderate:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, Mosaic results:{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn[0],
                                  FREQUENCY_1550, str(SYMBOL_RATE[1]), LEVEL_50,
                                  start_data_result.get("detect_mosic_result")) + "\n")

            code_rate_cn[1] = mosaic_result
            write_json_file("../../ekt_json/dvbs_symbol_err_rate.json", load_dict)
            dvbs_symbol_err_rate_json_to_csv("../../ekt_json/dvbs_symbol_err_rate.json",
                                             "../../ekt_test_report/dvbs_symbol_err_rate.csv")

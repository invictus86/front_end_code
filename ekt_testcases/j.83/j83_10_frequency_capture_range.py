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
from ekt_lib.ekt_utils import write_test_result, write_json_file, read_json_file, j83_10_frequency_capture_range_json_to_csv

MODULATION_64QAM = "J64"
MODULATION_256QAM = "J256"

SYMBOL_RATE_5361 = ["5.361e6", "5361"]

REQUENCY_LIST = [
    [60, 60.2],
    [201, 201.2],
    [315, 315.2],
    [405, 405.2],
    [501, 501.2],
    [603, 603.2],
    [705, 705.2],
    [801, 801.2],
    [858, 858.2],
    [60, 59.8],
    [201, 200.8],
    [315, 314.8],
    [405, 404.8],
    [501, 500.8],
    [603, 602.8],
    [705, 704.8],
    [801, 800.8],
    [858, 857.8],
]

SYMBOL_RATE_LIST = [SYMBOL_RATE_5361]
MODULATION_LIST = [MODULATION_64QAM, MODULATION_256QAM]

my_file = Path("../../ekt_json/j83_10_frequency_capture_range.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    list_test_parame_result = []

    for SYMBOL_RATE in SYMBOL_RATE_LIST:
        for REQUENCY in REQUENCY_LIST:
            list_test_result = []
            for MODULATION in MODULATION_LIST:
                list_test_result.append([MODULATION, None])
            list_test_parame_result.append([SYMBOL_RATE, REQUENCY, list_test_result])
    dict_test_parame_result["test_parame_result"] = list_test_parame_result

    write_json_file("../../ekt_json/j83_10_frequency_capture_range.json", dict_test_parame_result)

if __name__ == '__main__':
    """
    测试流程:
    ①重置设备
    ②选择 TSPLAYER
    ③播放流文件
    ④设置modulation,symbol_rate, CN, frequency,input_signal_level
    ⑤机顶盒应用中进行锁台并确认锁台成功  （针对stb-tester发送post请求运行testcase）
    ⑤依次修改可变参数,判断机顶盒画面是否含有马赛克并记录结果
    """
    load_dict = read_json_file("../../ekt_json/j83_10_frequency_capture_range.json")
    sfu_ip = ekt_cfg.SFU_IP
    specan = Ektsfu(sfu_ip)
    specan.preset_instrument()
    specan = Ektsfu(sfu_ip)
    specan.set_modulation_modulation_source("DTV")
    specan = Ektsfu(sfu_ip)
    specan.set_modulation_modulation_standard_dvt("J83B")
    specan = Ektsfu(sfu_ip)
    specan.set_player_timing_openfile(r"E:\333\DIVER.GTS")
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_input_source_j83b("TSPLayer")
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_rf("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_noise_noise_noise("OFF")
    # specan = Ektsfu(sfu_ip)
    # specan.set_noise_noise_awgn("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_modulator("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_baseband("OFF")

    for LOCK_PARAMETER in load_dict.get("test_parame_result"):
        loop_lock_mark = False
        for check_list in LOCK_PARAMETER[2]:
            if check_list[1] == None:
                loop_lock_mark = True
                break
        if loop_lock_mark == True:
            pass
        else:
            continue

        SYMBOL_RATE = LOCK_PARAMETER[0]
        FREQUENCY_LEVEL_OFFSET = LOCK_PARAMETER[1]

        # specan = Ektsfu(sfu_ip)
        # specan.set_digitaltv_coding_symbolrate_dvbc(SYMBOL_RATE[0])
        specan = Ektsfu(sfu_ip)
        specan.set_frequency_frequency_frequency(str(FREQUENCY_LEVEL_OFFSET[0]) + "MHz")
        # specan = Ektsfu(sfu_ip)
        # specan.set_level_level_offset(str(FREQUENCY_LEVEL_OFFSET[1]))
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_level("dBm", "-50")

        for PARAMETER in LOCK_PARAMETER[2]:
            if PARAMETER[1] == None:
                pass
            else:
                continue

            MODULATION = PARAMETER[0]
            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_coding_constellation_dvbc(MODULATION)
            time.sleep(3)
            net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
            net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": str(FREQUENCY_LEVEL_OFFSET[0])}))
            time.sleep(1)
            del net
            net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
            net.send_data(json.dumps({"cmd": "set_symbol_rate_data", "symbol_rate": str(SYMBOL_RATE[1])}))
            time.sleep(1)
            del net
            net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
            net.send_data(json.dumps({"cmd": "set_modulation_data", "modulation": str(MODULATION)}))
            time.sleep(1)
            del net

            """
            触发stb-tester进行频率和符号率设置
            """
            stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                        ekt_cfg.DVB_J83_LOCK_FUNCTION, ekt_cfg.DVB_J83_CATEGORY, ekt_cfg.DVB_J83_REMOTE)

            net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)

            lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
            if lock_state == "1":
                pass
            elif lock_state == "0":
                write_test_result("../../ekt_log/test_result_sfu.txt",
                                  (
                                          "j83_10_frequency_capture_range: current_time:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, {}".format(
                                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                              str(FREQUENCY_LEVEL_OFFSET[1]), str(SYMBOL_RATE[1]), str(-50),
                                              "Lock fail") + "\n"))
                continue
            elif lock_state == "2":
                write_test_result("../../ekt_log/test_result_sfu.txt",
                                  (
                                          "j83_10_frequency_capture_range: current_time:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, {}".format(
                                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                              str(FREQUENCY_LEVEL_OFFSET[1]), str(SYMBOL_RATE[1]), str(-50),
                                              "Frequency points are not supported") + "\n"))
                continue
            else:
                write_test_result("../../ekt_log/test_result_sfu.txt", ("Lock state err" + "\n"))
                continue

            _, _ = mosaic_algorithm(sfu_ip, -50, -50)
            specan = Ektsfu(sfu_ip)
            specan.set_frequency_frequency_frequency(str(FREQUENCY_LEVEL_OFFSET[1]) + "MHz")
            time.sleep(5)
            start_data_result, mosaic_result = mosaic_algorithm(sfu_ip, -50, -50)

            print (
                "j83_10_frequency_capture_range: current_time:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, Mosaic result:{}".format(
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]), str(-50),
                    start_data_result.get("detect_mosic_result")))
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              "j83_10_frequency_capture_range: current_time:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, Mosaic result:{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                  str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]), str(-50),
                                  start_data_result.get("detect_mosic_result")) + "\n")

            PARAMETER[1] = mosaic_result
            write_json_file("../../ekt_json/j83_10_frequency_capture_range.json", load_dict)
            j83_10_frequency_capture_range_json_to_csv("../../ekt_json/j83_10_frequency_capture_range.json",
                                                       "../../ekt_test_report/j83_10_frequency_capture_range.csv")

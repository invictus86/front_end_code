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
from ekt_lib.ekt_utils import write_test_result, write_json_file, read_json_file, find_level_offset_by_frequency, \
    j83_2_channel_bandwidth_json_to_csv

FREQUENCY_666 = 666
LEVEL_OFFSET_666 = find_level_offset_by_frequency("ANNEXB_FREQUENCY_LEVEL_OFFSET", 666)
LEVEL_50_666 = str("%.2f" % (-50 - LEVEL_OFFSET_666))

MODULATION_64QAM = "J64"
MODULATION_256QAM = "J256"

SYMBOL_RATE_5361 = ["5.361e6", "5361"]

PARAMETER_LIST = [
    [FREQUENCY_666, LEVEL_OFFSET_666, LEVEL_50_666, MODULATION_256QAM, SYMBOL_RATE_5361, None]
]

my_file = Path("../../ekt_json/j83_2_channel_bandwidth.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    dict_test_parame_result["test_parame_result"] = PARAMETER_LIST
    write_json_file("../../ekt_json/j83_2_channel_bandwidth.json", dict_test_parame_result)

if __name__ == '__main__':
    """
    测试流程：
    ①重置设备
    ②选择 TSPLAYER
    ③播放流文件
    ④设置code_rate，modulation，symbol_rate，frequency，input_signal_level
    ⑤机顶盒应用中进行锁台并确认锁台成功  （针对stb-tester发送post请求运行testcase，由于每款机顶盒界面、锁台操作不同，
    是否需要对testcase与PC端做参数交互？）
    ⑤依次修改可变参数，判断机顶盒画面是否含有马赛克并记录结果
    """
    load_dict = read_json_file("../../ekt_json/j83_2_channel_bandwidth.json")
    sfu_ip = "192.168.1.50"
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
    specan.set_noise_noise_noise("ADD")
    specan = Ektsfu(sfu_ip)
    specan.set_noise_noise_awgn("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_noise_settings_bandwith("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_modulator("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_baseband("OFF")

    for LOCK_PARAMETER in load_dict.get("test_parame_result"):

        MODULATION = LOCK_PARAMETER[3]
        SYMBOL_RATE = LOCK_PARAMETER[4]
        # CN = LOCK_PARAMETER[2]

        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_constellation_j83b(MODULATION)
        # specan = Ektsfu(sfu_ip)
        # specan.set_digitaltv_coding_symbolrate_j83b(SYMBOL_RATE[0])
        specan = Ektsfu(sfu_ip)
        specan.set_noise_awgn_cn(str("35"))

        # for PARAMETER in LOCK_PARAMETER[3]:

        FREQUENCY_LEVEL_OFFSET = [LOCK_PARAMETER[0], LOCK_PARAMETER[1]]

        specan = Ektsfu(sfu_ip)
        specan.set_frequency_frequency_frequency(str(FREQUENCY_LEVEL_OFFSET[0]) + "MHz")
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_offset(str(FREQUENCY_LEVEL_OFFSET[1]))
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_level("dBm", str("%.2f" % ((-50) - FREQUENCY_LEVEL_OFFSET[1])))

        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": str(FREQUENCY_LEVEL_OFFSET[0])}))
        time.sleep(1)
        del net
        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(json.dumps({"cmd": "set_symbol_rate_data", "symbol_rate": str(SYMBOL_RATE[1])}))
        time.sleep(1)
        del net
        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(json.dumps({"cmd": "set_modulation_data", "modulation": str(MODULATION)}))
        time.sleep(1)
        del net

        """
        触发stb-tester进行频率和符号率设置
        """
        try:
            stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                        ["tests/front_end_test/testcases.py::test_continuous_button_7514i"], "auto_front_end_test",
                                        "dcn7514i")
        except:
            time.sleep(60)
            stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                        ["tests/front_end_test/testcases.py::test_continuous_button_7514i"], "auto_front_end_test",
                                        "dcn7514i")
        net = ekt_net.EktNetClient('192.168.1.24', 9999)

        lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
        if lock_state == "1":
            pass
        elif lock_state == "0":
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              (
                                      "j83_2_channel_bandwidth: current_time:{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, {}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                                          str("%.2f" % ((-50) - FREQUENCY_LEVEL_OFFSET[1])),
                                          "锁台失败") + "\n"))
            continue
        elif lock_state == "2":
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              (
                                      "j83_2_channel_bandwidth: current_time:{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, {}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                                          str("%.2f" % ((-50) - FREQUENCY_LEVEL_OFFSET[1])),
                                          "频点不支持") + "\n"))
            LOCK_PARAMETER[5] = "Frequency points are not supported"
            write_json_file("../../ekt_json/j83_2_channel_bandwidth.json", load_dict)
            j83_2_channel_bandwidth_json_to_csv("../../ekt_json/j83_2_channel_bandwidth.json",
                                                "../../ekt_test_report/j83_2_channel_bandwidth.csv")
            continue
        else:
            write_test_result("../../ekt_log/test_result_sfu.txt", ("出错了" + "\n"))
            continue

        start_data_result, mosaic_result = mosaic_algorithm(sfu_ip, str("%.2f" % ((-50) - FREQUENCY_LEVEL_OFFSET[1])),
                                                            str("%.2f" % ((-50) - FREQUENCY_LEVEL_OFFSET[1])))
        print (
            "j83_2_channel_bandwidth: current_time:{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, 马赛克检测结果：{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                str("%.2f" % ((-50) - FREQUENCY_LEVEL_OFFSET[1])),
                start_data_result.get("detect_mosic_result")))
        write_test_result("../../ekt_log/test_result_sfu.txt",
                          "j83_2_channel_bandwidth: current_time:{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, 马赛克检测结果：{}".format(
                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                              str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                              str("%.2f" % ((-50) - FREQUENCY_LEVEL_OFFSET[1])),
                              start_data_result.get("detect_mosic_result")) + "\n")

        LOCK_PARAMETER[5] = mosaic_result
        write_json_file("../../ekt_json/j83_2_channel_bandwidth.json", load_dict)
        j83_2_channel_bandwidth_json_to_csv("../../ekt_json/j83_2_channel_bandwidth.json",
                                            "../../ekt_test_report/j83_2_channel_bandwidth.csv")

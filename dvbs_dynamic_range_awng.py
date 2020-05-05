#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ekt_sfe
import time
import json
import ekt_net
from ekt_stb_tester import stb_tester_detect_motion
from threshold_algorithm_SFE import iterate_to_find_threshold
import ekt_cfg
import datetime

CODE_RATE_1_2 = "R1_2"
CODE_RATE_2_3 = "R2_3"
CODE_RATE_3_4 = "R3_4"
CODE_RATE_5_6 = "R5_6"
CODE_RATE_7_8 = "R7_8"

SYMBOL_RATE_5M = "5.000000e6"
SYMBOL_RATE_10M = "10.000000e6"
SYMBOL_RATE_45M = "45.000000e6"
SYMBOL_RATE_27_5M = "27.500000e6"


SYMBOL_TATE_LIST = [str(i) + ".000000e6" for i in range(5, 46)]
FREQUENCY_LIST = [str(i) + " MHz" for i in range(950, 2150, 20)]
FREQUENCY_LIST.append("2147 MHz")


def set_dvbs_variable_parameter(specan, code_rate, modulation, symbol_rate, frequency, input_signal_level):
    specan.set_digitaltv_coding_constellation(modulation)
    specan.set_digitaltv_coding_coderate(code_rate)
    specan.set_digitaltv_coding_symbolrate(symbol_rate)
    specan.set_frequency_frequency_frequency(frequency)
    specan.set_level_level_level(input_signal_level)


def write_test_result(file_path, content):
    with open(file_path, "a") as f:
        f.write(content)


def read_ekt_config_data(file_path):
    with open(file_path, 'r') as f:
        dict_data = json.load(f, "utf-8")
        return dict_data


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
    sfe_ip = "192.168.1.47"
    specan = ekt_sfe.Ektsfe(sfe_ip)
    specan.preset_instrument()
    specan = ekt_sfe.Ektsfe(sfe_ip)
    specan.set_digitaltv_input_source("TSPL")
    specan = ekt_sfe.Ektsfe(sfe_ip)
    specan.set_digitaltv_input_load(r"D:\TSGEN\SDTV\DVB_25Hz\720_576i\LIVE\DIVER.GTS")

    dict_data = read_ekt_config_data("./ekt_config.json")
    DVBS_S2_FREQUENCY_LEVEL_OFFSET = dict_data.get("DVBS_S2_FREQUENCY_LEVEL_OFFSET")
    # DVBS2_QPSK_CODE_RATE_CN = dict_data.get("DVBS2_QPSK_CODE_RATE_CN")
    # DVBS2_8PSK_CODE_RATE_CN = dict_data.get("DVBS2_8PSK_CODE_RATE_CN")

    for FREQUENCY_LEVEL_OFFSET in DVBS_S2_FREQUENCY_LEVEL_OFFSET:
        specan = ekt_sfe.Ektsfe(sfe_ip)
        specan.set_frequency_frequency_frequency(str(FREQUENCY_LEVEL_OFFSET[0]) + "MHz")
        specan = ekt_sfe.Ektsfe(sfe_ip)
        specan.set_level_level_level("-50 dBm")
        specan = ekt_sfe.Ektsfe(sfe_ip)
        specan.set_digitaltv_coding_symbolrate("45.000000e6")

        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        # print str(FREQUENCY_LEVEL_OFFSET[0])
        # print type(str(FREQUENCY_LEVEL_OFFSET[0]))
        net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": str(FREQUENCY_LEVEL_OFFSET[0])}))
        time.sleep(1)
        del net
        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(json.dumps({"cmd": "set_symbol_rate_data", "symbol_rate": str(45000)}))
        time.sleep(1)
        del net

        """
        触发stb-tester进行频率和符号率设置
        """
        stb_tester_detect_motion(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                 ["tests/front_end_test/testcases.py::test_continuous_button"],
                                 "auto_front_end_test", "DSD4614iALM")
        try:
            res = iterate_to_find_threshold("192.168.1.47", -60, -80)
            print "current_time:{}, frequency：{}，symbol_rate：{}，{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(FREQUENCY_LEVEL_OFFSET[0]), str(45000), res)
            write_test_result("./test_result_sfe.txt",
                              "current_time:{}, frequency：{}，symbol_rate：{}，{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(FREQUENCY_LEVEL_OFFSET[0]),
                                  str(45000), res) + "\n")
        except:
            res = iterate_to_find_threshold("192.168.1.47", -60, -80)
            print "current_time:{}, frequency：{}，symbol_rate：{}，{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(FREQUENCY_LEVEL_OFFSET[0]), str(45000), res)
            write_test_result("./test_result_sfe.txt",
                              "current_time:{}, frequency：{}，symbol_rate：{}，{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), str(FREQUENCY_LEVEL_OFFSET[0]),
                                  str(45000), res) + "\n")

        """
        进行机顶盒的频率修改或其他参数的修改
        读取误码率或者判断机顶盒是否含有马赛克
        """

# if __name__ == '__main__':
#     sfe_ip = "192.168.1.47"
#     dict_data = read_ekt_config_data("./ekt_config.json")
#     DVBS_S2_FREQUENCY_LEVEL_OFFSET = dict_data.get("DVBS_S2_FREQUENCY_LEVEL_OFFSET")
#     print DVBS_S2_FREQUENCY_LEVEL_OFFSET
#     for FREQUENCY_LEVEL_OFFSET in DVBS_S2_FREQUENCY_LEVEL_OFFSET:
#         specan = ekt_sfe.Ektsfe(sfe_ip)
#         specan.set_frequency_frequency_frequency(str(FREQUENCY_LEVEL_OFFSET[0]) + "MHz")
#         # del specan
#         specan = ekt_sfe.Ektsfe(sfe_ip)
#         specan.set_level_level_level("-50 dBm")
#         # del specan
#         specan = ekt_sfe.Ektsfe(sfe_ip)
#         specan.set_digitaltv_coding_symbolrate("45.000000e6")
#         # del specan
#
#
#         net = ekt_net.EktNetClient('192.168.1.24', 9999)
#         net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": str(FREQUENCY_LEVEL_OFFSET[0])}))
#         time.sleep(1)
#         net.send_data(json.dumps({"cmd": "set_symbol_rate_data", "symbol_rate": str(45000)}))
#         time.sleep(1)
#         del net
#
#         """
#         触发stb-tester进行频率和符号率设置
#         """
#
#         stb_tester_detect_motion(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
#                                        ["tests/front_end_test/testcases.py::test_continuous_button"],
#                                        "auto_front_end_test", "DSD4614iALM")
#         res = iterate_to_find_threshold("192.168.1.47", -60, -80)
#         print res

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ekt_sfe
import time
import json
import ekt_net
from ekt_stb_tester import stb_tester_detect_motion
from threshold_algorithm_SFE import iterate_to_find_threshold, mosaic_algorithm

import ekt_cfg
import datetime

CODE_RATE_3_4 = "R3_4"
MODULATION_QPSK = "S4"
FREQUENCY_1550 = "1550 MHz"
LEVEL_70 = "-70 dBm"

SYMBOL_RATE_5M = ["5.000000e6", "05000"]
SYMBOL_RATE_10M = ["10.000000e6", "10000"]
SYMBOL_RATE_27_5M = ["27.500000e6", "27500"]
SYMBOL_RATE_45M = ["45.000000e6", "45000"]

SYMBOL_TATE_LIST = []


def generate_symbol_rate_list():
    for i in range(5, 46):
        if i < 10:
            SYMBOL_TATE_LIST.append([str(i) + ".000000e6", "0{}000".format(i)])
        else:
            SYMBOL_TATE_LIST.append([str(i) + ".000000e6", "{}000".format(i)])


generate_symbol_rate_list()


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
    specan.clean_reset()
    specan = ekt_sfe.Ektsfe(sfe_ip)
    specan.preset_instrument()
    # specan.timeout = 2000
    specan = ekt_sfe.Ektsfe(sfe_ip)
    specan.set_digitaltv_input_source("TSPL")
    specan = ekt_sfe.Ektsfe(sfe_ip)
    specan.set_digitaltv_input_load(r"D:\TSGEN\SDTV\DVB_25Hz\720_576i\LIVE\DIVER.GTS")

    dict_data = read_ekt_config_data("./ekt_config.json")
    # DVBS_S2_FREQUENCY_LEVEL_OFFSET = dict_data.get("DVBS_S2_FREQUENCY_LEVEL_OFFSET")
    # DVBS_QPSK_CODE_RATE_CN = dict_data.get("DVBS_QPSK_CODE_RATE_CN")

    # DVBS2_8PSK_CODE_RATE_CN = dict_data.get("DVBS2_8PSK_CODE_RATE_CN")

    # for code_rate_cn in DVBS_QPSK_CODE_RATE_CN:
    #     del specan
    specan = ekt_sfe.Ektsfe(sfe_ip)
    specan.set_digitaltv_coding_constellation("S4")
    specan = ekt_sfe.Ektsfe(sfe_ip)
    specan.set_digitaltv_coding_coderate(CODE_RATE_3_4)
    time.sleep(1)
    specan = ekt_sfe.Ektsfe(sfe_ip)
    specan.set_frequency_frequency_frequency(FREQUENCY_1550)
    specan = ekt_sfe.Ektsfe(sfe_ip)
    specan.set_level_level_level(LEVEL_70)
    for SYMBOL_RATE in SYMBOL_TATE_LIST:
        specan = ekt_sfe.Ektsfe(sfe_ip)
        specan.set_digitaltv_coding_symbolrate(SYMBOL_RATE[0])

        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        # print str(FREQUENCY_LEVEL_OFFSET[0])
        # print type(str(FREQUENCY_LEVEL_OFFSET[0]))
        net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": str(1550)}))
        time.sleep(1)
        del net
        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(json.dumps({"cmd": "set_symbol_rate_data", "symbol_rate": str(SYMBOL_RATE[1])}))
        time.sleep(1)
        del net

        """
        触发stb-tester进行频率和符号率设置
        """
        stb_tester_detect_motion(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                 ["tests/front_end_test/testcases.py::test_continuous_button"],
                                 "auto_front_end_test", "DSD4614iALM")
        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
        if lock_state == "1":
            pass
        elif lock_state == "0":
            write_test_result("./test_result_sfe.txt",
                              ("current_time:{}, coderate：{}, frequency：{}，symbol_rate：{}，{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), CODE_RATE_3_4,
                                  str(FREQUENCY_1550), str(SYMBOL_RATE[1]), "锁台失败") + "\n"))
            continue
        else:
            write_test_result("./test_result_sfe.txt", ("出错了" + "\n"))
            continue
        try:
            start_data_result = mosaic_algorithm(sfe_ip, LEVEL_70, "-50 dBm")
            # res = iterate_to_find_threshold(sfe_ip, -50, -100)
            print "current_time:{}, coderate：{}, frequency：{}，symbol_rate：{}，马赛克检测结果：{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), CODE_RATE_3_4,
                str(FREQUENCY_1550), str(SYMBOL_RATE[1]), start_data_result.get("detect_mosic_result"))
            write_test_result("./test_result_sfe.txt",
                              "current_time:{}, coderate：{}, frequency：{}，symbol_rate：{}，马赛克检测结果：{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), CODE_RATE_3_4,
                str(FREQUENCY_1550), str(SYMBOL_RATE[1]), start_data_result.get("detect_mosic_result")) + "\n")
        except:
            res = iterate_to_find_threshold(sfe_ip, -50, -100)
            print "current_time:{}, coderate：{}, frequency：{}，symbol_rate：{}，马赛克检测结果：{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), CODE_RATE_3_4,
                str(FREQUENCY_1550), str(SYMBOL_RATE[1]), start_data_result.get("detect_mosic_result"))
            write_test_result("./test_result_sfe.txt",
                              "current_time:{}, coderate：{}, frequency：{}，symbol_rate：{}，马赛克检测结果：{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), CODE_RATE_3_4,
                str(FREQUENCY_1550), str(SYMBOL_RATE[1]), start_data_result.get("detect_mosic_result")) + "\n")

        """
        进行机顶盒的频率修改或其他参数的修改
        读取误码率或者判断机顶盒是否含有马赛克
        """

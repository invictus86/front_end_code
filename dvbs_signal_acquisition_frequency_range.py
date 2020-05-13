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

CODE_RATE_LIST = ["R1_2", "R2_3", "R3_4", "R5_6", "R7_8"]

MODULATION_QPSK = "S4"
LEVEL_50 = "-50 dBm"

SYMBOL_RATE_FREQUENCY_5M = ["5.000000e6", "05000", [["950", "951"], ["1550", "1551"], ["2150", "2149"]]]
SYMBOL_RATE_FREQUENCY_27_5M = ["27.500000e6", "27500", [["950", "952.75"], ["1550", "1552.75"], ["2150", "2147.25"]]]
SYMBOL_RATE_FREQUENCY_45M = ["45.000000e6", "45000",  [["950", "954.5"], ["1550", "1554.5"], ["2150", "2145.5"]]]

dict_config_data = {
    "SYMBOL_RATE_FREQUENCY": [SYMBOL_RATE_FREQUENCY_5M, SYMBOL_RATE_FREQUENCY_27_5M, SYMBOL_RATE_FREQUENCY_45M]}


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
    specan = ekt_sfe.Ektsfe(sfe_ip)
    specan.set_digitaltv_input_source("TSPL")
    specan = ekt_sfe.Ektsfe(sfe_ip)
    specan.set_digitaltv_input_load(r"D:\TSGEN\SDTV\DVB_25Hz\720_576i\LIVE\DIVER.GTS")
    specan = ekt_sfe.Ektsfe(sfe_ip)
    specan.set_level_level_level(LEVEL_50)

    dict_data = read_ekt_config_data("./ekt_config.json")
    # DVBS_S2_FREQUENCY_LEVEL_OFFSET = dict_data.get("DVBS_S2_FREQUENCY_LEVEL_OFFSET")
    # DVBS_QPSK_CODE_RATE_CN = dict_data.get("DVBS_QPSK_CODE_RATE_CN")
    # DVBS2_8PSK_CODE_RATE_CN = dict_data.get("DVBS2_8PSK_CODE_RATE_CN")

    for code_rate_cn in CODE_RATE_LIST:
        del specan
        specan = ekt_sfe.Ektsfe(sfe_ip)
        specan.set_digitaltv_coding_coderate(code_rate_cn)
        time.sleep(1)
        for SYMBOL_RATE_FREQUENCY in dict_config_data.get("SYMBOL_RATE_FREQUENCY"):
            del specan
            specan = ekt_sfe.Ektsfe(sfe_ip)
            specan.set_digitaltv_coding_symbolrate(SYMBOL_RATE_FREQUENCY[0])
            for FREQUENCY_OFFSET in SYMBOL_RATE_FREQUENCY[2]:
                del specan
                specan = ekt_sfe.Ektsfe(sfe_ip)
                specan.set_frequency_frequency_frequency(FREQUENCY_OFFSET[1] + "MHz")
                net = ekt_net.EktNetClient('192.168.1.24', 9999)
                # print str(FREQUENCY_LEVEL_OFFSET[0])
                # print type(str(FREQUENCY_LEVEL_OFFSET[0]))
                net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": FREQUENCY_OFFSET[0]}))
                time.sleep(1)
                del net
                net = ekt_net.EktNetClient('192.168.1.24', 9999)
                net.send_data(json.dumps({"cmd": "set_symbol_rate_data", "symbol_rate": str(SYMBOL_RATE_FREQUENCY[1])}))
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
                                      ("current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，{}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn,
                                          FREQUENCY_OFFSET[1], SYMBOL_RATE_FREQUENCY[1], "锁台失败") + "\n"))
                    continue
                else:
                    write_test_result("./test_result_sfe.txt", ("出错了" + "\n"))
                    continue
                try:
                    start_data_result = mosaic_algorithm(sfe_ip, LEVEL_50, "-50 dBm")
                    print "current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，马赛克检测结果：{}".format(
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn,
                        FREQUENCY_OFFSET[1], SYMBOL_RATE_FREQUENCY[1], start_data_result.get("detect_mosic_result"))
                    write_test_result("./test_result_sfe.txt",
                                      "current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，马赛克检测结果：{}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn,
                                          FREQUENCY_OFFSET[1], SYMBOL_RATE_FREQUENCY[1],
                                          start_data_result.get("detect_mosic_result")) + "\n")
                except:
                    start_data_result = mosaic_algorithm(sfe_ip, LEVEL_50, "-50 dBm")
                    print "current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，马赛克检测结果：{}".format(
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn,
                        FREQUENCY_OFFSET[1], SYMBOL_RATE_FREQUENCY[1], start_data_result.get("detect_mosic_result"))
                    write_test_result("./test_result_sfe.txt",
                                      "current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，马赛克检测结果：{}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn,
                                          FREQUENCY_OFFSET[1], SYMBOL_RATE_FREQUENCY[1],
                                          start_data_result.get("detect_mosic_result")) + "\n")

                """
                进行机顶盒的频率修改或其他参数的修改
                读取误码率或者判断机顶盒是否含有马赛克
                """

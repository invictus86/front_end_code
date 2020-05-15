#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
from ekt_lib import ekt_net, ekt_cfg
import datetime
from ekt_lib.ekt_sfe import Ektsfe
from ekt_lib.ekt_stb_tester import stb_tester_detect_motion
from ekt_lib.threshold_algorithm_SFE import mosaic_algorithm
from ekt_lib.ekt_utils import write_test_result, read_ekt_config_data, find_level_offset_by_frequency

CODE_RATE_LIST = ["R1_2", "R2_3", "R3_4", "R5_6", "R7_8"]

MODULATION_QPSK = "S4"
LEVEL_OFFSET_950 = find_level_offset_by_frequency("DVBS_S2_FREQUENCY_LEVEL_OFFSET", 950)
LEVEL_50_950 = str("%.2f" % ((-50) - LEVEL_OFFSET_950))
LEVEL_OFFSET_1550 = find_level_offset_by_frequency("DVBS_S2_FREQUENCY_LEVEL_OFFSET", 1550)
LEVEL_50_1550 = str("%.2f" % ((-50) - LEVEL_OFFSET_1550))
LEVEL_OFFSET_2150 = find_level_offset_by_frequency("DVBS_S2_FREQUENCY_LEVEL_OFFSET", 2150)
LEVEL_50_2150 = str("%.2f" % ((-50) - LEVEL_OFFSET_2150))

SYMBOL_RATE_FREQUENCY_5M = ["5.000000e6", "05000", [["950", "952", LEVEL_50_950], ["1550", "1552", LEVEL_50_1550],
                                                    ["2150", "2148", LEVEL_50_2150]]]
SYMBOL_RATE_FREQUENCY_27_5M = ["27.500000e6", "27500", [["950", "952", LEVEL_50_950], ["1550", "1552", LEVEL_50_1550],
                                                        ["2150", "2148", LEVEL_50_2150]]]
SYMBOL_RATE_FREQUENCY_45M = ["45.000000e6", "45000", [["950", "952", LEVEL_50_950], ["1550", "1552", LEVEL_50_1550],
                                                      ["2150", "2148", LEVEL_50_2150]]]

dict_config_data = {
    "SYMBOL_RATE_FREQUENCY": [SYMBOL_RATE_FREQUENCY_5M, SYMBOL_RATE_FREQUENCY_27_5M, SYMBOL_RATE_FREQUENCY_45M]}

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
    specan = Ektsfe(sfe_ip)
    specan.clean_reset()
    specan = Ektsfe(sfe_ip)
    specan.preset_instrument()
    specan = Ektsfe(sfe_ip)
    specan.set_digitaltv_input_source("TSPL")
    specan = Ektsfe(sfe_ip)
    specan.set_digitaltv_input_load(r"D:\TSGEN\SDTV\DVB_25Hz\720_576i\LIVE\DIVER.GTS")

    dict_data = read_ekt_config_data("../ekt_lib/ekt_config.json")
    # DVBS_S2_FREQUENCY_LEVEL_OFFSET = dict_data.get("DVBS_S2_FREQUENCY_LEVEL_OFFSET")
    # DVBS_QPSK_CODE_RATE_CN = dict_data.get("DVBS_QPSK_CODE_RATE_CN")
    # DVBS2_8PSK_CODE_RATE_CN = dict_data.get("DVBS2_8PSK_CODE_RATE_CN")

    for code_rate_cn in CODE_RATE_LIST:
        del specan
        specan = Ektsfe(sfe_ip)
        specan.set_digitaltv_coding_coderate(code_rate_cn)
        time.sleep(1)
        for SYMBOL_RATE_FREQUENCY in dict_config_data.get("SYMBOL_RATE_FREQUENCY"):
            del specan
            specan = Ektsfe(sfe_ip)
            specan.set_digitaltv_coding_symbolrate(SYMBOL_RATE_FREQUENCY[0])
            for FREQUENCY_OFFSET in SYMBOL_RATE_FREQUENCY[2]:
                del specan
                specan = Ektsfe(sfe_ip)
                specan.set_frequency_frequency_frequency(FREQUENCY_OFFSET[0] + "MHz")
                specan = Ektsfe(sfe_ip)
                specan.set_level_level_level(FREQUENCY_OFFSET[2] + " dBm")
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
                    write_test_result("./../ekt_log/test_result_sfe.txt",
                                      (
                                              "dvbs_signal_tracking_frequency_range: current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, {}".format(
                                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                  code_rate_cn,
                                                  FREQUENCY_OFFSET[1], SYMBOL_RATE_FREQUENCY[1],
                                                  FREQUENCY_OFFSET[2], "锁台失败") + "\n"))
                    continue
                else:
                    write_test_result("./../ekt_log/test_result_sfe.txt", ("出错了" + "\n"))
                    continue
                try:
                    mosaic_algorithm(sfe_ip, FREQUENCY_OFFSET[2], "-50")
                    specan = Ektsfe(sfe_ip)
                    specan.set_frequency_frequency_frequency(FREQUENCY_OFFSET[1] + "MHz")
                    start_data_result = mosaic_algorithm(sfe_ip, FREQUENCY_OFFSET[2], "-50")
                    print "dvbs_signal_tracking_frequency_range: current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, 马赛克检测结果：{}".format(
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn,
                        FREQUENCY_OFFSET[1], SYMBOL_RATE_FREQUENCY[1], FREQUENCY_OFFSET[2],
                        start_data_result.get("detect_mosic_result"))
                    write_test_result("./../ekt_log/test_result_sfe.txt",
                                      "dvbs_signal_tracking_frequency_range: current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, 马赛克检测结果：{}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn,
                                          FREQUENCY_OFFSET[1], SYMBOL_RATE_FREQUENCY[1], FREQUENCY_OFFSET[2],
                                          start_data_result.get("detect_mosic_result")) + "\n")
                except:
                    mosaic_algorithm(sfe_ip, FREQUENCY_OFFSET[2], "-50")
                    specan = Ektsfe(sfe_ip)
                    specan.set_frequency_frequency_frequency(FREQUENCY_OFFSET[1] + "MHz")
                    start_data_result = mosaic_algorithm(sfe_ip, FREQUENCY_OFFSET[2], "-50")
                    print "dvbs_signal_tracking_frequency_range: current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, 马赛克检测结果：{}".format(
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn,
                        FREQUENCY_OFFSET[1], SYMBOL_RATE_FREQUENCY[1], FREQUENCY_OFFSET[2],
                        start_data_result.get("detect_mosic_result"))
                    write_test_result("./../ekt_log/test_result_sfe.txt",
                                      "dvbs_signal_tracking_frequency_range: current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, 马赛克检测结果：{}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn,
                                          FREQUENCY_OFFSET[1], SYMBOL_RATE_FREQUENCY[1], FREQUENCY_OFFSET[2],
                                          start_data_result.get("detect_mosic_result")) + "\n")

                """
                进行机顶盒的频率修改或其他参数的修改
                读取误码率或者判断机顶盒是否含有马赛克
                """

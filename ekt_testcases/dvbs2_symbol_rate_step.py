#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
from ekt_lib import ekt_net, ekt_cfg
import datetime
from ekt_lib.ekt_sfu import Ektsfu
from ekt_lib.ekt_stb_tester import stb_tester_detect_motion
from ekt_lib.threshold_algorithm_SFU import mosaic_algorithm
from ekt_lib.ekt_utils import write_test_result, read_ekt_config_data, generate_symbol_rate_list, \
    find_level_offset_by_frequency

CODE_RATE_3_4 = "R3_4"
MODULATION_8PSK = "S8"
FREQUENCY_1550 = "1550"
CN = "8.9"
LEVEL_OFFSET = find_level_offset_by_frequency("DVBS_S2_FREQUENCY_LEVEL_OFFSET", int(FREQUENCY_1550))
LEVEL_65 = str("%.2f" % ((-65) - LEVEL_OFFSET))

SYMBOL_RATE_LIST = generate_symbol_rate_list()

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
    sfu_ip = "192.168.1.50"
    specan = Ektsfu(sfu_ip)
    specan.preset_instrument()
    specan = Ektsfu(sfu_ip)
    specan.set_modulation_modulation_source("DTV")
    specan = Ektsfu(sfu_ip)
    specan.set_modulation_modulation_standard_dvt("DVS2")
    time.sleep(1)
    specan = Ektsfu(sfu_ip)
    specan.set_player_timing_openfile(r"E:\333\DIVER.GTS")
    time.sleep(1)
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_input_source_dvbs2("TSPLayer")
    time.sleep(1)
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_coding_constellation_dvbs2(MODULATION_8PSK)
    time.sleep(1)
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_rf("ON")
    time.sleep(1)
    specan = Ektsfu(sfu_ip)
    specan.set_noise_noise_noise("ADD")
    specan = Ektsfu(sfu_ip)
    specan.set_noise_noise_awgn("ON")
    time.sleep(1)
    specan.set_impairments_modulator("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_baseband("OFF")

    dict_data = read_ekt_config_data("../ekt_lib/ekt_config.json")
    # DVBS_S2_FREQUENCY_LEVEL_OFFSET = dict_data.get("DVBS_S2_FREQUENCY_LEVEL_OFFSET")
    # DVBS2_QPSK_CODE_RATE_CN = dict_data.get("DVBS2_QPSK_CODE_RATE_CN")

    # for code_rate_cn in DVBS2_QPSK_CODE_RATE_CN:
    #     del specan
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_coding_coderate_dvbs2(CODE_RATE_3_4)
    time.sleep(1)
    specan = Ektsfu(sfu_ip)
    specan.set_noise_awgn_cn(CN)
    time.sleep(1)
    specan = Ektsfu(sfu_ip)
    specan.set_frequency_frequency_frequency(FREQUENCY_1550 + "MHz")
    time.sleep(1)
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_offset(str("-4.1"))
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_level("dBm", LEVEL_65)

    for SYMBOL_RATE in SYMBOL_RATE_LIST:
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_symbolrate_dvbs2(SYMBOL_RATE[0])

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
        stb_tester_detect_motion(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                 ["tests/front_end_test/testcases.py::test_continuous_button"],
                                 "auto_front_end_test", "DSD4614iALM")
        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
        if lock_state == "1":
            pass
        elif lock_state == "0":
            write_test_result("../ekt_log/test_result_sfu.txt",
                              ("dvbs2_symbol_rate_step: current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), CODE_RATE_3_4,
                                  FREQUENCY_1550, str(SYMBOL_RATE[1]), "锁台失败") + "\n"))
            continue
        else:
            write_test_result("../ekt_log/test_result_sfu.txt", ("出错了" + "\n"))
            continue
        try:
            start_data_result = mosaic_algorithm(sfu_ip, "-65", "-50")
            print "dvbs2_symbol_rate_step: current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，马赛克检测结果：{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), CODE_RATE_3_4,
                FREQUENCY_1550, str(SYMBOL_RATE[1]), start_data_result.get("detect_mosic_result"))
            write_test_result("../ekt_log/test_result_sfu.txt",
                              "dvbs2_symbol_rate_step: current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，马赛克检测结果：{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), CODE_RATE_3_4,
                                  FREQUENCY_1550, str(SYMBOL_RATE[1]),
                                  start_data_result.get("detect_mosic_result")) + "\n")
        except:
            start_data_result = mosaic_algorithm(sfu_ip, "-65", "-50")
            print "dvbs2_symbol_rate_step: current_time:{},  coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，马赛克检测结果：{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), CODE_RATE_3_4,
                FREQUENCY_1550, str(SYMBOL_RATE[1]), start_data_result.get("detect_mosic_result"))
            write_test_result("../ekt_log/test_result_sfu.txt",
                              "dvbs2_symbol_rate_step: current_time:{},  coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，马赛克检测结果：{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), CODE_RATE_3_4,
                                  str(FREQUENCY_1550), str(SYMBOL_RATE[1]),
                                  start_data_result.get("detect_mosic_result")) + "\n")

        """
        进行机顶盒的频率修改或其他参数的修改
        读取误码率或者判断机顶盒是否含有马赛克
        """

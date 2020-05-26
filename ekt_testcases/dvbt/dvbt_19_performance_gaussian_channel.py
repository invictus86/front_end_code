#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import datetime
from ekt_lib import ekt_net, ekt_cfg
from ekt_lib.ekt_sfu import Ektsfu
from ekt_lib.ekt_stb_tester import stb_tester_execute_testcase
from ekt_lib.threshold_algorithm_SFU import iterate_to_find_threshold_noise_cn_step_by_step
from ekt_lib.ekt_utils import write_test_result, read_ekt_config_data

MODULATION_QPSK = "T4"
MODULATION_16QAM = "T16"
MODULATION_64QAM = "T64"

CODE_RATE_1_2 = "R1_2"
CODE_RATE_2_3 = "R2_3"
CODE_RATE_3_4 = "R3_4"
CODE_RATE_5_6 = "R5_6"
CODE_RATE_7_8 = "R7_8"

GUARD_G1_4 = "G1_4"
GUARD_G1_8 = "G1_8"

MODULATION__CODERATE_SPEC_LIST = [
    [MODULATION_QPSK, CODE_RATE_1_2, GUARD_G1_4, 7.0],
    [MODULATION_QPSK, CODE_RATE_2_3, GUARD_G1_4, 7.0],
    [MODULATION_QPSK, CODE_RATE_3_4, GUARD_G1_4, 7.0],
    [MODULATION_QPSK, CODE_RATE_5_6, GUARD_G1_4, 7.0],
    [MODULATION_QPSK, CODE_RATE_7_8, GUARD_G1_4, 7.0],
    [MODULATION_16QAM, CODE_RATE_1_2, GUARD_G1_4, 7.0],
    [MODULATION_16QAM, CODE_RATE_2_3, GUARD_G1_4, 7.0],
    [MODULATION_16QAM, CODE_RATE_3_4, GUARD_G1_4, 7.0],
    [MODULATION_16QAM, CODE_RATE_5_6, GUARD_G1_4, 7.0],
    [MODULATION_16QAM, CODE_RATE_7_8, GUARD_G1_4, 7.0],
    [MODULATION_64QAM, CODE_RATE_1_2, GUARD_G1_4, 7.0],
    [MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_4, 7.0],
    [MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, 7.0],
    [MODULATION_64QAM, CODE_RATE_3_4, GUARD_G1_4, 7.0],
    [MODULATION_64QAM, CODE_RATE_5_6, GUARD_G1_4, 7.0],
    [MODULATION_64QAM, CODE_RATE_7_8, GUARD_G1_4, 7.0]]

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
    specan.set_modulation_modulation_standard_dvt("DVBT")
    specan = Ektsfu(sfu_ip)
    specan.set_player_timing_openfile(r"E:\333\DIVER.GTS")
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_input_source_dvbt("TSPLayer")
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_rf("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_noise_noise_noise("ADD")
    specan = Ektsfu(sfu_ip)
    specan.set_noise_noise_awgn("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_noise_settings_bandwith("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_fading_fading_state("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_modulator("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_baseband("OFF")

    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_coding_fftmode_dvbt("M8K")

    dict_data = read_ekt_config_data("../../ekt_lib/ekt_config.json")
    DVBT_T2_FREQUENCY_LEVEL_OFFSET = dict_data.get("DVBT_T2_FREQUENCY_LEVEL_OFFSET")
    # DVBS2_QPSK_CODE_RATE_CN = dict_data.get("DVBS2_QPSK_CODE_RATE_CN")
    # DVBS2_8PSK_CODE_RATE_CN = dict_data.get("DVBS2_8PSK_CODE_RATE_CN")

    for FREQUENCY_LEVEL_OFFSET in DVBT_T2_FREQUENCY_LEVEL_OFFSET:
        if FREQUENCY_LEVEL_OFFSET[0] < 400:
            CURRENT_BANDWIDTH = 7
            # specan = Ektsfu(sfu_ip)
            # specan.set_digitaltv_framing_fftsize_dvbt2("M32K")
        else:
            CURRENT_BANDWIDTH = 8
            # specan = Ektsfu(sfu_ip)
            # specan.set_digitaltv_framing_fftsize_dvbt2("M32E")
        specan = Ektsfu(sfu_ip)
        specan.set_frequency_frequency_frequency(str(int(FREQUENCY_LEVEL_OFFSET[0])) + "MHz")
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_channelbandwidth_dvbt("BW_{}".format(str(CURRENT_BANDWIDTH)))
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_offset(str(FREQUENCY_LEVEL_OFFSET[1]))
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_level("dBm", "-60")
        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(
            json.dumps({"cmd": "set_frequency_data", "frequency": str(int(FREQUENCY_LEVEL_OFFSET[0]))}))
        time.sleep(1)
        del net
        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(json.dumps({"cmd": "set_bandwidth_data", "bandwidth": str(CURRENT_BANDWIDTH)}))
        time.sleep(1)
        del net
        """
        触发stb-tester进行频率和符号率设置
        """
        stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                    ["tests/front_end_test/testcases.py::test_continuous_button_7414g"],
                                    "auto_front_end_test", "DSD4614iALM")
        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
        if lock_state == "1":
            pass
        elif lock_state == "0":
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              (
                                      "dvbt2_receiver_signal_input__min_level: current_time:{}, frequency：{} MHz，bandwidth：{} Ksym/s, {}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          str(FREQUENCY_LEVEL_OFFSET[0]), str(CURRENT_BANDWIDTH),
                                          "锁台失败") + "\n"))
            continue
        else:
            write_test_result("../../ekt_log/test_result_sfu.txt", ("出错了" + "\n"))
            continue
        for MODULATION_CODERATE_SPEC in MODULATION__CODERATE_SPEC_LIST:
            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_coding_constellation_dvbt(MODULATION_CODERATE_SPEC[0])
            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_coding_coderate_dvbt(MODULATION_CODERATE_SPEC[1])
            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_coding_guard_dvbt(MODULATION_CODERATE_SPEC[2])

            try:
                res = iterate_to_find_threshold_noise_cn_step_by_step(sfu_ip, MODULATION_CODERATE_SPEC[3] + 3)
                print "dvbt_19_performance_gaussian_channel: current_time:{}, modulation: {} coderate：{}, frequency：{} MHz，bandwidth：{} MHZ，{}".format(
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), MODULATION_CODERATE_SPEC[0],
                    MODULATION_CODERATE_SPEC[1], str(FREQUENCY_LEVEL_OFFSET[0]), str(CURRENT_BANDWIDTH), res)
                write_test_result("../../ekt_log/test_result_sfu.txt",
                                  "dvbt_19_performance_gaussian_channel: current_time:{}, modulation: {} coderate：{}, frequency：{} MHz，bandwidth：{} MHZ，{}".format(
                                      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                      MODULATION_CODERATE_SPEC[0], MODULATION_CODERATE_SPEC[1],
                                      str(FREQUENCY_LEVEL_OFFSET[0]), str(CURRENT_BANDWIDTH), res) + "\n")
            except:
                res = iterate_to_find_threshold_noise_cn_step_by_step(sfu_ip, MODULATION_CODERATE_SPEC[3] + 3)
                print "dvbt_19_performance_gaussian_channel: current_time:{}, modulation: {} coderate：{}, frequency：{} MHz，bandwidth：{} MHZ，{}".format(
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), MODULATION_CODERATE_SPEC[0],
                    MODULATION_CODERATE_SPEC[1], str(FREQUENCY_LEVEL_OFFSET[0]), str(CURRENT_BANDWIDTH), res)
                write_test_result("../../ekt_log/test_result_sfu.txt",
                                  "dvbt_19_performance_gaussian_channel: current_time:{}, modulation: {} coderate：{}, frequency：{} MHz，bandwidth：{} MHZ，{}".format(
                                      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                      MODULATION_CODERATE_SPEC[0], MODULATION_CODERATE_SPEC[1],
                                      str(FREQUENCY_LEVEL_OFFSET[0]), str(CURRENT_BANDWIDTH), res) + "\n")
            """
            进行机顶盒的频率修改或其他参数的修改
            读取误码率或者判断机顶盒是否含有马赛克
            """

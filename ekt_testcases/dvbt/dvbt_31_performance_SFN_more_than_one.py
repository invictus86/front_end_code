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
from ekt_lib.threshold_algorithm_SFU import iterate_to_find_threshold_noise_cn_step_by_step
from ekt_lib.ekt_utils import write_test_result, write_json_file, read_json_file, find_level_offset_by_frequency, \
    dvbt_31_performance_SFN_json_to_csv

FFT_SIZE_8K = "M8K"

MODULATION_QPSK = "T4"
MODULATION_16QAM = "T16"
MODULATION_64QAM = "T64"

CODE_RATE_1_2 = "R1_2"
CODE_RATE_2_3 = "R2_3"
CODE_RATE_3_4 = "R3_4"

GUARD_G1_4 = "G1_4"
GUARD_G1_8 = "G1_8"

FREQUENCY_666 = 666
LEVEL_OFFSET_666 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", 666.0)
LEVEL_50_666 = str("%.2f" % (-50 - LEVEL_OFFSET_666))

PARAMETER_LIST = [
    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_3_4, GUARD_G1_4, 27.6, [
        [0, 100.1, 0, 0, 0, 200.1, None],
        [0, 100.1, 3, 0, 3, 200.1, None],
        [0, 100.1, 6, 0, 6, 200.1, None],
        [0, 100.1, 9, 0, 9, 200.1, None],
        [0, 100.1, 12, 0, 12, 200.1, None],
        [0, 100.1, 15, 0, 15, 200.1, None],
        [0, 100.1, 18, 0, 18, 200.1, None],
        [0, 100.1, 21, 0, 21, 200.1, None],
        [0, 100.1, 15, 0, 0, 200.1, None],
        [0, 100.1, 15, 0, 3, 200.1, None],
        [0, 100.1, 15, 0, 6, 200.1, None],
        [0, 100.1, 15, 0, 9, 200.1, None],
        [0, 100.1, 15, 0, 12, 200.1, None],
        [0, 100.1, 15, 0, 18, 200.1, None],
        [0, 100.1, 15, 0, 21, 200.1, None],
        [0, 100.1, 0, 0, 15, 200.1, None],
        [0, 100.1, 3, 0, 15, 200.1, None],
        [0, 100.1, 6, 0, 15, 200.1, None],
        [0, 100.1, 9, 0, 15, 200.1, None],
        [0, 100.1, 12, 0, 15, 200.1, None],
        [0, 100.1, 18, 0, 15, 200.1, None],
        [0, 100.1, 21, 0, 15, 200.1, None]]],

    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, 23.2, [
        [0, 50.1, 0, 0, 0, 100.1, None],
        [0, 50.1, 3, 0, 3, 100.1, None],
        [0, 50.1, 6, 0, 6, 100.1, None],
        [0, 50.1, 9, 0, 9, 100.1, None],
        [0, 50.1, 12, 0, 12, 100.1, None],
        [0, 50.1, 15, 0, 15, 100.1, None],
        [0, 50.1, 18, 0, 18, 100.1, None],
        [0, 50.1, 21, 0, 21, 100.1, None],
        [0, 50.1, 15, 0, 0, 100.1, None],
        [0, 50.1, 15, 0, 3, 100.1, None],
        [0, 50.1, 15, 0, 6, 100.1, None],
        [0, 50.1, 15, 0, 9, 100.1, None],
        [0, 50.1, 15, 0, 12, 100.1, None],
        [0, 50.1, 15, 0, 18, 100.1, None],
        [0, 50.1, 15, 0, 21, 100.1, None],
        [0, 50.1, 0, 0, 15, 100.1, None],
        [0, 50.1, 3, 0, 15, 100.1, None],
        [0, 50.1, 6, 0, 15, 100.1, None],
        [0, 50.1, 9, 0, 15, 100.1, None],
        [0, 50.1, 12, 0, 15, 100.1, None],
        [0, 50.1, 18, 0, 15, 100.1, None],
        [0, 50.1, 21, 0, 15, 100.1, None]]],

    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_4, 23.2, [
        [0, 100.1, 0, 0, 0, 200.1, None],
        [0, 100.1, 3, 0, 3, 200.1, None],
        [0, 100.1, 6, 0, 6, 200.1, None],
        [0, 100.1, 9, 0, 9, 200.1, None],
        [0, 100.1, 12, 0, 12, 200.1, None],
        [0, 100.1, 15, 0, 15, 200.1, None],
        [0, 100.1, 18, 0, 18, 200.1, None],
        [0, 100.1, 21, 0, 21, 200.1, None],
        [0, 100.1, 15, 0, 0, 200.1, None],
        [0, 100.1, 15, 0, 3, 200.1, None],
        [0, 100.1, 15, 0, 6, 200.1, None],
        [0, 100.1, 15, 0, 9, 200.1, None],
        [0, 100.1, 15, 0, 12, 200.1, None],
        [0, 100.1, 15, 0, 18, 200.1, None],
        [0, 100.1, 15, 0, 21, 200.1, None],
        [0, 100.1, 0, 0, 15, 200.1, None],
        [0, 100.1, 3, 0, 15, 200.1, None],
        [0, 100.1, 6, 0, 15, 200.1, None],
        [0, 100.1, 9, 0, 15, 200.1, None],
        [0, 100.1, 12, 0, 15, 200.1, None],
        [0, 100.1, 18, 0, 15, 200.1, None],
        [0, 100.1, 21, 0, 15, 200.1, None]]]
]

my_file = Path("../../ekt_json/dvbt_31_performance_SFN_more_than_one.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    list_test_parame_result = []

    for PARAMETER in PARAMETER_LIST:
        list_test_result = []
        for FADING in PARAMETER[5]:
            list_test_result.append(
                [FADING[0], FADING[1], FADING[2], FADING[3], FADING[4], FADING[5], FADING[6]])
        list_test_parame_result.append(
            [PARAMETER[0], PARAMETER[1], PARAMETER[2], PARAMETER[3], PARAMETER[4], list_test_result])
    dict_test_parame_result["test_parame_result"] = list_test_parame_result
    write_json_file("../../ekt_json/dvbt_31_performance_SFN_more_than_one.json",
                    dict_test_parame_result)

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
    load_dict = read_json_file("../../ekt_json/dvbt_31_performance_SFN_more_than_one.json")
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
    specan.set_fading_fading_state("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_modulator("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_baseband("OFF")

    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_state("2", "1", "ON")
    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_state("3", "1", "ON")
    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_state("4", "1", "ON")

    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_profile("2", "1", "SPATh")
    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_profile("3", "1", "SPATh")
    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_profile("4", "1", "SPATh")

    specan = Ektsfu(sfu_ip)
    specan.set_frequency_frequency_frequency(str(FREQUENCY_666) + "MHz")
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_coding_channelbandwidth_dvbt("BW_{}".format(str(8)))
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_offset(str(LEVEL_OFFSET_666))
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_level("dBm", str(LEVEL_50_666))

    net = ekt_net.EktNetClient('192.168.1.24', 9999)
    net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": str(int(FREQUENCY_666))}))
    time.sleep(1)
    del net
    net = ekt_net.EktNetClient('192.168.1.24', 9999)
    net.send_data(json.dumps({"cmd": "set_bandwidth_data", "bandwidth": str(8)}))
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
                                  "dvbt_31_performance_SFN_more_than_one: current_time:{}, frequency:{} MHz,bandwidth:{} Ksym/s, {}".format(
                                      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                      str(FREQUENCY_666), str(8), "Lock fail") + "\n"))

    for PARAMETER in load_dict.get("test_parame_result"):
        loop_lock_mark = False
        for FADING in PARAMETER[5]:
            if FADING[6] == None:
                loop_lock_mark = True
                break
        if loop_lock_mark == True:
            pass
        else:
            continue

        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_fftmode_dvbt(PARAMETER[0])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_constellation_dvbt(PARAMETER[1])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_coderate_dvbt(PARAMETER[2])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_guard_dvbt(PARAMETER[3])

        for FADING in PARAMETER[5]:
            if FADING[6] == None:
                pass
            else:
                continue
            specan = Ektsfu(sfu_ip)
            specan.set_fading_profile_pathloss("2", "1", "{} dB".format(str(FADING[0])))
            specan = Ektsfu(sfu_ip)
            specan.set_fading_profile_basicdelay("2", "{}E-6".format(FADING[1]))
            specan = Ektsfu(sfu_ip)
            specan.set_fading_profile_pathloss("3", "1", "{} dB".format(str(FADING[2])))
            specan = Ektsfu(sfu_ip)
            specan.set_fading_profile_basicdelay("3", "{}E-6".format(FADING[3]))
            specan = Ektsfu(sfu_ip)
            specan.set_fading_profile_pathloss("4", "1", "{} dB".format(str(FADING[4])))
            specan = Ektsfu(sfu_ip)
            specan.set_fading_profile_basicdelay("4", "{}E-6".format(FADING[5]))

            res, test_result = iterate_to_find_threshold_noise_cn_step_by_step(sfu_ip, PARAMETER[4])
            print(
                "dvbt_31_performance_SFN_more_than_one: current_time:{}, modulation: {} coderate:{}, frequency:{} MHz,bandwidth:{} MHZ,{}".format(
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), PARAMETER[1],
                    PARAMETER[2], str(FREQUENCY_666), str(8), res))
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              "dvbt_31_performance_SFN_more_than_one: current_time:{}, modulation: {} coderate:{}, frequency:{} MHz,bandwidth:{} MHZ,{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), PARAMETER[1],
                                  PARAMETER[2], str(FREQUENCY_666), str(8), res) + "\n")

            FADING[6] = test_result
            write_json_file("../../ekt_json/dvbt_31_performance_SFN_more_than_one.json", load_dict)
            dvbt_31_performance_SFN_json_to_csv(
                "../../ekt_json/dvbt_31_performance_SFN_more_than_one.json",
                "../../ekt_test_report/dvbt_31_performance_SFN_more_than_one.csv")

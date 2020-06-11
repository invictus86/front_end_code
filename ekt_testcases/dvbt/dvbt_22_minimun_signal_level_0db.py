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
from ekt_lib.threshold_algorithm_SFU import mosaic_algorithm, iterate_to_find_threshold_step_by_step
from ekt_lib.ekt_utils import write_test_result, find_level_offset_by_frequency, write_json_file, read_json_file, \
    dvbt_22_minimun_level_0db_to_csv

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

FREQUENCY_199 = 199
LEVEL_OFFSET_198_5 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", 198.5)
LEVEL_50_199 = str("%.2f" % (-50 - LEVEL_OFFSET_198_5))

PARAMETER_LIST = [
    [FREQUENCY_666, LEVEL_OFFSET_666, LEVEL_50_666, 8, [
        [FFT_SIZE_8K, MODULATION_QPSK, CODE_RATE_1_2, GUARD_G1_4, -89.4,
         [1.95, 10, 28, 56, 70, 90, 105, 112.1, 170, 212]],
        [FFT_SIZE_8K, MODULATION_QPSK, CODE_RATE_2_3, GUARD_G1_4, -84.5,
         [1.95, 10, 28, 56, 70, 90, 105, 112.1, 170, 212]],
        [FFT_SIZE_8K, MODULATION_QPSK, CODE_RATE_3_4, GUARD_G1_4, -80.8,
         [1.95, 10, 28, 56, 70, 90, 105, 112.1, 170, 212]],
        [FFT_SIZE_8K, MODULATION_16QAM, CODE_RATE_1_2, GUARD_G1_4, -84.9,
         [1.95, 10, 28, 56, 70, 90, 105, 112.1, 170, 212]],
        [FFT_SIZE_8K, MODULATION_16QAM, CODE_RATE_2_3, GUARD_G1_4, -80.3,
         [1.95, 10, 28, 56, 70, 90, 105, 112.1, 170, 212]],
        [FFT_SIZE_8K, MODULATION_16QAM, CODE_RATE_3_4, GUARD_G1_4, -76.1,
         [1.95, 10, 28, 56, 70, 90, 105, 112.1, 170, 212]],
        [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_1_2, GUARD_G1_4, -79.2,
         [1.95, 10, 28, 56, 70, 90, 105, 112.1, 170, 212]],
        [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_4, -75.0,
         [1.95, 10, 28, 56, 70, 90, 105, 112.1, 170, 212]],
        [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, -75.0,
         [1.95, 10, 28, 56, 70, 90, 105]],
        [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_3_4, GUARD_G1_4, -70.6,
         [1.95, 10, 28, 56, 70, 90, 105, 112.1, 170, 212]]]
     ],
    [FREQUENCY_199, LEVEL_OFFSET_198_5, LEVEL_50_199, 7, [
        [FFT_SIZE_8K, MODULATION_QPSK, CODE_RATE_1_2, GUARD_G1_4, -89.9,
         [1.95, 10, 28, 56, 70, 90, 105, 128.1, 170, 243]],
        [FFT_SIZE_8K, MODULATION_QPSK, CODE_RATE_2_3, GUARD_G1_4, -85.0,
         [1.95, 10, 28, 56, 70, 90, 105, 128.1, 170, 243]],
        [FFT_SIZE_8K, MODULATION_QPSK, CODE_RATE_3_4, GUARD_G1_4, -81.3,
         [1.95, 10, 28, 56, 70, 90, 105, 128.1, 170, 243]],
        [FFT_SIZE_8K, MODULATION_16QAM, CODE_RATE_1_2, GUARD_G1_4, -85.4,
         [1.95, 10, 28, 56, 70, 90, 105, 128.1, 170, 243]],
        [FFT_SIZE_8K, MODULATION_16QAM, CODE_RATE_2_3, GUARD_G1_4, -80.8,
         [1.95, 10, 28, 56, 70, 90, 105, 128.1, 170, 243]],
        [FFT_SIZE_8K, MODULATION_16QAM, CODE_RATE_3_4, GUARD_G1_4, -76.6,
         [1.95, 10, 28, 56, 70, 90, 105, 128.1, 170, 243]],
        [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_1_2, GUARD_G1_4, -79.7,
         [1.95, 10, 28, 56, 70, 90, 105, 128.1, 170, 243]],
        [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_4, -75.5,
         [1.95, 10, 28, 56, 70, 90, 105, 128.1, 170, 243]],
        [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, -75.5,
         [1.95, 10, 28, 56, 70, 90, 105]],
        [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_3_4, GUARD_G1_4, -71.1,
         [1.95, 10, 28, 56, 70, 90, 105, 128.1, 170, 243]]]
     ]
]

my_file = Path("../../ekt_json/dvbt_22_minimun_signal_level_0db.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    list_test_parame_result = []

    for PARAMETER_FIXED in PARAMETER_LIST:
        list_test_parame = []
        for PARAMETER in PARAMETER_FIXED[4]:
            list_test_result = []
            for fading in PARAMETER[5]:
                list_test_result.append([fading, None])
            list_test_parame.append(
                [PARAMETER[0], PARAMETER[1], PARAMETER[2], PARAMETER[3], PARAMETER[4], list_test_result])
        list_test_parame_result.append(
            [PARAMETER_FIXED[0], PARAMETER_FIXED[1], PARAMETER_FIXED[2], PARAMETER_FIXED[3], list_test_parame])

    dict_test_parame_result["test_parame_result"] = list_test_parame_result
    write_json_file("../../ekt_json/dvbt_22_minimun_signal_level_0db.json",
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
    load_dict = read_json_file("../../ekt_json/dvbt_22_minimun_signal_level_0db.json")
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
    specan.set_noise_noise_noise("OFF")
    # specan = Ektsfu(sfu_ip)
    # specan.set_noise_noise_awgn("ON")
    # specan = Ektsfu(sfu_ip)
    # specan.set_noise_settings_bandwith("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_fading_fading_state("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_modulator("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_baseband("OFF")

    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_state("1", "1", "ON")
    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_state("2", "1", "ON")

    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_profile("1", "1", "SPATh")
    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_profile("2", "1", "SPATh")


    for PARAMETER_FIXED in load_dict.get("test_parame_result"):
        for PARAMETER in PARAMETER_FIXED[4]:
            loop_lock_mark = False
            for FADING in PARAMETER[5]:
                if FADING[1] == None:
                    loop_lock_mark = True
                    break
            if loop_lock_mark == True:
                pass
            else:
                continue
            specan = Ektsfu(sfu_ip)
            specan.set_frequency_frequency_frequency(str(PARAMETER_FIXED[0]) + "MHz")
            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_coding_channelbandwidth_dvbt("BW_{}".format(str(PARAMETER_FIXED[3])))
            specan = Ektsfu(sfu_ip)
            specan.set_level_level_offset(str(PARAMETER_FIXED[1]))
            specan = Ektsfu(sfu_ip)
            specan.set_level_level_level("dBm", str(PARAMETER_FIXED[2]))

            net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
            net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": str(int(PARAMETER_FIXED[0]))}))
            time.sleep(1)
            del net
            net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
            net.send_data(json.dumps({"cmd": "set_bandwidth_data", "bandwidth": str(PARAMETER_FIXED[3])}))
            time.sleep(1)
            del net
            """
            触发stb-tester进行频率和符号率设置
            """
            stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                        ["tests/front_end_test/testcases.py::test_continuous_button_7414g"],
                                        "auto_front_end_test", "DSD4614iALM")
            net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
            lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
            if lock_state == "1":
                pass
            elif lock_state == "0":
                write_test_result("../../ekt_log/test_result_sfu.txt",
                                  (
                                          "dvbt_22_minimun_signal_level_0db: current_time:{}, frequency:{} MHz,bandwidth:{} Ksym/s, {}".format(
                                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                              str(PARAMETER_FIXED[0]), str(8), "Lock fail") + "\n"))

            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_coding_fftmode_dvbt(PARAMETER[0])
            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_coding_constellation_dvbt(PARAMETER[1])
            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_coding_coderate_dvbt(PARAMETER[2])
            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_coding_guard_dvbt(PARAMETER[3])

            for FADING in PARAMETER[5]:
                if FADING[1] == None:
                    pass
                else:
                    continue
                specan = Ektsfu(sfu_ip)
                specan.set_fading_profile_basicdelay("2", "{}E-6".format(str(FADING[0])))

                # 设置spec
                res, test_result = iterate_to_find_threshold_step_by_step(sfu_ip,
                                                                          float(
                                                                              "%.2f" % (PARAMETER[4] - PARAMETER_FIXED[
                                                                                  1] + 5)),
                                                                          level_offset=str(PARAMETER_FIXED[1]))
                print(
                    "dvbt_22_minimun_signal_level_0db: current_time:{}, modulation: {} coderate:{}, frequency:{} MHz,bandwidth:{} MHZ,{}".format(
                        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), PARAMETER[1],
                        PARAMETER[2], str(PARAMETER_FIXED[0]), str(PARAMETER_FIXED[3]), res))
                write_test_result("../../ekt_log/test_result_sfu.txt",
                                  "dvbt_22_minimun_signal_level_0db: current_time:{}, modulation: {} coderate:{}, frequency:{} MHz,bandwidth:{} MHZ,{}".format(
                                      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), PARAMETER[1],
                                      PARAMETER[2], str(PARAMETER_FIXED[0]), str(PARAMETER_FIXED[3]), res) + "\n")

                FADING[1] = test_result
                write_json_file("../../ekt_json/dvbt_22_minimun_signal_level_0db.json", load_dict)
                dvbt_22_minimun_level_0db_to_csv(
                    "../../ekt_json/dvbt_22_minimun_signal_level_0db.json",
                    "../../ekt_test_report/dvbt_22_minimun_signal_level_0db.csv")

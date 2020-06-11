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
from ekt_lib.threshold_algorithm_SFU import mosaic_algorithm, iterate_to_find_threshold_noise_cn_step_by_step
from ekt_lib.ekt_utils import write_test_result, find_level_offset_by_frequency, write_json_file, read_json_file, \
    dvbt2_68_performance_in_SFN_echo_json_to_csv

FREQUENCY_666 = 666
LEVEL_OFFSET_666 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", 666.0)
LEVEL_50_666 = str("%.2f" % (-50 - LEVEL_OFFSET_666))

FREQUENCY_199 = 199
LEVEL_OFFSET_198_5 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", 198.5)
LEVEL_50_199 = str("%.2f" % (-50 - LEVEL_OFFSET_198_5))

MODULATION_QPSK = "T4"
MODULATION_16QAM = "T16"
MODULATION_64QAM = "T64"
MODULATION_256QAM = "T256"

CODE_RATE_1_2 = "R1_2"
CODE_RATE_3_5 = "R3_5"
CODE_RATE_2_3 = "R2_3"
CODE_RATE_3_4 = "R3_4"
CODE_RATE_4_5 = "R4_5"
CODE_RATE_5_6 = "R5_6"

GUARD_G1_128 = "G1128"
GUARD_G1_32 = "G1_32"
GUARD_G1_16 = "G1_16"
GUARD_G19_256 = "G19256"
GUARD_G1_8 = "G1_8"
GUARD_G19_128 = "G19128"
GUARD_G1_4 = "G1_4"

KE32 = "M32E"
KN32 = "M32K"

PARAMETER_LIST = [
    [FREQUENCY_666, LEVEL_OFFSET_666, LEVEL_50_666, 8, KE32, MODULATION_256QAM, "PP4", CODE_RATE_2_3, GUARD_G1_16,
     24.6, [
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
    [FREQUENCY_666, LEVEL_OFFSET_666, LEVEL_50_666, 8, KE32, MODULATION_256QAM, "PP4", CODE_RATE_3_5, GUARD_G19_256,
     22.6, [
         [0, 120.1, 0, 0, 0, 240.1, None],
         [0, 120.1, 3, 0, 3, 240.1, None],
         [0, 120.1, 6, 0, 6, 240.1, None],
         [0, 120.1, 9, 0, 9, 240.1, None],
         [0, 120.1, 12, 0, 12, 240.1, None],
         [0, 120.1, 15, 0, 15, 240.1, None],
         [0, 120.1, 18, 0, 18, 240.1, None],
         [0, 120.1, 21, 0, 21, 240.1, None],
         [0, 120.1, 15, 0, 0, 240.1, None],
         [0, 120.1, 15, 0, 3, 240.1, None],
         [0, 120.1, 15, 0, 6, 240.1, None],
         [0, 120.1, 15, 0, 9, 240.1, None],
         [0, 120.1, 15, 0, 12, 240.1, None],
         [0, 120.1, 15, 0, 18, 240.1, None],
         [0, 120.1, 15, 0, 21, 240.1, None],
         [0, 120.1, 0, 0, 15, 240.1, None],
         [0, 120.1, 3, 0, 15, 240.1, None],
         [0, 120.1, 6, 0, 15, 240.1, None],
         [0, 120.1, 9, 0, 15, 240.1, None],
         [0, 120.1, 12, 0, 15, 240.1, None],
         [0, 120.1, 18, 0, 15, 240.1, None],
         [0, 120.1, 21, 0, 15, 240.1, None]]],
    [FREQUENCY_199, LEVEL_OFFSET_198_5, LEVEL_50_199, 7, KN32, MODULATION_256QAM, "PP2", CODE_RATE_2_3, GUARD_G1_8,
     25.1, [
         [0, 243.1, 0, 0, 0, 486.1, None],
         [0, 243.1, 3, 0, 3, 486.1, None],
         [0, 243.1, 6, 0, 6, 486.1, None],
         [0, 243.1, 9, 0, 9, 486.1, None],
         [0, 243.1, 12, 0, 12, 486.1, None],
         [0, 243.1, 15, 0, 15, 486.1, None],
         [0, 243.1, 18, 0, 18, 486.1, None],
         [0, 243.1, 21, 0, 21, 486.1, None],
         [0, 243.1, 15, 0, 0, 486.1, None],
         [0, 243.1, 15, 0, 3, 486.1, None],
         [0, 243.1, 15, 0, 6, 486.1, None],
         [0, 243.1, 15, 0, 9, 486.1, None],
         [0, 243.1, 15, 0, 12, 486.1, None],
         [0, 243.1, 15, 0, 18, 486.1, None],
         [0, 243.1, 15, 0, 21, 486.1, None],
         [0, 243.1, 0, 0, 15, 486.1, None],
         [0, 243.1, 3, 0, 15, 486.1, None],
         [0, 243.1, 6, 0, 15, 486.1, None],
         [0, 243.1, 9, 0, 15, 486.1, None],
         [0, 243.1, 12, 0, 15, 486.1, None],
         [0, 243.1, 18, 0, 15, 486.1, None],
         [0, 243.1, 21, 0, 15, 486.1, None]]]
]

my_file = Path("../../ekt_json/dvbt2_68_performance_in_SFN_echo.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    dict_test_parame_result["test_parame_result"] = PARAMETER_LIST
    write_json_file("../../ekt_json/dvbt2_68_performance_in_SFN_echo.json",
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
    load_dict = read_json_file("../../ekt_json/dvbt2_68_performance_in_SFN_echo.json")
    sfu_ip = "192.168.1.50"
    specan = Ektsfu(sfu_ip)
    specan.preset_instrument()
    specan = Ektsfu(sfu_ip)
    specan.set_modulation_modulation_source("DTV")
    specan = Ektsfu(sfu_ip)
    specan.set_modulation_modulation_standard_dvt("T2DVb")
    specan = Ektsfu(sfu_ip)
    specan.set_player_timing_openfile(r"E:\333\DIVER.GTS")
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_input_source_dvbt2("TSPLayer")
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

    LIST_PARAMETER_DATA = load_dict.get("test_parame_result")
    for PARAMETER_FIXED in LIST_PARAMETER_DATA:
        loop_lock_mark = False
        for FADING in PARAMETER_FIXED[10]:
            if FADING[6] == None:
                loop_lock_mark = True
                break
        if loop_lock_mark == True:
            pass
        else:
            continue

        specan = Ektsfu(sfu_ip)
        specan.set_frequency_frequency_frequency(str(int(PARAMETER_FIXED[0])) + "MHz")
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_offset(str(PARAMETER_FIXED[1]))
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_level("dBm", PARAMETER_FIXED[2])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_channelbandwidth_dvbt2("BW_{}".format(str(PARAMETER_FIXED[3])))

        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_fftsize_dvbt2(PARAMETER_FIXED[4])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_bicm_constellation_dvbt2(PARAMETER_FIXED[5])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_pilot_dvbt2(PARAMETER_FIXED[6])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_bicm_coderate_dvbt2(PARAMETER_FIXED[7])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_guard_dvbt2(PARAMETER_FIXED[8])

        # specan = Ektsfu(sfu_ip)
        # specan.set_fading_profile_additdelay("1", "2", "1.95E-6")

        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        net.send_data(
            json.dumps({"cmd": "set_frequency_data", "frequency": str(int(PARAMETER_FIXED[0]))}))
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
                                      "dvbt2_68_performance_in_SFN_echo: current_time:{}, frequency:{} MHz,bandwidth:{} Ksym/s, {}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          str(PARAMETER_FIXED[0]), str(PARAMETER_FIXED[3]),
                                          "Lock fail") + "\n"))
            continue
        else:
            write_test_result("../../ekt_log/test_result_sfu.txt", ("Lock state err" + "\n"))
            continue

        for FADING in PARAMETER_FIXED[10]:
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

            # specan = Ektsfu(sfu_ip)
            # specan.set_fading_profile_basicdelay("2", "{}E-6".format(str(PARAMETER[7])))

            res, test_result = iterate_to_find_threshold_noise_cn_step_by_step(sfu_ip, PARAMETER_FIXED[9])
            print(
                "dvbt2_68_performance_in_SFN_echo: current_time:{}, modulation: {} coderate:{}, frequency:{} MHz,bandwidth:{} MHZ,{}".format(
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), PARAMETER_FIXED[5],
                    PARAMETER_FIXED[7], str(PARAMETER_FIXED[0]), str(PARAMETER_FIXED[3]), res))
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              "dvbt2_68_performance_in_SFN_echo: current_time:{}, modulation: {} coderate:{}, frequency:{} MHz,bandwidth:{} MHZ,{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), PARAMETER_FIXED[5],
                                  PARAMETER_FIXED[7], str(PARAMETER_FIXED[0]), str(PARAMETER_FIXED[3]), res) + "\n")

            FADING[6] = test_result
            write_json_file("../../ekt_json/dvbt2_68_performance_in_SFN_echo.json", load_dict)
            dvbt2_68_performance_in_SFN_echo_json_to_csv(
                "../../ekt_json/dvbt2_68_performance_in_SFN_echo.json",
                "../../ekt_test_report/dvbt2_68_performance_in_SFN_echo.csv")

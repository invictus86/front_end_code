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
from ekt_lib.threshold_algorithm_SFU import iterate_to_find_threshold_fading_att_step_by_step
from ekt_lib.ekt_utils import write_test_result, write_json_file, read_json_file, find_level_offset_by_frequency, \
    dvbt_33_performance_SFN_outside_guard_json_to_csv

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
    [FREQUENCY_199, LEVEL_OFFSET_198_5, LEVEL_50_199, 7, FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8,
     [[0, 0, -298, None],
      [0, 0, -266, None],
      [0, 0, -256, None],
      [0, 0, -215, None],
      [0, 0, -165, None],
      [0, 0, -135, None],
      [0, 0, -128, None],
      [0, 0, 298, None],
      [0, 0, 266, None],
      [0, 0, 256, None],
      [0, 0, 215, None],
      [0, 0, 165, None],
      [0, 0, 135, None],
      [0, 0, 128, None]
      ]],
    [FREQUENCY_199, LEVEL_OFFSET_198_5, LEVEL_50_199, 7, FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_4,
     [[0, 0, -298, None],
      [0, 0, -266, None],
      [0, 0, -256, None],
      [0, 0, 298, None],
      [0, 0, 266, None],
      [0, 0, 256, None]
      ]],
    [FREQUENCY_199, LEVEL_OFFSET_198_5, LEVEL_50_199, 7, FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_3_4, GUARD_G1_4,
     [[0, 0, -298, None],
      [0, 0, -266, None],
      [0, 0, -256, None],
      [0, 0, 298, None],
      [0, 0, 266, None],
      [0, 0, 256, None]
      ]],

    [FREQUENCY_666, LEVEL_OFFSET_666, LEVEL_50_666, 8, FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8,
     [[0, 0, -260, None],
      [0, 0, -230, None],
      [0, 0, -200, None],
      [0, 0, -150, None],
      [0, 0, -120, None],
      [0, 0, 260, None],
      [0, 0, 230, None],
      [0, 0, 200, None],
      [0, 0, 150, None],
      [0, 0, 120, None]
      ]],
    [FREQUENCY_666, LEVEL_OFFSET_666, LEVEL_50_666, 8, FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_4,
     [[0, 0, -260, None],
      [0, 0, -230, None],
      [0, 0, 260, None],
      [0, 0, 230, None]
      ]],
    [FREQUENCY_666, LEVEL_OFFSET_666, LEVEL_50_666, 8, FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_3_4, GUARD_G1_4,
     [[0, 0, -260, None],
      [0, 0, -230, None],
      [0, 0, 260, None],
      [0, 0, 230, None]
      ]]
]

my_file = Path("../../ekt_json/dvbt_33_performance_SFN_outside_guard.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    dict_test_parame_result["test_parame_result"] = PARAMETER_LIST
    write_json_file("../../ekt_json/dvbt_33_performance_SFN_outside_guard.json",
                    dict_test_parame_result)

if __name__ == '__main__':
    """
    测试流程:
    ①重置设备
    ②选择 TSPLAYER
    ③播放流文件
    ④设置code_rate,modulation,bandwidth,guard, frequency,input_signal_level
    ⑤机顶盒应用中进行锁台并确认锁台成功  （针对stb-tester发送post请求运行testcase）
    ⑤依次修改可变参数,判断机顶盒画面是否含有马赛克并记录结果
    """
    load_dict = read_json_file("../../ekt_json/dvbt_33_performance_SFN_outside_guard.json")
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
    specan.set_fading_profile_state("2", "1", "ON")
    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_state("3", "1", "ON")

    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_profile("2", "1", "SPATh")
    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_profile("3", "1", "SPATh")

    for PARAMETER in load_dict.get("test_parame_result"):
        loop_lock_mark = False
        for DELAY in PARAMETER[8]:
            if DELAY[3] == None:
                loop_lock_mark = True
                break
        if loop_lock_mark == True:
            pass
        else:
            continue

        specan = Ektsfu(sfu_ip)
        specan.set_frequency_frequency_frequency(str(PARAMETER[0]) + "MHz")
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_channelbandwidth_dvbt("BW_{}".format(str(PARAMETER[3])))
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_offset(str(PARAMETER[1]))
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_level("dBm", str(PARAMETER[2]))

        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_fftmode_dvbt(PARAMETER[4])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_constellation_dvbt(PARAMETER[5])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_coderate_dvbt(PARAMETER[6])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_guard_dvbt(PARAMETER[7])

        specan = Ektsfu(sfu_ip)
        specan.set_fading_profile_pathloss("2", "1", "{} dB".format(str(0)))

        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": str(int(PARAMETER[0]))}))
        time.sleep(1)
        del net
        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        net.send_data(json.dumps({"cmd": "set_bandwidth_data", "bandwidth": str(PARAMETER[3])}))
        time.sleep(1)
        del net
        """
        触发stb-tester进行频率和符号率设置
        """
        stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                    ekt_cfg.DVB_T_LOCK_FUNCTION, ekt_cfg.DVB_T_CATEGORY, ekt_cfg.DVB_T_REMOTE)
        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
        if lock_state == "1":
            pass
        elif lock_state == "0":
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              (
                                      "dvbt_33_performance_SFN_outside_guard: current_time:{}, frequency:{} MHz,bandwidth:{} Ksym/s, {}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          str(PARAMETER[0]), str(PARAMETER[3]), "Lock fail") + "\n"))
            continue
        else:
            write_test_result("../../ekt_log/test_result_sfu.txt", ("Lock state err" + "\n"))
            continue

        for DELAY in PARAMETER[8]:
            if DELAY[3] == None:
                pass
            else:
                continue

            if DELAY[2] < 0:
                main_delay = abs(DELAY[2])
                per_delay = 0
            else:
                main_delay = DELAY[1]
                per_delay = DELAY[2]

            specan = Ektsfu(sfu_ip)
            specan.set_fading_profile_basicdelay("2", "{}E-6".format(str(main_delay)))
            time.sleep(1)
            specan = Ektsfu(sfu_ip)
            specan.set_fading_profile_basicdelay("3", "{}E-6".format(str(per_delay)))
            time.sleep(1)

            specan = Ektsfu(sfu_ip)
            specan.set_fading_profile_pathloss("3", "1", "{} dB".format(str(DELAY[0])))
            time.sleep(1)

            res, test_result = iterate_to_find_threshold_fading_att_step_by_step(sfu_ip, 16)
            print(
                "dvbt_33_performance_SFN_outside_guard: current_time:{}, modulation: {} coderate:{}, frequency:{} MHz,bandwidth:{} MHZ,{}".format(
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), PARAMETER[5],
                    PARAMETER[6], str(PARAMETER[0]), str(PARAMETER[3]), res))
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              "dvbt_33_performance_SFN_outside_guard: current_time:{}, modulation: {} coderate:{}, frequency:{} MHz,bandwidth:{} MHZ,{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), PARAMETER[5],
                                  PARAMETER[6], str(PARAMETER[0]), str(PARAMETER[3]), res) + "\n")

            DELAY[3] = test_result
            write_json_file("../../ekt_json/dvbt_33_performance_SFN_outside_guard.json", load_dict)
            dvbt_33_performance_SFN_outside_guard_json_to_csv(
                "../../ekt_json/dvbt_33_performance_SFN_outside_guard.json",
                "../../ekt_test_report/dvbt_33_performance_SFN_outside_guard.csv")

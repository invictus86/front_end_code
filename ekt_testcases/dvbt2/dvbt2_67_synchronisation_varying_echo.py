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
    dvbt2_67_synchronisation_varying_echo_json_to_csv

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
    [FREQUENCY_666, LEVEL_OFFSET_666, LEVEL_50_666, 8, [
        [KE32, MODULATION_256QAM, "PP7", CODE_RATE_2_3, GUARD_G1_128, 8, 28.1, 10, None],
        [KE32, MODULATION_256QAM, "PP7", CODE_RATE_2_3, GUARD_G1_128, 8, 28.1, 26, None],

        [KE32, MODULATION_256QAM, "PP4", CODE_RATE_2_3, GUARD_G1_16, 8, 28.1, 10, None],
        [KE32, MODULATION_256QAM, "PP4", CODE_RATE_2_3, GUARD_G1_16, 8, 28.1, 26, None],
        [KE32, MODULATION_256QAM, "PP4", CODE_RATE_2_3, GUARD_G1_16, 8, 28.1, 112.1, None],
        [KE32, MODULATION_256QAM, "PP4", CODE_RATE_2_3, GUARD_G1_16, 8, 28.1, 133, None],
        [KE32, MODULATION_256QAM, "PP4", CODE_RATE_2_3, GUARD_G1_16, 8, 28.1, 152, None],
        [KE32, MODULATION_256QAM, "PP4", CODE_RATE_2_3, GUARD_G1_16, 8, 28.1, 212, None],

        [KE32, MODULATION_256QAM, "PP4", CODE_RATE_3_5, GUARD_G19_256, 8, 26.1, 10, None],
        [KE32, MODULATION_256QAM, "PP4", CODE_RATE_3_5, GUARD_G19_256, 8, 26.1, 26, None],
        [KE32, MODULATION_256QAM, "PP4", CODE_RATE_3_5, GUARD_G19_256, 8, 26.1, 112.1, None],
        [KE32, MODULATION_256QAM, "PP4", CODE_RATE_3_5, GUARD_G19_256, 8, 26.1, 133, None],
        [KE32, MODULATION_256QAM, "PP4", CODE_RATE_3_5, GUARD_G19_256, 8, 26.1, 152, None],
        [KE32, MODULATION_256QAM, "PP4", CODE_RATE_3_5, GUARD_G19_256, 8, 26.1, 212, None],
        [KE32, MODULATION_256QAM, "PP4", CODE_RATE_3_5, GUARD_G19_256, 8, 26.1, 253, None],

        [KE32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 8, 31, 10, None],
        [KE32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 8, 31, 26, None],
        [KE32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 8, 31, 112.1, None],
        [KE32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 8, 31, 133, None],
        [KE32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 8, 31, 152, None],
        [KE32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 8, 31, 212, None],
        [KE32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 8, 31, 253, None],
        [KE32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 8, 31, 256, None],
        [KE32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 8, 31, 289, None],
        [KE32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 8, 31, 426, None]]],
    [FREQUENCY_199, LEVEL_OFFSET_198_5, LEVEL_50_199, 7,
     [[KN32, MODULATION_256QAM, "PP4", CODE_RATE_2_3, GUARD_G19_256, 7, 28.1, 10, None],
      [KN32, MODULATION_256QAM, "PP4", CODE_RATE_2_3, GUARD_G19_256, 7, 28.1, 26, None],
      [KN32, MODULATION_256QAM, "PP4", CODE_RATE_2_3, GUARD_G19_256, 7, 28.1, 112.1, None],
      [KN32, MODULATION_256QAM, "PP4", CODE_RATE_2_3, GUARD_G19_256, 7, 28.1, 133, None],
      [KN32, MODULATION_256QAM, "PP4", CODE_RATE_2_3, GUARD_G19_256, 7, 28.1, 152, None],
      [KN32, MODULATION_256QAM, "PP4", CODE_RATE_2_3, GUARD_G19_256, 7, 28.1, 212, None],
      [KN32, MODULATION_256QAM, "PP4", CODE_RATE_2_3, GUARD_G19_256, 7, 28.1, 253, None],
      [KN32, MODULATION_256QAM, "PP4", CODE_RATE_2_3, GUARD_G19_256, 7, 28.1, 256, None],
      [KN32, MODULATION_256QAM, "PP4", CODE_RATE_2_3, GUARD_G19_256, 7, 28.1, 289, None],

      [KN32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 7, 31, 10, None],
      [KN32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 7, 31, 26, None],
      [KN32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 7, 31, 112.1, None],
      [KN32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 7, 31, 133, None],
      [KN32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 7, 31, 152, None],
      [KN32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 7, 31, 212, None],
      [KN32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 7, 31, 253, None],
      [KN32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 7, 31, 256, None],
      [KN32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 7, 31, 289, None],
      [KN32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 7, 31, 426, None],
      [KN32, MODULATION_256QAM, "PP2", CODE_RATE_3_4, GUARD_G1_8, 7, 31, 486, None]
      ]]
]

my_file = Path("../../ekt_json/dvbt2_67_synchronisation_varying_echo.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    dict_test_parame_result["test_parame_result"] = PARAMETER_LIST
    write_json_file("../../ekt_json/dvbt2_67_synchronisation_varying_echo.json",
                    dict_test_parame_result)

# 32KN 256QAM PP4 R2/3 G19/256 7M                     frame length set to 55

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
    load_dict = read_json_file("../../ekt_json/dvbt2_67_synchronisation_varying_echo.json")
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
    specan.set_fading_profile_state("1", "1", "ON")
    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_state("2", "1", "ON")

    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_profile("1", "1", "SPATh")
    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_profile("2", "1", "SPATh")

    LIST_PARAMETER_DATA = load_dict.get("test_parame_result")
    for PARAMETER_FIXED in LIST_PARAMETER_DATA:
        loop_lock_mark = False
        for PARAMETER in PARAMETER_FIXED[4]:
            if PARAMETER[8] == None:
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
                                    ekt_cfg.DVB_T2_LOCK_FUNCTION, ekt_cfg.DVB_T2_CATEGORY, ekt_cfg.DVB_T2_REMOTE)
        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
        if lock_state == "1":
            pass
        elif lock_state == "0":
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              (
                                      "dvbt2_67_synchronisation_varying_echo: current_time:{}, frequency:{} MHz,bandwidth:{} Ksym/s, {}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          str(PARAMETER_FIXED[0]), str(PARAMETER_FIXED[3]),
                                          "Lock fail") + "\n"))
            continue
        else:
            write_test_result("../../ekt_log/test_result_sfu.txt", ("Lock state err" + "\n"))
            continue

        for PARAMETER in PARAMETER_FIXED[4]:
            if PARAMETER[8] == None:
                pass
            else:
                continue
            # 待确认设置项是否正确
            if PARAMETER[3] == CODE_RATE_2_3 and PARAMETER[4] == GUARD_G19_256:
                specan = Ektsfu(sfu_ip)
                specan.set_digitaltv_system_papr_dvbt2("TR")
                specan = Ektsfu(sfu_ip)
                specan.set_digitaltv_framing_ldata_dvbt2("54")
            else:
                specan = Ektsfu(sfu_ip)
                specan.set_digitaltv_system_papr_dvbt2("OFF")


            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_framing_fftsize_dvbt2(PARAMETER[0])
            time.sleep(1)
            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_bicm_constellation_dvbt2(PARAMETER[1])
            time.sleep(1)
            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_framing_pilot_dvbt2(PARAMETER[2])
            time.sleep(1)
            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_bicm_coderate_dvbt2(PARAMETER[3])
            time.sleep(1)
            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_framing_guard_dvbt2(PARAMETER[4])
            time.sleep(1)
            specan = Ektsfu(sfu_ip)
            specan.set_fading_profile_basicdelay("2", "{}E-6".format(str(PARAMETER[7])))
            time.sleep(1)

            res, test_result = iterate_to_find_threshold_noise_cn_step_by_step(sfu_ip, PARAMETER[6])
            print(
                "dvbt2_67_synchronisation_varying_echo: current_time:{}, modulation: {} coderate:{}, frequency:{} MHz,bandwidth:{} MHZ,{}".format(
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), PARAMETER[1],
                    PARAMETER[2], str(FREQUENCY_666), str(8), res))
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              "dvbt2_67_synchronisation_varying_echo: current_time:{}, modulation: {} coderate:{}, frequency:{} MHz,bandwidth:{} MHZ,{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), PARAMETER[1],
                                  PARAMETER[2], str(FREQUENCY_666), str(8), res) + "\n")

            PARAMETER[8] = test_result
            write_json_file("../../ekt_json/dvbt2_67_synchronisation_varying_echo.json", load_dict)
            dvbt2_67_synchronisation_varying_echo_json_to_csv(
                "../../ekt_json/dvbt2_67_synchronisation_varying_echo.json",
                "../../ekt_test_report/dvbt2_67_synchronisation_varying_echo.csv")

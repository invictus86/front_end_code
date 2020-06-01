#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import datetime
from ekt_lib import ekt_net, ekt_cfg
from ekt_lib.ekt_sfu import Ektsfu
from pathlib2 import Path
from ekt_lib.ekt_stb_tester import stb_tester_execute_testcase
from ekt_lib.threshold_algorithm_SFU import mosaic_algorithm
from ekt_lib.ekt_utils import write_test_result, find_level_offset_by_frequency, write_json_file, read_json_file, \
    dvbt2_53_changes_modulation_parameters_to_csv

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

FFT_SIZE_1K = "M1K"
FFT_SIZE_2K = "M2K"
FFT_SIZE_4K = "M4K"
FFT_SIZE_8K = "M8K"
FFT_SIZE_16K = "M16K"
# FFT_SIZE_32K = "M32K"
FFT_SIZE_32KE = "M32E"

KE32 = "M32E"
KN32 = "M32K"

FREQUENCY_666 = 666
LEVEL_OFFSET_666 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", 666.0)
LEVEL_50_666 = str("%.2f" % (-50 - LEVEL_OFFSET_666))

PARAMETER_LIST = [
    [FFT_SIZE_32KE, MODULATION_256QAM, 'PP4', CODE_RATE_2_3, GUARD_G1_16, 8, 62, None],
    [FFT_SIZE_16K, MODULATION_256QAM, 'PP4', CODE_RATE_2_3, GUARD_G1_16, 8, 62, None],
    [FFT_SIZE_8K, MODULATION_256QAM, 'PP4', CODE_RATE_2_3, GUARD_G1_16, 8, 62, None],
    [FFT_SIZE_4K, MODULATION_256QAM, 'PP4', CODE_RATE_2_3, GUARD_G1_16, 8, 62, None],
    [FFT_SIZE_2K, MODULATION_256QAM, 'PP4', CODE_RATE_2_3, GUARD_G1_16, 8, 62, None],
    [FFT_SIZE_1K, MODULATION_256QAM, 'PP4', CODE_RATE_2_3, GUARD_G1_16, 8, 62, None],

    [FFT_SIZE_32KE, MODULATION_256QAM, 'PP4', CODE_RATE_2_3, GUARD_G1_32, 8, 62, None],
    [FFT_SIZE_32KE, MODULATION_256QAM, 'PP4', CODE_RATE_2_3, GUARD_G1_16, 8, 62, None],
    [FFT_SIZE_32KE, MODULATION_256QAM, 'PP4', CODE_RATE_2_3, GUARD_G1_8, 8, 62, None],
    [FFT_SIZE_32KE, MODULATION_256QAM, 'PP4', CODE_RATE_2_3, GUARD_G1_4, 8, 62, None],
    [FFT_SIZE_32KE, MODULATION_256QAM, 'PP4', CODE_RATE_2_3, GUARD_G1_128, 8, 62, None],
    [FFT_SIZE_32KE, MODULATION_256QAM, 'PP4', CODE_RATE_2_3, GUARD_G19_128, 8, 62, None],
    [FFT_SIZE_32KE, MODULATION_256QAM, 'PP4', CODE_RATE_2_3, GUARD_G19_256, 8, 62, None],

    [FFT_SIZE_32KE, MODULATION_256QAM, 'PP2', CODE_RATE_2_3, GUARD_G1_16, 8, 62, None],
    [FFT_SIZE_32KE, MODULATION_256QAM, 'PP4', CODE_RATE_2_3, GUARD_G1_16, 8, 62, None],
    [FFT_SIZE_32KE, MODULATION_256QAM, 'PP6', CODE_RATE_2_3, GUARD_G1_16, 8, 62, None],
    [FFT_SIZE_32KE, MODULATION_256QAM, 'PP7', CODE_RATE_2_3, GUARD_G1_16, 8, 62, None],

    [FFT_SIZE_32KE, MODULATION_256QAM, 'PP2', CODE_RATE_2_3, GUARD_G1_16, 8, 60, None],
    [FFT_SIZE_32KE, MODULATION_256QAM, 'PP2', CODE_RATE_2_3, GUARD_G1_16, 8, 62, None],

    [FFT_SIZE_32KE, MODULATION_256QAM, 'PP4', CODE_RATE_3_5, GUARD_G1_16, 8, 62, None],
    [FFT_SIZE_32KE, MODULATION_256QAM, 'PP4', CODE_RATE_2_3, GUARD_G1_16, 8, 62, None],
    [FFT_SIZE_32KE, MODULATION_256QAM, 'PP4', CODE_RATE_3_4, GUARD_G1_16, 8, 62, None],
]

# 未设置change BW extension 、 change PAPR

my_file = Path("../../ekt_json/dvbt2_53_changes_modulation_parameters.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    list_test_parame_result = []

    for PARAMETER in PARAMETER_LIST:
        list_test_parame_result.append(
            [PARAMETER[0], PARAMETER[1], PARAMETER[2], PARAMETER[3], PARAMETER[4], PARAMETER[5], PARAMETER[6], PARAMETER[7]])

    dict_test_parame_result["test_parame_result"] = list_test_parame_result

    write_json_file("../../ekt_json/dvbt2_53_changes_modulation_parameters.json",
                    dict_test_parame_result)

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
    load_dict = read_json_file("../../ekt_json/dvbt2_53_changes_modulation_parameters.json")
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
    specan.set_noise_noise_noise("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_fading_fading_state("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_modulator("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_baseband("OFF")

    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_system_papr_dvbt2("TR")

    specan = Ektsfu(sfu_ip)
    specan.set_frequency_frequency_frequency(str(int(FREQUENCY_666)) + "MHz")
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_framing_channelbandwidth_dvbt2("BW_{}".format(str(8)))
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_offset(str(LEVEL_OFFSET_666))
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_level("dBm", LEVEL_50_666)

    net = ekt_net.EktNetClient('192.168.1.24', 9999)
    net.send_data(
        json.dumps({"cmd": "set_frequency_data", "frequency": str(int(FREQUENCY_666))}))
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
                                  "dvbt2_53_changes_modulation_parameters: current_time:{}, frequency：{} MHz，bandwidth：{} Ksym/s, {}".format(
                                      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                      str(FREQUENCY_666), str(8),
                                      "锁台失败") + "\n"))
    else:
        write_test_result("../../ekt_log/test_result_sfu.txt", ("出错了" + "\n"))

    for PARAMETER in load_dict.get("test_parame_result"):
        if PARAMETER[7] == None:
            pass
        else:
            continue
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_fftsize_dvbt2(PARAMETER[0])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_bicm_constellation_dvbt2(PARAMETER[1])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_pilot_dvbt2(PARAMETER[2])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_bicm_coderate_dvbt2(PARAMETER[3])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_guard_dvbt2(PARAMETER[4])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_ldata_dvbt2(str(PARAMETER[6]))
        time.sleep(5)

        start_data_result, test_result = mosaic_algorithm(sfu_ip, LEVEL_50_666, LEVEL_50_666)
        print (
            "dvbt_5_frequency_offset: current_time:{}, modulation: {},coderate：{}, frequency：{} MHz，bandwidth：{} MHZ，{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), PARAMETER[1],
                PARAMETER[3], str(FREQUENCY_666), str(8), start_data_result.get("detect_mosic_result")))
        write_test_result("../../ekt_log/test_result_sfu.txt",
                          "dvbt_5_frequency_offset: current_time:{}, modulation: {},coderate：{}, frequency：{} MHz，bandwidth：{} MHZ，{}".format(
                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), PARAMETER[1],
                              PARAMETER[3], str(FREQUENCY_666), str(8),
                              start_data_result.get("detect_mosic_result")) + "\n")
        PARAMETER[7] = test_result
        write_json_file(
            "../../ekt_json/dvbt2_53_changes_modulation_parameters.json", load_dict)
        dvbt2_53_changes_modulation_parameters_to_csv(
            "../../ekt_json/dvbt2_53_changes_modulation_parameters.json",
            "../../ekt_test_report/dvbt2_53_changes_modulation_parameters.csv")

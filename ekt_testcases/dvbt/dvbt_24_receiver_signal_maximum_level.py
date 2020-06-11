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
from ekt_lib.threshold_algorithm_SFU import mosaic_algorithm
from ekt_lib.ekt_utils import write_test_result, write_json_file, read_json_file, find_level_offset_by_frequency, \
    dvbt_24_receiver_maximum_level_to_csv

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
LEVEL_30_666 = str("%.2f" % (-30 - LEVEL_OFFSET_666))

PARAMETER_LIST = [
    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, -35, None],
    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_4, -35, None],
    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_3_4, GUARD_G1_4, -35, None],
]

my_file = Path("../../ekt_json/dvbt_24_receiver_signal_maximum_level.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    dict_test_parame_result["test_parame_result"] = PARAMETER_LIST
    write_json_file("../../ekt_json/dvbt_24_receiver_signal_maximum_level.json",
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
    load_dict = read_json_file("../../ekt_json/dvbt_24_receiver_signal_maximum_level.json")
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
    specan = Ektsfu(sfu_ip)
    specan.set_fading_fading_state("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_modulator("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_baseband("OFF")

    specan = Ektsfu(sfu_ip)
    specan.set_frequency_frequency_frequency(str(int(FREQUENCY_666)) + "MHz")
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_coding_channelbandwidth_dvbt("BW_{}".format(str(8)))
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_offset(str(LEVEL_OFFSET_666))
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_level("dBm", LEVEL_30_666)

    net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
    net.send_data(
        json.dumps({"cmd": "set_frequency_data", "frequency": str(int(FREQUENCY_666))}))
    time.sleep(1)
    del net
    net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
    net.send_data(json.dumps({"cmd": "set_bandwidth_data", "bandwidth": str(8)}))
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
                                  "dvbt_21_receiver_signal_input__min_level: current_time:{}, frequency:{} MHz,bandwidth:{} Ksym/s, {}".format(
                                      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                      str(FREQUENCY_666),
                                      str(8), "Lock fail") + "\n"))
    else:
        write_test_result("../../ekt_log/test_result_sfu.txt", ("Lock state err" + "\n"))

    for PARAMETER in load_dict.get("test_parame_result"):
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_fftmode_dvbt(PARAMETER[0])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_constellation_dvbt(PARAMETER[1])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_coderate_dvbt(PARAMETER[2])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_guard_dvbt(PARAMETER[3])

        start_data_result = mosaic_algorithm(sfu_ip, LEVEL_30_666, LEVEL_30_666)
        print (
            "dvbt_5_frequency_offset: current_time:{}, modulation: {},coderate:{}, frequency:{} MHz,bandwidth:{} MHZ,{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), PARAMETER[1],
                PARAMETER[2], str(FREQUENCY_666), str(8), start_data_result.get("detect_mosic_result")))
        write_test_result("../../ekt_log/test_result_sfu.txt",
                          "dvbt_5_frequency_offset: current_time:{}, modulation: {},coderate:{}, frequency:{} MHz,bandwidth:{} MHZ,{}".format(
                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), PARAMETER[1],
                              PARAMETER[2], str(FREQUENCY_666), str(8),
                              start_data_result.get("detect_mosic_result")) + "\n")
        PARAMETER[5] = start_data_result.get("detect_mosic_result")
        write_json_file(
            "../../ekt_json/dvbt_24_receiver_signal_maximum_level.json", load_dict)
        dvbt_24_receiver_maximum_level_to_csv(
            "../../ekt_json/dvbt_24_receiver_signal_maximum_level.json",
            "../../ekt_test_report/dvbt_24_receiver_signal_maximum_level.csv")

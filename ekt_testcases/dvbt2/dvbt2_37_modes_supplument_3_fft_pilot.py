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
from ekt_lib.ekt_utils import write_test_result, find_level_offset_by_frequency, write_json_file, read_json_file, \
    dvbt2_37_modes_supplument_3_fft_pilot_json_to_csv, get_ldata_from_lf_fftsize

FREQUENCY_666 = 666.0

LEVEL_OFFSET_666 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", FREQUENCY_666)
LEVEL_50 = str("%.2f" % (-50 - LEVEL_OFFSET_666))

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

FFTSIZE_PIL_LEVEL_GUARD_LIST = [
    [MODULATION_64QAM, CODE_RATE_2_3, "M1K", "PP2", 90, GUARD_G1_8, None],
    [MODULATION_64QAM, CODE_RATE_2_3, "M2K", "PP2", 90, GUARD_G1_8, None],
    [MODULATION_64QAM, CODE_RATE_2_3, "M4K", "PP2", 90, GUARD_G1_8, None],
    [MODULATION_64QAM, CODE_RATE_2_3, "M8K", "PP2", 90, GUARD_G1_8, None],
    [MODULATION_64QAM, CODE_RATE_2_3, "M8E", "PP2", 90, GUARD_G1_8, None],
    [MODULATION_256QAM, CODE_RATE_2_3, "M16K", "PP2", 90, GUARD_G1_8, None],
    [MODULATION_256QAM, CODE_RATE_2_3, "M16E", "PP2", 90, GUARD_G1_8, None],
    [MODULATION_256QAM, CODE_RATE_2_3, "M32K", "PP2", 60, GUARD_G1_8, None],
    [MODULATION_256QAM, CODE_RATE_2_3, "M32E", "PP2", 60, GUARD_G1_8, None],

    [MODULATION_256QAM, CODE_RATE_2_3, "M16K", "PP1", 90, GUARD_G1_4, None],
    [MODULATION_256QAM, CODE_RATE_3_4, "M32K", "PP2", 60, GUARD_G1_8, None],
    [MODULATION_256QAM, CODE_RATE_2_3, "M16K", "PP3", 90, GUARD_G1_8, None],
    [MODULATION_256QAM, CODE_RATE_2_3, "M32K", "PP4", 62, GUARD_G1_16, None],
    [MODULATION_256QAM, CODE_RATE_2_3, "M16K", "PP5", 90, GUARD_G1_16, None],
    [MODULATION_256QAM, CODE_RATE_3_4, "M32K", "PP6", 62, GUARD_G1_32, None],
    [MODULATION_256QAM, CODE_RATE_3_4, "M32K", "PP7", 60, GUARD_G1_128, None],
    [MODULATION_256QAM, CODE_RATE_3_4, "M32K", "PP8", 62, GUARD_G1_16, None]
]

my_file = Path("../../ekt_json/dvbt2_37_modes_supplument_3_fft_pilot.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    dict_test_parame_result["test_parame_result"] = FFTSIZE_PIL_LEVEL_GUARD_LIST
    write_json_file("../../ekt_json/dvbt2_37_modes_supplument_3_fft_pilot.json", dict_test_parame_result)

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
    load_dict = read_json_file("../../ekt_json/dvbt2_37_modes_supplument_3_fft_pilot.json")
    sfu_ip = ekt_cfg.SFU_IP
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
    specan.set_frequency_frequency_frequency(str(FREQUENCY_666) + "MHz")
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_framing_channelbandwidth_dvbt2("BW_{}".format(str("8")))
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_offset(str(LEVEL_OFFSET_666))
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_level("dBm", LEVEL_50)
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_system_papr_dvbt2("TR")
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_framing_ldata_dvbt2("45")

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
                                ekt_cfg.DVB_T2_LOCK_FUNCTION, ekt_cfg.DVB_T2_CATEGORY, ekt_cfg.DVB_T2_REMOTE)
    net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
    lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
    if lock_state == "1":
        pass
    elif lock_state == "0":
        write_test_result("../../ekt_log/test_result_sfu.txt",
                          (
                                  "dvbt2_37_modes_supplument_3_fft_pilot: current_time:{}, frequency:{} MHz,bandwidth:{} Ksym/s, {}".format(
                                      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                      str(FREQUENCY_666), str(8), "Lock fail") + "\n"))
    else:
        write_test_result("../../ekt_log/test_result_sfu.txt", ("Lock state err" + "\n"))

    for PARAME in load_dict.get("test_parame_result"):
        if PARAME[6] == None:
            pass
        else:
            continue

        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_bicm_constellation_dvbt2(PARAME[0])
        time.sleep(1)
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_bicm_coderate_dvbt2(PARAME[1])
        time.sleep(1)
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_fftsize_dvbt2(PARAME[2])
        time.sleep(1)
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_pilot_dvbt2(PARAME[3])
        time.sleep(1)

        ldata = get_ldata_from_lf_fftsize(PARAME[4], PARAME[2])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_ldata_dvbt2(str(ldata))
        time.sleep(1)
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_guard_dvbt2(PARAME[5])
        time.sleep(1)

        start_data_result, mosaic_result = mosaic_algorithm(sfu_ip, float(LEVEL_50), float(LEVEL_50))
        print (
            "dvbt2_37_modes_supplument_3_fft_pilot: current_time:{}, fft_size: {}, modulation: {},coderate:{}, PIL:{}, guard:{}, frequency:{} MHz,bandwidth:{} MHZ,{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), PARAME[3], PARAME[0],
                PARAME[1], PARAME[2], PARAME[5], FREQUENCY_666, str("8"), start_data_result.get("detect_mosic_result")))
        write_test_result("../../ekt_log/test_result_sfu.txt",
                          "dvbt2_37_modes_supplument_3_fft_pilot: current_time:{}, fft_size: {}, modulation: {},coderate:{}, PIL:{}, guard:{}, frequency:{} MHz,bandwidth:{} MHZ,{}".format(
                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), PARAME[3], PARAME[0],
                              PARAME[1], PARAME[2], PARAME[5], FREQUENCY_666, str("8"),
                              start_data_result.get("detect_mosic_result")) + "\n")
        PARAME[6] = mosaic_result
        write_json_file("../../ekt_json/dvbt2_37_modes_supplument_3_fft_pilot.json", load_dict)
        dvbt2_37_modes_supplument_3_fft_pilot_json_to_csv(
            "../../ekt_json/dvbt2_37_modes_supplument_3_fft_pilot.json", "../../ekt_test_report/dvbt2_37_modes_supplument_3_fft_pilot.csv")

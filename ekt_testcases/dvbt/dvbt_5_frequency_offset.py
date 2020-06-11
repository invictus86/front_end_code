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
from ekt_lib.ekt_utils import write_test_result, write_json_file, read_json_file, dvbt_5_frequency_offset_json_to_csv

MODULATION_64QAM = "T64"
FFT_SIZE_8K = "M8K"
CODE_RATE_2_3 = "R2_3"
GUARD_G1_8 = "G1_8"
LEVEL_60 = "-60"

FREQUENCY_BW_OFFSET_LIST = [
    [177, 7, -0.05, None],
    [177, 7, 0, None],
    [177, 7, +0.05, None],
    [226, 7, -0.05, None],
    [226, 7, 0, None],
    [226, 7, +0.05, None],
    [474, 8, -0.05, None],
    [474, 8, 0, None],
    [474, 8, +0.05, None],
    [858, 8, -0.05, None],
    [858, 8, 0, None],
    [858, 8, +0.05, None]]

my_file = Path("../../ekt_json/dvbt_5_frequency_offset.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    dict_test_parame_result["test_parame_result"] = FREQUENCY_BW_OFFSET_LIST
    write_json_file("../../ekt_json/dvbt_5_frequency_offset.json", dict_test_parame_result)
    
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
    load_dict = read_json_file("../../ekt_json/dvbt_5_frequency_offset.json")
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
    specan.set_digitaltv_coding_constellation_dvbt(MODULATION_64QAM)
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_coding_fftmode_dvbt(FFT_SIZE_8K)
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_coding_coderate_dvbt(CODE_RATE_2_3)
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_coding_guard_dvbt(GUARD_G1_8)

    for FREQUENCY_BW in load_dict.get("test_parame_result"):
        if FREQUENCY_BW[3] == None:
            pass
        else:
            continue
        specan = Ektsfu(sfu_ip)
        specan.set_frequency_frequency_frequency(str(int(FREQUENCY_BW[0]) + FREQUENCY_BW[2]) + "MHz")
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_channelbandwidth_dvbt("BW_{}".format(str(FREQUENCY_BW[1])))
        specan = Ektsfu(sfu_ip)
        # specan.set_level_level_offset(str(FREQUENCY_LEVEL_OFFSET[1]))
        # specan = Ektsfu(sfu_ip)
        specan.set_level_level_level("dBm", "-60")

        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        net.send_data(
            json.dumps({"cmd": "set_frequency_data", "frequency": str(int(FREQUENCY_BW[0]))}))
        time.sleep(1)
        del net
        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        net.send_data(json.dumps({"cmd": "set_bandwidth_data", "bandwidth": str(FREQUENCY_BW[1])}))
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
                                      "dvbt_5_frequency_offset: current_time:{}, frequency:{} MHz,stb_frequency:{} MHz,bandwidth:{} Ksym/s, {}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          str(FREQUENCY_BW[0]), str(int(FREQUENCY_BW[0] + FREQUENCY_BW[2])),
                                          str(FREQUENCY_BW[1]),
                                          "Lock fail") + "\n"))
            continue
        else:
            write_test_result("../../ekt_log/test_result_sfu.txt", ("Lock state err" + "\n"))
            continue

        start_data_result, mosaic_result = mosaic_algorithm(sfu_ip, "-60", "-60")
        print ("dvbt_5_frequency_offset: current_time:{}, modulation: {},coderate:{}, frequency:{} MHz,stb_frequency:{} MHz,bandwidth:{} MHZ,{}".format(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), MODULATION_64QAM,
            CODE_RATE_2_3, str(FREQUENCY_BW[0] + FREQUENCY_BW[2]), str(int(FREQUENCY_BW[0])), str(FREQUENCY_BW[1]),
            start_data_result.get("detect_mosic_result")))
        write_test_result("../../ekt_log/test_result_sfu.txt",
                          "dvbt_5_frequency_offset: current_time:{}, modulation: {}, coderate:{}, frequency:{} MHz,stb_frequency:{} MHz,bandwidth:{} MHZ,{}".format(
                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                              MODULATION_64QAM, CODE_RATE_2_3, str(FREQUENCY_BW[0] + FREQUENCY_BW[2]),
                              str(int(FREQUENCY_BW[0])), str(FREQUENCY_BW[1]),
                              start_data_result.get("detect_mosic_result")) + "\n")
        FREQUENCY_BW[3] = mosaic_result
        write_json_file("../../ekt_json/dvbt_5_frequency_offset.json", load_dict)
        dvbt_5_frequency_offset_json_to_csv(
            "../../ekt_json/dvbt_5_frequency_offset.json",
            "../../ekt_test_report/dvbt_5_frequency_offset.csv")

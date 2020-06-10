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
from ekt_lib.ekt_utils import write_test_result, write_json_file, read_json_file, dvbt2_34_centre_frequencies_json_to_csv

MODULATION_64QAM = "T64"
FFT_SIZE_8K = "M8K"
CODE_RATE_2_3 = "R2_3"
GUARD_G1_8 = "G1_8"
LEVEL_60 = "-60"

FREQUENCY_BW_LIST = [
    [177.5, 7, None],
    [184.5, 7, None],
    [191.5, 7, None],
    [198.5, 7, None],
    [205.5, 7, None],
    [212.5, 7, None],
    [219.5, 7, None],
    [226.5, 7, None],
    [474.0, 8, None],
    [482.0, 8, None],
    [490.0, 8, None],
    [498.0, 8, None],
    [506.0, 8, None],
    [514.0, 8, None],
    [522.0, 8, None],
    [530.0, 8, None],
    [538.0, 8, None],
    [546.0, 8, None],
    [554.0, 8, None],
    [562.0, 8, None],
    [570.0, 8, None],
    [578.0, 8, None],
    [586.0, 8, None],
    [594.0, 8, None],
    [602.0, 8, None],
    [610.0, 8, None],
    [618.0, 8, None],
    [626.0, 8, None],
    [634.0, 8, None],
    [642.0, 8, None],
    [650.0, 8, None],
    [658.0, 8, None],
    [666.0, 8, None],
    [674.0, 8, None],
    [682.0, 8, None],
    [690.0, 8, None],
    [698.0, 8, None],
    [706.0, 8, None],
    [714.0, 8, None],
    [722.0, 8, None],
    [730.0, 8, None],
    [738.0, 8, None],
    [746.0, 8, None],
    [754.0, 8, None],
    [762.0, 8, None],
    [770.0, 8, None],
    [778.0, 8, None],
    [786.0, 8, None],
    [794.0, 8, None],
    [802.0, 8, None],
    [810.0, 8, None],
    [818.0, 8, None],
    [826.0, 8, None],
    [834.0, 8, None],
    [842.0, 8, None],
    [850.0, 8, None],
    [858.0, 8, None],
    [114.5, 7, None],
    [121.5, 7, None],
    [128.5, 7, None],
    [135.5, 7, None],
    [142.5, 7, None],
    [149.5, 7, None],
    [156.5, 7, None],
    [163.5, 7, None],
    [233.5, 7, None],
    [240.5, 7, None],
    [247.5, 7, None],
    [254.5, 7, None],
    [261.5, 7, None],
    [268.5, 7, None],
    [275.5, 7, None],
    [282.5, 7, None],
    [289.5, 7, None],
    [296.5, 7, None],
    [114.0, 8, None],
    [114.5, 8, None],
    [121.5, 8, None],
    [122.0, 8, None],
    [128.5, 8, None],
    [130.0, 8, None],
    [135.5, 8, None],
    [138.0, 8, None],
    [142.5, 8, None],
    [146.0, 8, None],
    [149.5, 8, None],
    [154.0, 8, None],
    [156.5, 8, None],
    [162.0, 8, None],
    [163.5, 8, None],
    [170.0, 8, None],
    [170.5, 8, None],
    [177.5, 8, None],
    [178.0, 8, None],
    [184.5, 8, None],
    [186.0, 8, None],
    [191.5, 8, None],
    [194.0, 8, None],
    [198.5, 8, None],
    [202.0, 8, None],
    [205.5, 8, None],
    [210.0, 8, None],
    [212.5, 8, None],
    [218.0, 8, None],
    [219.5, 8, None],
    [226.0, 8, None],
    [226.5, 8, None],
    [233.5, 8, None],
    [234.0, 8, None],
    [240.5, 8, None],
    [242.0, 8, None],
    [247.5, 8, None],
    [250.0, 8, None],
    [254.5, 8, None],
    [258.0, 8, None],
    [261.5, 8, None],
    [266.0, 8, None],
    [268.5, 8, None],
    [274.0, 8, None],
    [275.5, 8, None],
    [282.0, 8, None],
    [282.5, 8, None],
    [289.5, 8, None],
    [290.0, 8, None],
    [296.5, 8, None],
    [298.0, 8, None],
    [306.0, 8, None],
    [314.0, 8, None],
    [322.0, 8, None],
    [330.0, 8, None],
    [338.0, 8, None],
    [346.0, 8, None],
    [354.0, 8, None],
    [362.0, 8, None],
    [370.0, 8, None],
    [378.0, 8, None],
    [386.0, 8, None],
    [394.0, 8, None],
    [402.0, 8, None],
    [410.0, 8, None],
    [418.0, 8, None],
    [426.0, 8, None],
    [434.0, 8, None],
    [442.0, 8, None],
    [450.0, 8, None],
    [458.0, 8, None],
    [466.0, 8, None]]

my_file = Path("../../ekt_json/dvbt2_34_centre_frequencies.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    dict_test_parame_result["test_parame_result"] = FREQUENCY_BW_LIST
    write_json_file("../../ekt_json/dvbt2_34_centre_frequencies.json", dict_test_parame_result)

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
    load_dict = read_json_file("../../ekt_json/dvbt2_34_centre_frequencies.json")
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
    specan.set_digitaltv_framing_pilot_dvbt2("PP2")
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_bicm_constellation_dvbt2(MODULATION_64QAM)
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_framing_fftsize_dvbt2(FFT_SIZE_8K)
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_bicm_coderate_dvbt2(CODE_RATE_2_3)
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_framing_guard_dvbt2(GUARD_G1_8)

    for FREQUENCY_BW in load_dict.get("test_parame_result"):
        if FREQUENCY_BW[2] == None:
            pass
        else:
            continue
        specan = Ektsfu(sfu_ip)
        specan.set_frequency_frequency_frequency(str(int(FREQUENCY_BW[0])) + "MHz")
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_channelbandwidth_dvbt2("BW_{}".format(str(FREQUENCY_BW[1])))
        specan = Ektsfu(sfu_ip)
        # specan.set_level_level_offset(str(FREQUENCY_LEVEL_OFFSET[1]))
        # specan = Ektsfu(sfu_ip)
        specan.set_level_level_level("dBm", "-60")

        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(
            json.dumps({"cmd": "set_frequency_data", "frequency": str(int(FREQUENCY_BW[0]))}))
        time.sleep(1)
        del net
        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(json.dumps({"cmd": "set_bandwidth_data", "bandwidth": str(FREQUENCY_BW[1])}))
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
                                      "dvbt2_34_centre_frequencies: current_time:{}, frequency:{} MHz,bandwidth:{} Ksym/s, {}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          str(FREQUENCY_BW[0]), str(FREQUENCY_BW[1]),
                                          "Lock fail") + "\n"))
            continue
        else:
            write_test_result("../../ekt_log/test_result_sfu.txt", ("Lock state err" + "\n"))
            continue

        start_data_result, mosaic_result = mosaic_algorithm(sfu_ip, "-60", "-60")
        print ("dvbt2_34_centre_frequencies: current_time:{}, modulation: {},coderate:{}, frequency:{} MHz,bandwidth:{} MHZ,{}".format(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), MODULATION_64QAM,
            CODE_RATE_2_3, str(FREQUENCY_BW[0]), str(FREQUENCY_BW[1]), start_data_result.get("detect_mosic_result")))
        write_test_result("../../ekt_log/test_result_sfu.txt",
                          "dvbt2_34_centre_frequencies: current_time:{}, modulation: {}, coderate:{}, frequency:{} MHz,bandwidth:{} MHZ,{}".format(
                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                              MODULATION_64QAM, CODE_RATE_2_3,
                              str(FREQUENCY_BW[0]), str(FREQUENCY_BW[1]),
                              start_data_result.get("detect_mosic_result")) + "\n")
        FREQUENCY_BW[2] = mosaic_result
        write_json_file("../../ekt_json/dvbt2_34_centre_frequencies.json", load_dict)
        dvbt2_34_centre_frequencies_json_to_csv(
            "../../ekt_json/dvbt2_34_centre_frequencies.json",
            "../../ekt_test_report/dvbt2_34_centre_frequencies.csv")

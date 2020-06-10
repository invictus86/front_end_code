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
    dvbt2_51_verification_strength_json_to_csv

MODULATION_256QAM = "T256"
PP4 = "PP4"
CODE_RATE_2_3 = "R2_3"
CODE_RATE_3_5 = "R3_5"
CODE_RATE_3_4 = "R3_4"

GUARD_G1_16 = "G1_16"
GUARD_G19_256 = "G19256"

FREQUENCY_474 = 474
FREQUENCY_666 = 666
FREQUENCY_786 = 786

FREQUENCY_178 = 178
FREQUENCY_199 = 199
FREQUENCY_227 = 227

LEVEL_OFFSET_474 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", 474.0)
LEVEL_OFFSET_666 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", 666.0)
LEVEL_OFFSET_786 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", 786.0)

LEVEL_OFFSET_177_5 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", 177.5)
LEVEL_OFFSET_198_5 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", 198.5)
LEVEL_OFFSET_226_5 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", 226.5)

PARAMETER_LIST = [
    [MODULATION_256QAM, PP4, CODE_RATE_2_3, GUARD_G1_16, 8,
     [[FREQUENCY_474, LEVEL_OFFSET_474], [FREQUENCY_666, LEVEL_OFFSET_666], [FREQUENCY_786, LEVEL_OFFSET_786]]],
    [MODULATION_256QAM, PP4, CODE_RATE_2_3, GUARD_G19_256, 7,
     [[FREQUENCY_178, LEVEL_OFFSET_177_5], [FREQUENCY_199, LEVEL_OFFSET_198_5], [FREQUENCY_227, LEVEL_OFFSET_226_5]]],
    [MODULATION_256QAM, PP4, CODE_RATE_3_5, GUARD_G19_256, 7,
     [[FREQUENCY_474, LEVEL_OFFSET_474], [FREQUENCY_666, LEVEL_OFFSET_666], [FREQUENCY_786, LEVEL_OFFSET_786]]],
    [MODULATION_256QAM, PP4, CODE_RATE_3_4, GUARD_G1_16, 7,
     [[FREQUENCY_474, LEVEL_OFFSET_474], [FREQUENCY_666, LEVEL_OFFSET_666], [FREQUENCY_786, LEVEL_OFFSET_786]]],
]

LEVEL_LIST = [-40, -50, -60, -70, -80, -95]

my_file = Path("../../ekt_json/dvbt2_51_verification_signal_strength_indicator_ssi.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    list_test_parame_result = []

    for PARAMETER in PARAMETER_LIST:
        for frequency in PARAMETER[5]:
            list_test_result = []
            for LEVEL in LEVEL_LIST:
                list_test_result.append([LEVEL, None])

            list_test_parame_result.append(
                [frequency, PARAMETER[0], PARAMETER[1], PARAMETER[2], PARAMETER[3], PARAMETER[4], list_test_result])

    dict_test_parame_result["test_parame_result"] = list_test_parame_result
    # print dict_test_parame_result

    write_json_file("../../ekt_json/dvbt2_51_verification_signal_strength_indicator_ssi.json",
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
    load_dict = read_json_file("../../ekt_json/dvbt2_51_verification_signal_strength_indicator_ssi.json")
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
    # 666MHZ 报错,设置低一些
    # specan.set_digitaltv_framing_ldata_dvbt2("61")
    specan.set_digitaltv_framing_ldata_dvbt2("45")

    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_framing_fftsize_dvbt2("M32E")

    stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                ["tests/front_end_test/testcases.py::test_continuous_button_7414g_set_search"],
                                "auto_front_end_test", "DSD4614iALM")

    for PARAMETER in load_dict.get("test_parame_result"):
        loop_lock_mark = False
        for check_list in PARAMETER[6]:
            if check_list[1] == None:
                loop_lock_mark = True
                break
        if loop_lock_mark == True:
            pass
        else:
            continue

        specan = Ektsfu(sfu_ip)
        specan.set_frequency_frequency_frequency(str(PARAMETER[0][0]) + "MHz")
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_offset(str(PARAMETER[0][1]))

        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_bicm_constellation_dvbt2(PARAMETER[1])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_pilot_dvbt2(PARAMETER[2])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_bicm_coderate_dvbt2(PARAMETER[3])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_guard_dvbt2(PARAMETER[4])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_channelbandwidth_dvbt2("BW_{}".format(str(PARAMETER[5])))

        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": str(int(PARAMETER[0][0]))}))
        time.sleep(1)
        del net
        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(json.dumps({"cmd": "set_bandwidth_data", "bandwidth": str(PARAMETER[5])}))
        time.sleep(1)
        del net
        """
        触发stb-tester进行频率和符号率设置
        """
        stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                    [
                                        "tests/front_end_test/testcases.py::test_continuous_button_7414g_set_frequency_bandwidth"],
                                    "auto_front_end_test", "DSD4614iALM")

        for LEVEL in PARAMETER[6]:
            if LEVEL[1] == None:
                pass
            else:
                continue
            specan = Ektsfu(sfu_ip)
            specan.set_level_level_level("dBm", str(LEVEL[0] - float(PARAMETER[0][1])))
            time.sleep(5)
            stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                        [
                                            "tests/front_end_test/testcases.py::test_ocr_strength_quality"],
                                        "auto_front_end_test", "DSD4614iALM")

            net = ekt_net.EktNetClient('192.168.1.24', 9999)
            strength_quality_data = net.send_rec(json.dumps({"cmd": "get_strength_quality"}))
            time.sleep(0.5)

            dict_strength_quality_data = json.loads(strength_quality_data)
            strength_num = dict_strength_quality_data.get("strength_num")
            LEVEL[1] = strength_num
            write_json_file(
                "../../ekt_json/dvbt2_51_verification_signal_strength_indicator_ssi.json", load_dict)
            dvbt2_51_verification_strength_json_to_csv(
                "../../ekt_json/dvbt2_51_verification_signal_strength_indicator_ssi.json",
                "../../ekt_test_report/dvbt2_51_verification_signal_strength_indicator_ssi.csv")

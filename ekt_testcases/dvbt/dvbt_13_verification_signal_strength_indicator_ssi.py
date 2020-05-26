#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import datetime
from ekt_lib import ekt_net, ekt_cfg
from ekt_lib.ekt_sfu import Ektsfu
from ekt_lib.ekt_stb_tester import stb_tester_execute_testcase
from ekt_lib.threshold_algorithm_SFU import mosaic_algorithm
from ekt_lib.ekt_utils import write_test_result, find_level_offset_by_frequency

MODULATION_64QAM = "T64"
CODE_RATE_2_3 = "R2_3"
CODE_RATE_3_4 = "R3_4"
GUARD_G1_8 = "G1_8"
FFT_SIZE_8K = "M8K"
LEVEL_60 = "-80"

BW_7 = "BW_7"
BW_8 = "BW_8"

LEVEL_OFFSET_666 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", 666.0)
LEVEL_OFFSET_474 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", 474.0)
LEVEL_OFFSET_786 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", 786.0)
LEVEL_OFFSET_177_5 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", 177.5)
LEVEL_OFFSET_198_5 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", 198.5)
LEVEL_OFFSET_226_5 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", 226.5)

PARAMETER_LIST = [
    [MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, 8, 666, LEVEL_OFFSET_666],
    [MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, 8, 474, LEVEL_OFFSET_474],
    [MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, 8, 786, LEVEL_OFFSET_786],
    [MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, 7, 117.5, LEVEL_OFFSET_177_5],
    [MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, 7, 198.5, LEVEL_OFFSET_198_5],
    [MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, 7, 226.5, LEVEL_OFFSET_226_5],
    [MODULATION_64QAM, CODE_RATE_3_4, GUARD_G1_8, 7, 666, LEVEL_OFFSET_666],
]

LEVEL_LIST = [-40, -50, -60, -70, -80, -95]



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
    specan.set_digitaltv_coding_fftmode_dvbt(FFT_SIZE_8K)

    stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                ["tests/front_end_test/testcases.py::test_continuous_button_7414g_set_search"],
                                "auto_front_end_test", "DSD4614iALM")
    for PARAMETER in PARAMETER_LIST:
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_constellation_dvbt(PARAMETER[0])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_coderate_dvbt(PARAMETER[1])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_guard_dvbt(PARAMETER[2])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_channelbandwidth_dvbt("BW_{}".format(str(PARAMETER[3])))
        specan = Ektsfu(sfu_ip)
        specan.set_frequency_frequency_frequency(str(int(PARAMETER[4])) + "MHz")
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_offset(str(PARAMETER[5]))

        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": str(int(PARAMETER[4]))}))
        time.sleep(1)
        del net
        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(json.dumps({"cmd": "set_bandwidth_data", "bandwidth": str(PARAMETER[3])}))
        time.sleep(1)
        del net
        """
        触发stb-tester进行频率和符号率设置
        """
        stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                    [
                                        "tests/front_end_test/testcases.py::test_continuous_button_7414g_set_frequency_bandwidth"],
                                    "auto_front_end_test", "DSD4614iALM")

        for LEVEL in LEVEL_LIST:
            specan = Ektsfu(sfu_ip)
            specan.set_level_level_level("dBm", str(LEVEL))
            stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                        [
                                            "tests/front_end_test/testcases.py::test_ocr_strength_quality"],
                                        "auto_front_end_test", "DSD4614iALM")

            net = ekt_net.EktNetClient('192.168.1.24', 9999)
            strength_quality_data = net.send_rec(json.dumps({"cmd": "get_strength_quality"}))
            time.sleep(0.5)

            dict_strength_quality_data = json.loads(strength_quality_data)
            print dict_strength_quality_data

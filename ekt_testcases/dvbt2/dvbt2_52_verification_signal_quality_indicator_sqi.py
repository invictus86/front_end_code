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
    dvbt2_52_verification_quality_json_to_csv

MODULATION_256QAM = "T256"
PP4 = "PP4"
PP2 = "PP2"
CODE_RATE_3_5 = "R3_5"
CODE_RATE_2_3 = "R2_3"
CODE_RATE_3_4 = "R3_4"

GUARD_G19_256 = "G19256"
GUARD_G1_16 = "G1_16"
GUARD_G1_8 = "G1_8"

FREQUENCY_666 = 666

LEVEL_OFFSET_666 = find_level_offset_by_frequency("DVBT_T2_FREQUENCY_LEVEL_OFFSET", 666.0)

PARAMETER_LIST = [
    [MODULATION_256QAM, PP4, CODE_RATE_3_5, GUARD_G19_256, 8, [27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16]],
    [MODULATION_256QAM, PP4, CODE_RATE_2_3, GUARD_G1_16, 8, [27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17]],
    [MODULATION_256QAM, PP2, CODE_RATE_3_4, GUARD_G1_8, 8, [27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13]]
]

my_file = Path("../../ekt_json/dvbt2_52_verification_signal_quality_indicator_sqi.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    list_test_parame_result = []

    for PARAMETER in PARAMETER_LIST:
        list_test_result = []
        for CN in PARAMETER[5]:
            list_test_result.append([CN, None])

        list_test_parame_result.append(
            [PARAMETER[0], PARAMETER[1], PARAMETER[2], PARAMETER[3], PARAMETER[4], list_test_result])

    dict_test_parame_result["test_parame_result"] = list_test_parame_result
    # print dict_test_parame_result

    write_json_file("../../ekt_json/dvbt2_52_verification_signal_quality_indicator_sqi.json",
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
    load_dict = read_json_file("../../ekt_json/dvbt2_52_verification_signal_quality_indicator_sqi.json")
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
    specan.set_noise_noise_noise("ADD")
    specan = Ektsfu(sfu_ip)
    specan.set_noise_noise_awgn("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_noise_settings_bandwith("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_fading_fading_state("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_modulator("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_baseband("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_system_papr_dvbt2("TR")
    specan = Ektsfu(sfu_ip)
    # 待确认第三项SFU是否会报错
    specan.set_digitaltv_framing_ldata_dvbt2("61")

    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_framing_fftsize_dvbt2("M32E")

    specan = Ektsfu(sfu_ip)
    specan.set_frequency_frequency_frequency(str(FREQUENCY_666) + "MHz")
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_offset(str(LEVEL_OFFSET_666))

    specan = Ektsfu(sfu_ip)
    specan.set_level_level_level("dBm", str(-60))

    stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                ekt_cfg.DVB_T2_SET_SEARCH_FUNCTION, ekt_cfg.DVB_T2_SET_SEARCH_CATEGORY, ekt_cfg.DVB_T2_SET_SEARCH_REMOTE)

    for PARAMETER in load_dict.get("test_parame_result"):
        loop_lock_mark = False
        for check_list in PARAMETER[5]:
            if check_list[1] == None:
                loop_lock_mark = True
                break
        if loop_lock_mark == True:
            pass
        else:
            continue
        if PARAMETER[1] == "PP2":
            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_framing_ldata_dvbt2("45")
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_bicm_constellation_dvbt2(PARAMETER[0])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_pilot_dvbt2(PARAMETER[1])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_bicm_coderate_dvbt2(PARAMETER[2])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_guard_dvbt2(PARAMETER[3])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_framing_channelbandwidth_dvbt2("BW_{}".format(str(PARAMETER[4])))

        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": str(int(FREQUENCY_666))}))
        time.sleep(1)
        del net
        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        net.send_data(json.dumps({"cmd": "set_bandwidth_data", "bandwidth": str(PARAMETER[4])}))
        time.sleep(1)
        del net
        """
        触发stb-tester进行频率和符号率设置
        """
        stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                    ekt_cfg.DVB_T2_SET_FREQUENCY_BANDWIDTH_FUNCTION, ekt_cfg.DVB_T2_SET_FREQUENCY_BANDWIDTH_CATEGORY,
                                    ekt_cfg.DVB_T2_SET_FREQUENCY_BANDWIDTH_REMOTE)

        for CN in PARAMETER[5]:
            if CN[1] == None:
                pass
            else:
                continue
            time.sleep(5)
            specan = Ektsfu(sfu_ip)
            specan.set_noise_awgn_cn(str(CN[0]))
            time.sleep(5)

            stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                        ekt_cfg.DVB_T2_OCR_FUNCTION, ekt_cfg.DVB_T2_OCR_CATEGORY, ekt_cfg.DVB_T2_OCR_REMOTE)

            net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
            strength_quality_data = net.send_rec(json.dumps({"cmd": "get_strength_quality"}))
            time.sleep(0.5)

            dict_strength_quality_data = json.loads(strength_quality_data)
            quality_num = dict_strength_quality_data.get("quality_num")
            CN[1] = quality_num
            write_json_file(
                "../../ekt_json/dvbt2_52_verification_signal_quality_indicator_sqi.json", load_dict)
            dvbt2_52_verification_quality_json_to_csv(
                "../../ekt_json/dvbt2_52_verification_signal_quality_indicator_sqi.json",
                "../../ekt_test_report/dvbt2_52_verification_signal_quality_indicator_sqi.csv")
    # 测试完成之后复原主界面，方便下个测试项
    stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                ["tests/front_end_test/testcases.py::test_exit"], ekt_cfg.DVB_T2_SET_SEARCH_CATEGORY,
                                ekt_cfg.DVB_T2_SET_SEARCH_REMOTE)

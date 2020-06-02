#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import datetime
from ekt_lib import ekt_net, ekt_cfg
from ekt_lib.ekt_sfu import Ektsfu
from pathlib2 import Path
from ekt_lib.ekt_stb_tester import stb_tester_execute_testcase
from ekt_lib.threshold_algorithm_SFU import iterate_to_find_threshold_noise_cn_step_by_step
from ekt_lib.ekt_utils import write_test_result, write_json_file, read_json_file, find_level_offset_by_frequency, \
    dvbt_29_performance_time_varying_to_csv

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

PARAMETER_LIST = [
    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, 23.2, 20, 0, None],
    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, 23.2, 20, 1, None],
    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, 23.2, 20, 5, None],
    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, 23.2, 20, 10, None],
    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, 23.2, 20, 15, None],
    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, 23.2, 20, 20, None],

    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_4, 22.2, 20, 0, None],
    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_4, 22.2, 20, 1, None],
    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_4, 22.2, 20, 5, None],
    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_4, 22.2, 20, 10, None],
    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_4, 22.2, 20, 15, None],
    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_4, 22.2, 20, 20, None],

    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_3_4, GUARD_G1_4, 27.6, 20, 0, None],
    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_3_4, GUARD_G1_4, 27.6, 20, 1, None],
    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_3_4, GUARD_G1_4, 27.6, 20, 5, None],
    [FFT_SIZE_8K, MODULATION_64QAM, CODE_RATE_3_4, GUARD_G1_4, 27.6, 20, 10, None],
]

# 无法设置fading 里面的Doppler     SFU的 set_fading_settings_reference 设置无效

my_file = Path("../../ekt_json/dvbt_29_performance_time_varying_channel.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    dict_test_parame_result["test_parame_result"] = PARAMETER_LIST
    write_json_file("../../ekt_json/dvbt_29_performance_time_varying_channel.json",
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
    load_dict = read_json_file("../../ekt_json/dvbt_29_performance_time_varying_channel.json")
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
    specan.set_fading_settings_reference("FDOPpler")

    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_state("1", "1", "ON")
    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_state("1", "2", "ON")

    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_profile("1", "1", "SPATh")
    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_profile("1", "2", "SPATh")

    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_additdelay("2", "1", "20E-6")

    specan = Ektsfu(sfu_ip)
    specan.set_frequency_frequency_frequency(str(FREQUENCY_666) + "MHz")
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_coding_channelbandwidth_dvbt("BW_{}".format(str(8)))
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_offset(str(LEVEL_OFFSET_666))
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_level("dBm", str(LEVEL_50_666))

    net = ekt_net.EktNetClient('192.168.1.24', 9999)
    net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": str(int(FREQUENCY_666))}))
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
                                  "dvbt_29_performance_time_varying_channel: current_time:{}, frequency：{} MHz，bandwidth：{} Ksym/s, {}".format(
                                      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                      str(FREQUENCY_666), str(8), "锁台失败") + "\n"))

    for PARAMETER in load_dict.get("test_parame_result"):
        if PARAMETER[7] == None:
            pass
        else:
            continue
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_fftmode_dvbt(PARAMETER[0])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_constellation_dvbt(PARAMETER[1])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_coderate_dvbt(PARAMETER[2])
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_guard_dvbt(PARAMETER[3])
        specan = Ektsfu(sfu_ip)
        specan.set_fading_profile_pathloss("1", "2", "{} dB".format(str(PARAMETER[6])))

        res, test_result = iterate_to_find_threshold_noise_cn_step_by_step(sfu_ip, PARAMETER[4])
        print(
            "dvbt_29_performance_time_varying_channel: current_time:{}, modulation: {} coderate：{}, frequency：{} MHz，bandwidth：{} MHZ，{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), PARAMETER[1],
                PARAMETER[2], str(FREQUENCY_666), str(8), res))
        write_test_result("../../ekt_log/test_result_sfu.txt",
                          "dvbt_29_performance_time_varying_channel: current_time:{}, modulation: {} coderate：{}, frequency：{} MHz，bandwidth：{} MHZ，{}".format(
                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), PARAMETER[1],
                              PARAMETER[2], str(FREQUENCY_666), str(8), res) + "\n")

        PARAMETER[7] = test_result
        write_json_file("../../ekt_json/dvbt_29_performance_time_varying_channel.json", load_dict)
        dvbt_29_performance_time_varying_to_csv(
            "../../ekt_json/dvbt_29_performance_time_varying_channel.json",
            "../../ekt_test_report/dvbt_29_performance_time_varying_channel.csv")

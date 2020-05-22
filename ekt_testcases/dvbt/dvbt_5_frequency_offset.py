#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import datetime
from ekt_lib import ekt_net, ekt_cfg
from ekt_lib.ekt_sfu import Ektsfu
from ekt_lib.ekt_stb_tester import stb_tester_execute_testcase
from ekt_lib.threshold_algorithm_SFU import mosaic_algorithm
from ekt_lib.ekt_utils import write_test_result

MODULATION_64QAM = "T64"
FFT_SIZE_8K = "M8K"
CODE_RATE_2_3 = "R2_3"
GUARD_G1_8 = "G1_8"
LEVEL_60 = "-60"

FREQUENCY_BW_OFFSET_LIST = [
    [177.5, 7, -50],
    [177.5, 7, 0],
    [177.5, 7, +50],
    [226.5, 7, -50],
    [226.5, 7, 0],
    [226.5, 7, +50],
    [474.0, 8, -50],
    [474.0, 8, 0],
    [474.0, 8, +50],
    [858.0, 8, -50],
    [858.0, 8, 0],
    [858.0, 8, +50]]

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
    specan.set_digitaltv_coding_constellation_dvbt(MODULATION_64QAM)
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_coding_fftmode_dvbt(FFT_SIZE_8K)
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_coding_coderate_dvbt(CODE_RATE_2_3)
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_coding_guard_dvbt(GUARD_G1_8)

    for FREQUENCY_BW in FREQUENCY_BW_OFFSET_LIST:
        specan = Ektsfu(sfu_ip)
        specan.set_frequency_frequency_frequency(str(FREQUENCY_BW[0]) + "MHz")
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_channelbandwidth_dvbt("BW_{}".format(str(FREQUENCY_BW[1])))
        specan = Ektsfu(sfu_ip)
        # specan.set_level_level_offset(str(FREQUENCY_LEVEL_OFFSET[1]))
        # specan = Ektsfu(sfu_ip)
        specan.set_level_level_level("dBm", "-60")

        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(
            json.dumps({"cmd": "set_frequency_data", "frequency": str(int(FREQUENCY_BW[0] + FREQUENCY_BW[2]))}))
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
                                      "dvbt_5_frequency_offset: current_time:{}, frequency：{} MHz，stb_frequency：{} MHz，bandwidth：{} Ksym/s, {}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          str(FREQUENCY_BW[0]), str(int(FREQUENCY_BW[0] + FREQUENCY_BW[2])),
                                          str(FREQUENCY_BW[1]),
                                          "锁台失败") + "\n"))
            continue
        else:
            write_test_result("../../ekt_log/test_result_sfu.txt", ("出错了" + "\n"))
            continue

        try:
            start_data_result = mosaic_algorithm(sfu_ip, "-60", "-60")
            print "dvbt_5_frequency_offset: current_time:{}, modulation: {},coderate：{}, frequency：{} MHz，stb_frequency：{} MHz，bandwidth：{} MHZ，{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), MODULATION_64QAM,
                CODE_RATE_2_3, str(FREQUENCY_BW[0]), str(int(FREQUENCY_BW[0] + FREQUENCY_BW[2])), str(FREQUENCY_BW[1]),
                start_data_result.get("detect_mosic_result"))
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              "dvbt_5_frequency_offset: current_time:{}, modulation: {}, coderate：{}, frequency：{} MHz，stb_frequency：{} MHz，bandwidth：{} MHZ，{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                  MODULATION_64QAM, CODE_RATE_2_3, str(FREQUENCY_BW[0]),
                                  str(int(FREQUENCY_BW[0] + FREQUENCY_BW[2])), str(FREQUENCY_BW[1]),
                                  start_data_result.get("detect_mosic_result")) + "\n")
        except:
            start_data_result = mosaic_algorithm(sfu_ip, "-60", "-60")
            print "dvbt_5_frequency_offset: current_time:{}, modulation: {},coderate：{}, frequency：{} MHz，stb_frequency：{} MHz，bandwidth：{} MHZ，{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), MODULATION_64QAM,
                CODE_RATE_2_3, str(FREQUENCY_BW[0]), str(int(FREQUENCY_BW[0] + FREQUENCY_BW[2])), str(FREQUENCY_BW[1]),
                start_data_result.get("detect_mosic_result"))
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              "dvbt_5_frequency_offset: current_time:{}, modulation: {}, coderate：{}, frequency：{} MHz，stb_frequency：{} MHz，bandwidth：{} MHZ，{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                  MODULATION_64QAM, CODE_RATE_2_3, str(FREQUENCY_BW[0]),
                                  str(int(FREQUENCY_BW[0] + FREQUENCY_BW[2])), str(FREQUENCY_BW[1]),
                                  start_data_result.get("detect_mosic_result")) + "\n")
        """
        进行机顶盒的频率修改或其他参数的修改
        读取误码率或者判断机顶盒是否含有马赛克
        """
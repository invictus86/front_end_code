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

FREQUENCY_BW_LIST = [
    [177.5, 7],
    [184.5, 7],
    [191.5, 7],
    [198.5, 7],
    [205.5, 7],
    [212.5, 7],
    [219.5, 7],
    [226.5, 7],
    [474.0, 8],
    [482.0, 8],
    [490.0, 8],
    [498.0, 8],
    [506.0, 8],
    [514.0, 8],
    [522.0, 8],
    [530.0, 8],
    [538.0, 8],
    [546.0, 8],
    [554.0, 8],
    [562.0, 8],
    [570.0, 8],
    [578.0, 8],
    [586.0, 8],
    [594.0, 8],
    [602.0, 8],
    [610.0, 8],
    [618.0, 8],
    [626.0, 8],
    [634.0, 8],
    [642.0, 8],
    [650.0, 8],
    [658.0, 8],
    [666.0, 8],
    [674.0, 8],
    [682.0, 8],
    [690.0, 8],
    [698.0, 8],
    [706.0, 8],
    [714.0, 8],
    [722.0, 8],
    [730.0, 8],
    [738.0, 8],
    [746.0, 8],
    [754.0, 8],
    [762.0, 8],
    [770.0, 8],
    [778.0, 8],
    [786.0, 8],
    [794.0, 8],
    [802.0, 8],
    [810.0, 8],
    [818.0, 8],
    [826.0, 8],
    [834.0, 8],
    [842.0, 8],
    [850.0, 8],
    [858.0, 8],
    [114.5, 7],
    [121.5, 7],
    [128.5, 7],
    [135.5, 7],
    [142.5, 7],
    [149.5, 7],
    [156.5, 7],
    [163.5, 7],
    [233.5, 7],
    [240.5, 7],
    [247.5, 7],
    [254.5, 7],
    [261.5, 7],
    [268.5, 7],
    [275.5, 7],
    [282.5, 7],
    [289.5, 7],
    [296.5, 7],
    [114.0, 8],
    [114.5, 8],
    [121.5, 8],
    [122.0, 8],
    [128.5, 8],
    [130.0, 8],
    [135.5, 8],
    [138.0, 8],
    [142.5, 8],
    [146.0, 8],
    [149.5, 8],
    [154.0, 8],
    [156.5, 8],
    [162.0, 8],
    [163.5, 8],
    [170.0, 8],
    [170.5, 8],
    [177.5, 8],
    [178.0, 8],
    [184.5, 8],
    [186.0, 8],
    [191.5, 8],
    [194.0, 8],
    [198.5, 8],
    [202.0, 8],
    [205.5, 8],
    [210.0, 8],
    [212.5, 8],
    [218.0, 8],
    [219.5, 8],
    [226.0, 8],
    [226.5, 8],
    [233.5, 8],
    [234.0, 8],
    [240.5, 8],
    [242.0, 8],
    [247.5, 8],
    [250.0, 8],
    [254.5, 8],
    [258.0, 8],
    [261.5, 8],
    [266.0, 8],
    [268.5, 8],
    [274.0, 8],
    [275.5, 8],
    [282.0, 8],
    [282.5, 8],
    [289.5, 8],
    [290.0, 8],
    [296.5, 8],
    [298.0, 8],
    [306.0, 8],
    [314.0, 8],
    [322.0, 8],
    [330.0, 8],
    [338.0, 8],
    [346.0, 8],
    [354.0, 8],
    [362.0, 8],
    [370.0, 8],
    [378.0, 8],
    [386.0, 8],
    [394.0, 8],
    [402.0, 8],
    [410.0, 8],
    [418.0, 8],
    [426.0, 8],
    [434.0, 8],
    [442.0, 8],
    [450.0, 8],
    [458.0, 8],
    [466.0, 8]]

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

    for FREQUENCY_BW in FREQUENCY_BW_LIST:
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
                                      "dvbt_4_centre_frequencies: current_time:{}, frequency：{} MHz，bandwidth：{} Ksym/s, {}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          str(FREQUENCY_BW[0]), str(FREQUENCY_BW[1]),
                                          "锁台失败") + "\n"))
            continue
        else:
            write_test_result("../../ekt_log/test_result_sfu.txt", ("出错了" + "\n"))
            continue

        try:
            start_data_result = mosaic_algorithm(sfu_ip, "-60", "-60")
            print "dvbt_4_centre_frequencies: current_time:{}, modulation: {},coderate：{}, frequency：{} MHz，bandwidth：{} MHZ，{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), MODULATION_64QAM,
                CODE_RATE_2_3, str(FREQUENCY_BW[0]), str(FREQUENCY_BW[1]), start_data_result.get("detect_mosic_result"))
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              "dvbt_4_centre_frequencies: current_time:{}, modulation: {}, coderate：{}, frequency：{} MHz，bandwidth：{} MHZ，{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                  MODULATION_64QAM, CODE_RATE_2_3,
                                  str(FREQUENCY_BW[0]), str(FREQUENCY_BW[1]),
                                  start_data_result.get("detect_mosic_result")) + "\n")
        except:
            start_data_result = mosaic_algorithm(sfu_ip, "-60", "-60")
            print "dvbt_4_centre_frequencies: current_time:{}, modulation: {},coderate：{}, frequency：{} MHz，bandwidth：{} MHZ，{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), MODULATION_64QAM,
                CODE_RATE_2_3, str(FREQUENCY_BW[0]), str(FREQUENCY_BW[1]), start_data_result.get("detect_mosic_result"))
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              "dvbt_4_centre_frequencies: current_time:{}, modulation: {}, coderate：{}, frequency：{} MHz，bandwidth：{} MHZ，{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                  MODULATION_64QAM, CODE_RATE_2_3,
                                  str(FREQUENCY_BW[0]), str(FREQUENCY_BW[1]),
                                  start_data_result.get("detect_mosic_result")) + "\n")
        """
        进行机顶盒的频率修改或其他参数的修改
        读取误码率或者判断机顶盒是否含有马赛克
        """

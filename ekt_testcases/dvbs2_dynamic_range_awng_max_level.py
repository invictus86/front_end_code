#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import datetime
from ekt_lib import ekt_net, ekt_cfg
from ekt_lib.ekt_sfu import Ektsfu
from ekt_lib.ekt_stb_tester import stb_tester_detect_motion
from ekt_lib.threshold_algorithm_SFU import iterate_to_find_threshold, mosaic_algorithm
from ekt_lib.ekt_utils import write_test_result, read_ekt_config_data

AWGN_ON = "ON"
AWGN_OFF = "OFF"

MODULATION_QPSK = "S4"
MODULATION_8PSK = "S8"

SYMBOL_RATE_5M = ["5.000000e6", "05000"]
SYMBOL_RATE_10M = ["10.000000e6", "10000"]
SYMBOL_RATE_27_5M = ["27.500000e6", "27500"]
SYMBOL_RATE_45M = ["45.000000e6", "45000"]

dict_config_data = {
    "MODULATION": [MODULATION_QPSK, MODULATION_8PSK],
    # "SYMBOL_RATE": [SYMBOL_RATE_5M, SYMBOL_RATE_10M, SYMBOL_RATE_27_5M, SYMBOL_RATE_45M],
    # "SYMBOL_RATE": [SYMBOL_RATE_10M, SYMBOL_RATE_27_5M, SYMBOL_RATE_45M],
    "SYMBOL_RATE": [SYMBOL_RATE_5M, SYMBOL_RATE_10M],

}

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
    specan.set_modulation_modulation_standard_dvt("DVS2")
    time.sleep(1)
    specan = Ektsfu(sfu_ip)
    specan.set_player_timing_openfile(r"E:\333\DIVER.GTS")
    time.sleep(1)
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_input_source_dvbs2("TSPLayer")
    time.sleep(1)
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_rf("ON")
    time.sleep(1)
    specan = Ektsfu(sfu_ip)
    specan.set_noise_noise_noise("ADD")
    specan = Ektsfu(sfu_ip)
    specan.set_noise_noise_awgn("ON")
    time.sleep(1)
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_modulator("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_baseband("OFF")

    dict_data = read_ekt_config_data("../ekt_lib/ekt_config.json")
    DVBS_S2_FREQUENCY_LEVEL_OFFSET = dict_data.get("DVBS_S2_FREQUENCY_LEVEL_OFFSET")
    DVBS2_QPSK_CODE_RATE_CN = dict_data.get("DVBS2_QPSK_CODE_RATE_CN")
    DVBS2_8PSK_CODE_RATE_CN = dict_data.get("DVBS2_8PSK_CODE_RATE_CN")

    for MODULATION in dict_config_data.get("MODULATION"):
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_constellation_dvbs2(MODULATION)
        time.sleep(1)
        CURRENT_DVBS2_CODE_RATE_CN = None
        if MODULATION == MODULATION_QPSK:
            CURRENT_DVBS2_CODE_RATE_CN = DVBS2_QPSK_CODE_RATE_CN
        elif MODULATION == MODULATION_8PSK:
            CURRENT_DVBS2_CODE_RATE_CN = DVBS2_8PSK_CODE_RATE_CN
        else:
            write_test_result("../ekt_log/test_result_sfu.txt", ("MODULATION 出错了: {}".format(MODULATION) + "\n"))
        for code_rate_cn in CURRENT_DVBS2_CODE_RATE_CN:
            del specan
            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_coding_coderate_dvbs2(code_rate_cn[0])
            time.sleep(1)
            specan = Ektsfu(sfu_ip)
            # print str(code_rate_cn[1])
            specan.set_noise_awgn_cn(str(code_rate_cn[1]))
            time.sleep(1)

            for SYMBOL_RATE in dict_config_data.get("SYMBOL_RATE"):
                del specan
                specan = Ektsfu(sfu_ip)
                specan.set_digitaltv_coding_symbolrate_dvbs2(SYMBOL_RATE[0])
                for FREQUENCY_LEVEL_OFFSET in DVBS_S2_FREQUENCY_LEVEL_OFFSET:
                    del specan
                    specan = Ektsfu(sfu_ip)
                    specan.set_frequency_frequency_frequency(str(FREQUENCY_LEVEL_OFFSET[0]) + "MHz")
                    time.sleep(1)
                    specan = Ektsfu(sfu_ip)
                    specan.set_level_level_offset(str(FREQUENCY_LEVEL_OFFSET[1]))
                    specan = Ektsfu(sfu_ip)
                    # specan.set_level_level_level("dBm", "-30")
                    specan.set_level_level_level("dBm", str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])))

                    net = ekt_net.EktNetClient('192.168.1.24', 9999)
                    # print str(FREQUENCY_LEVEL_OFFSET[0])
                    # print type(str(FREQUENCY_LEVEL_OFFSET[0]))
                    net.send_data(
                        json.dumps({"cmd": "set_frequency_data", "frequency": str(FREQUENCY_LEVEL_OFFSET[0])}))
                    time.sleep(1)
                    del net
                    net = ekt_net.EktNetClient('192.168.1.24', 9999)
                    net.send_data(json.dumps({"cmd": "set_symbol_rate_data", "symbol_rate": str(SYMBOL_RATE[1])}))
                    time.sleep(1)
                    del net

                    """
                    触发stb-tester进行频率和符号率设置
                    """
                    stb_tester_detect_motion(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                             ["tests/front_end_test/testcases.py::test_continuous_button"],
                                             "auto_front_end_test", "DSD4614iALM")
                    net = ekt_net.EktNetClient('192.168.1.24', 9999)
                    lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
                    if lock_state == "1":
                        pass
                    elif lock_state == "0":
                        write_test_result("../ekt_log/test_result_sfu.txt",
                                          (
                                                  "dvbs2_dynamic_range_awng_max_level: current_time:{}, modulation: {}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, {}".format(
                                                      datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                      MODULATION, code_rate_cn[0],
                                                      str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                                                      str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])),
                                                      "锁台失败") + "\n"))
                        continue
                    else:
                        write_test_result("../ekt_log/test_result_sfu.txt", ("出错了" + "\n"))
                        continue
                    try:
                        start_data_result = mosaic_algorithm(sfu_ip, str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])),
                                                             "-10")
                        print "dvbs2_dynamic_range_awng_max_level: current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, 马赛克检测结果：{}".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn[0],
                            str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                            str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])),
                            start_data_result.get("detect_mosic_result"))
                        write_test_result("../ekt_log/test_result_sfu.txt",
                                          "dvbs2_dynamic_range_awng_max_level: current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, 马赛克检测结果：{}".format(
                                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn[0],
                                              str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                                              str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])),
                                              start_data_result.get("detect_mosic_result")) + "\n")
                    except:
                        start_data_result = mosaic_algorithm(sfu_ip, str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])),
                                                             "-10")
                        print "dvbs2_dynamic_range_awng_max_level: current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, 马赛克检测结果：{}".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn[0],
                            str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                            str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])),
                            start_data_result.get("detect_mosic_result"))
                        write_test_result("../ekt_log/test_result_sfu.txt",
                                          "dvbs2_dynamic_range_awng_max_level: current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, 马赛克检测结果：{}".format(
                                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn[0],
                                              str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                                              str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])),
                                              start_data_result.get("detect_mosic_result")) + "\n")
                    """
                    进行机顶盒的频率修改或其他参数的修改
                    读取误码率或者判断机顶盒是否含有马赛克
                    """

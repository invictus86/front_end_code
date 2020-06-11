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
from ekt_lib.ekt_utils import write_test_result, read_ekt_config_data, write_json_file, read_json_file, \
    dvbs2_18_dynamic_range_awng_max_level_json_to_csv

MODULATION_QPSK = "S4"
MODULATION_8PSK = "S8"

SYMBOL_RATE_5M = ["5.000000e6", "05000", 5]
SYMBOL_RATE_10M = ["10.000000e6", "10000", 10]
SYMBOL_RATE_27_5M = ["27.500000e6", "27500", 27.5]
SYMBOL_RATE_45M = ["45.000000e6", "45000", 45]

dict_config_data = {
    "MODULATION": [MODULATION_QPSK, MODULATION_8PSK],
    "SYMBOL_RATE": [SYMBOL_RATE_5M, SYMBOL_RATE_10M, SYMBOL_RATE_27_5M, SYMBOL_RATE_45M],
}

my_file = Path("../../ekt_json/dvbs2_18_dynamic_range_awng_max_level.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    list_test_parame_result = []

    dict_data = read_ekt_config_data("../../ekt_lib/ekt_config.json")
    DVBS_S2_FREQUENCY_LEVEL_OFFSET = dict_data.get("DVBS_S2_FREQUENCY_LEVEL_OFFSET")
    DVBS2_QPSK_CODE_RATE_CN = dict_data.get("DVBS2_QPSK_CODE_RATE_CN")
    DVBS2_8PSK_CODE_RATE_CN = dict_data.get("DVBS2_8PSK_CODE_RATE_CN")

    for SYMBOL_RATE in dict_config_data.get("SYMBOL_RATE"):
        for FREQUENCY_LEVEL_OFFSET in DVBS_S2_FREQUENCY_LEVEL_OFFSET:
            list_test_result = []
            for MODULATION in dict_config_data.get("MODULATION"):
                CURRENT_DVBS2_CODE_RATE_CN = None
                if MODULATION == MODULATION_QPSK:
                    CURRENT_DVBS2_CODE_RATE_CN = DVBS2_QPSK_CODE_RATE_CN
                elif MODULATION == MODULATION_8PSK:
                    CURRENT_DVBS2_CODE_RATE_CN = DVBS2_8PSK_CODE_RATE_CN

                for code_rate_cn in CURRENT_DVBS2_CODE_RATE_CN:
                    list_test_result.append([MODULATION, code_rate_cn, None])
            list_test_parame_result.append([SYMBOL_RATE, FREQUENCY_LEVEL_OFFSET, list_test_result])
    dict_test_parame_result["test_parame_result"] = list_test_parame_result

    write_json_file("../../ekt_json/dvbs2_18_dynamic_range_awng_max_level.json", dict_test_parame_result)

if __name__ == '__main__':
    """
    测试流程:
    ①重置设备
    ②选择 TSPLAYER
    ③播放流文件
    ④设置modulation,symbol_rate,code_rate,frequency,input_signal_level
    ⑤机顶盒应用中进行锁台并确认锁台成功  （针对stb-tester发送post请求运行testcase）
    ⑤依次修改可变参数,判断机顶盒画面是否含有马赛克并记录结果
    """
    load_dict = read_json_file("../../ekt_json/dvbs2_18_dynamic_range_awng_max_level.json")
    sfu_ip = "192.168.1.50"
    specan = Ektsfu(sfu_ip)
    specan.preset_instrument()
    specan = Ektsfu(sfu_ip)
    specan.set_modulation_modulation_source("DTV")
    specan = Ektsfu(sfu_ip)
    specan.set_modulation_modulation_standard_dvt("DVS2")
    specan = Ektsfu(sfu_ip)
    specan.set_player_timing_openfile(r"E:\333\DIVER.GTS")
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_input_source_dvbs2("TSPLayer")
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_rf("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_noise_noise_noise("ADD")
    specan = Ektsfu(sfu_ip)
    specan.set_noise_noise_awgn("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_noise_settings_bandwith("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_modulator("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_baseband("OFF")

    for LOCK_PARAMETER in load_dict.get("test_parame_result"):
        loop_lock_mark = False
        for check_list in LOCK_PARAMETER[2]:
            if check_list[2] == None:
                loop_lock_mark = True
                break
        if loop_lock_mark == True:
            pass
        else:
            continue

        SYMBOL_RATE = LOCK_PARAMETER[0]
        FREQUENCY_LEVEL_OFFSET = LOCK_PARAMETER[1]
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_symbolrate_dvbs2(SYMBOL_RATE[0])
        specan = Ektsfu(sfu_ip)
        specan.set_noise_settings_receiver("{}e6".format(str(SYMBOL_RATE[2] * 1.2)))
        specan = Ektsfu(sfu_ip)
        specan.set_frequency_frequency_frequency(str(FREQUENCY_LEVEL_OFFSET[0]) + "MHz")
        time.sleep(1)
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_offset(str(FREQUENCY_LEVEL_OFFSET[1]))
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_level("dBm", str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])))

        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": str(FREQUENCY_LEVEL_OFFSET[0])}))
        time.sleep(1)
        del net
        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        net.send_data(json.dumps({"cmd": "set_symbol_rate_data", "symbol_rate": str(SYMBOL_RATE[1])}))
        time.sleep(1)
        del net

        """
        触发stb-tester进行频率和符号率设置
        """
        stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                    ekt_cfg.DVB_S2_LOCK_FUNCTION, ekt_cfg.DVB_S2_CATEGORY, ekt_cfg.DVB_S2_REMOTE)
        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
        if lock_state == "1":
            pass
        elif lock_state == "0":
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              (
                                      "dvbs2_18_dynamic_range_awng_max_level: current_time:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, {}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                                          str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])),
                                          "Lock fail") + "\n"))
            continue
        else:
            write_test_result("../../ekt_log/test_result_sfu.txt", ("Lock state err" + "\n"))
            continue
        for PARAMETER in LOCK_PARAMETER[2]:
            if PARAMETER[2] == None:
                pass
            else:
                continue
            MODULATION = PARAMETER[0]
            code_rate_cn = PARAMETER[1]

            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_coding_constellation_dvbs2(MODULATION)
            time.sleep(1)

            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_coding_coderate_dvbs2(code_rate_cn[0])
            time.sleep(1)
            specan = Ektsfu(sfu_ip)
            specan.set_noise_awgn_cn(str(code_rate_cn[1]))
            time.sleep(1)

            start_data_result, mosaic_result = mosaic_algorithm(sfu_ip, str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])), "-10")
            print (
                "dvbs2_18_dynamic_range_awng_max_level: current_time:{}, modulation: {}, coderate:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, Mosaic results:{}".format(
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), MODULATION, code_rate_cn[0],
                    str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                    str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])),
                    start_data_result.get("detect_mosic_result")))
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              "dvbs2_18_dynamic_range_awng_max_level: current_time:{}, modulation: {}, coderate:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, Mosaic results:{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), MODULATION, code_rate_cn[0],
                                  str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                                  str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])),
                                  start_data_result.get("detect_mosic_result")) + "\n")

            PARAMETER[2] = mosaic_result
            write_json_file("../../ekt_json/dvbs2_18_dynamic_range_awng_max_level.json", load_dict)
            dvbs2_18_dynamic_range_awng_max_level_json_to_csv("../../ekt_json/dvbs2_18_dynamic_range_awng_max_level.json",
                                                              "../../ekt_test_report/dvbs2_18_dynamic_range_awng_max_level.csv")

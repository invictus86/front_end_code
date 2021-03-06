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
from ekt_lib.threshold_algorithm_SFU import iterate_to_find_threshold_step_by_step_dvbs2, mosaic_algorithm
from ekt_lib.ekt_utils import write_test_result, read_ekt_config_data, write_json_file, read_json_file, \
    dvbc_1_dynamic_range_awng_min_level_json_to_csv

test_start_level = -60

MODULATION_64QAM = "C64"
MODULATION_256QAM = "C256"

SYMBOL_RATE_6952 = ["6.952e6", "6952"]

PARAMETER_LIST = [
    [MODULATION_64QAM, SYMBOL_RATE_6952, 27],
    [MODULATION_256QAM, SYMBOL_RATE_6952, 35],
]

my_file = Path("../../ekt_json/dvbc_1_dynamic_range_awng_min_level.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    list_test_parame_result = []

    dict_data = read_ekt_config_data("../../ekt_lib/ekt_config.json")
    DVBC_FREQUENCY_LEVEL_OFFSET = dict_data.get("DVBC_FREQUENCY_LEVEL_OFFSET")

    for PARAMETER in PARAMETER_LIST:
        list_test_result = []
        for FREQUENCY_LEVEL_OFFSET in DVBC_FREQUENCY_LEVEL_OFFSET:
            list_test_result.append([FREQUENCY_LEVEL_OFFSET, None, None, None])
        list_test_parame_result.append([PARAMETER[0], PARAMETER[1], PARAMETER[2], list_test_result])
    dict_test_parame_result["test_parame_result"] = list_test_parame_result

    write_json_file("../../ekt_json/dvbc_1_dynamic_range_awng_min_level.json", dict_test_parame_result)

if __name__ == '__main__':
    """
    测试准备:
    ①清除节目列表
    ②恢复出厂设置
    ③锁台界面QAM 需设置为 AUTO
    """
    load_dict = read_json_file("../../ekt_json/dvbc_1_dynamic_range_awng_min_level.json")
    sfu_ip = ekt_cfg.SFU_IP
    specan = Ektsfu(sfu_ip)
    specan.preset_instrument()
    specan = Ektsfu(sfu_ip)
    specan.set_modulation_modulation_source("DTV")
    specan = Ektsfu(sfu_ip)
    specan.set_modulation_modulation_standard_dvt("DVBC")
    specan = Ektsfu(sfu_ip)
    specan.set_player_timing_openfile(r"E:\333\DIVER.GTS")
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_input_source_dvbc("TSPLayer")
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_rf("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_noise_noise_noise("ADD")
    specan = Ektsfu(sfu_ip)
    specan.set_noise_noise_awgn("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_noise_settings_bandwith("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_modulator("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_baseband("OFF")

    for LOCK_PARAMETER in load_dict.get("test_parame_result"):
        loop_lock_mark = False
        for check_list in LOCK_PARAMETER[3]:
            if check_list[1] == None:
                loop_lock_mark = True
                break
        if loop_lock_mark == True:
            pass
        else:
            continue

        MODULATION = LOCK_PARAMETER[0]
        SYMBOL_RATE = LOCK_PARAMETER[1]
        CN = LOCK_PARAMETER[2]

        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_constellation_dvbc(MODULATION)
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_symbolrate_dvbc(SYMBOL_RATE[0])
        specan = Ektsfu(sfu_ip)
        specan.set_noise_awgn_cn(str(CN))

        for PARAMETER in LOCK_PARAMETER[3]:
            if PARAMETER[1] == None or PARAMETER[2] == None:
                pass
            else:
                continue

            FREQUENCY_LEVEL_OFFSET = PARAMETER[0]

            specan = Ektsfu(sfu_ip)
            specan.set_frequency_frequency_frequency(str(FREQUENCY_LEVEL_OFFSET[0]) + "MHz")
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

            net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
            net.send_data(json.dumps({"cmd": "set_modulation_data", "modulation": MODULATION}))
            time.sleep(1)
            del net

            """
            触发stb-tester进行频率和符号率设置
            """
            stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                        ekt_cfg.DVB_C_LOCK_FUNCTION, ekt_cfg.DVB_C_CATEGORY, ekt_cfg.DVB_C_REMOTE)

            net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)

            lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
            if lock_state == "1":
                pass
            elif lock_state == "0":
                write_test_result("../../ekt_log/test_result_sfu.txt",
                                  (
                                          "dvbc_1_dynamic_range_awng_min_level: current_time:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, {}".format(
                                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                              str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                                              str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])),
                                              "Lock fail") + "\n"))
                continue
            elif lock_state == "2":
                write_test_result("../../ekt_log/test_result_sfu.txt",
                                  (
                                          "dvbc_1_dynamic_range_awng_min_level: current_time:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, {}".format(
                                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                              str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                                              str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])),
                                              "Frequency points are not supported") + "\n"))
                PARAMETER[1] = "Frequency points are not supported"
                write_json_file("../../ekt_json/dvbc_1_dynamic_range_awng_min_level.json", load_dict)
                dvbc_1_dynamic_range_awng_min_level_json_to_csv("../../ekt_json/dvbc_1_dynamic_range_awng_min_level.json",
                                                                "../../ekt_test_report/dvbc_1_dynamic_range_awng_min_level.csv")
                continue
            else:
                write_test_result("../../ekt_log/test_result_sfu.txt", ("Lock state err" + "\n"))
                continue

            start_data_result, mosaic_result = mosaic_algorithm(sfu_ip, str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])), "-10")
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              "dvbc_1_dynamic_range_awng_min_level: current_time:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, Mosaic results:{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                  str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                                  str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])),
                                  start_data_result.get("detect_mosic_result")) + "\n")
            PARAMETER[2] = mosaic_result

            res, test_result = iterate_to_find_threshold_step_by_step_dvbs2(sfu_ip, (test_start_level - FREQUENCY_LEVEL_OFFSET[1]),
                                                                            level_offset=str(FREQUENCY_LEVEL_OFFSET[1]))
            print (
                "dvbc_1_dynamic_range_awng_min_level: current_time:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,{}".format(
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]), res))
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              "dvbc_1_dynamic_range_awng_min_level: current_time:{}, frequency:{} MHz,symbol_rate:{} Ksym/s, {}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                  str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]), res) + "\n")

            PARAMETER[1] = test_result

            DVBC_1_SPEC = None
            if MODULATION == MODULATION_64QAM:
                DVBC_1_SPEC = ekt_cfg.DVBC_1_C64_SPEC
            elif MODULATION == MODULATION_256QAM:
                DVBC_1_SPEC = ekt_cfg.DVBC_1_C256_SPEC
            else:
                print "Illegal data {}".format(MODULATION)

            if test_result is None:
                pass
            elif float(test_result) <= DVBC_1_SPEC:
                PARAMETER[3] = "Pass"
            elif float(test_result) > DVBC_1_SPEC:
                PARAMETER[3] = "Fail"
            else:
                PARAMETER[3] = "test result err"
            write_json_file("../../ekt_json/dvbc_1_dynamic_range_awng_min_level.json", load_dict)
            dvbc_1_dynamic_range_awng_min_level_json_to_csv("../../ekt_json/dvbc_1_dynamic_range_awng_min_level.json",
                                                            "../../ekt_test_report/dvbc_1_dynamic_range_awng_min_level.csv")

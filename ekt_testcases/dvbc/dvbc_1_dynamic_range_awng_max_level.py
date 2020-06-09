#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import datetime
from ekt_lib import ekt_net, ekt_cfg
from ekt_lib.ekt_sfu import Ektsfu
from pathlib2 import Path
from ekt_lib.ekt_stb_tester import stb_tester_execute_testcase
from ekt_lib.threshold_algorithm_SFU import mosaic_algorithm
from ekt_lib.ekt_utils import write_test_result, read_ekt_config_data, write_json_file, read_json_file, \
    dvbc_1_dynamic_range_awng_max_level_json_to_csv

MODULATION_64QAM = "C64"
MODULATION_256QAM = "C256"

SYMBOL_RATE_6952 = ["6.952e6", "6952"]

PARAMETER_LIST = [
    [MODULATION_64QAM, SYMBOL_RATE_6952, 27],
    [MODULATION_256QAM, SYMBOL_RATE_6952, 35],
]

my_file = Path("../../ekt_json/dvbc_1_dynamic_range_awng_max_level.json")
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
            list_test_result.append([FREQUENCY_LEVEL_OFFSET, None])
        list_test_parame_result.append([PARAMETER[0], PARAMETER[1], PARAMETER[2], list_test_result])
    dict_test_parame_result["test_parame_result"] = list_test_parame_result

    write_json_file("../../ekt_json/dvbc_1_dynamic_range_awng_max_level.json", dict_test_parame_result)

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
    load_dict = read_json_file("../../ekt_json/dvbc_1_dynamic_range_awng_max_level.json")
    sfu_ip = "192.168.1.50"
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
            if PARAMETER[1] == None:
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

            net = ekt_net.EktNetClient('192.168.1.24', 9999)
            net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": str(FREQUENCY_LEVEL_OFFSET[0])}))
            time.sleep(1)
            del net
            net = ekt_net.EktNetClient('192.168.1.24', 9999)
            net.send_data(json.dumps({"cmd": "set_symbol_rate_data", "symbol_rate": str(SYMBOL_RATE[1])}))
            time.sleep(1)
            del net

            """
            触发stb-tester进行频率和符号率设置
            """
            try:
                stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                            ["tests/front_end_test/testcases.py::test_continuous_button_7514i"], "auto_front_end_test",
                                            "dcn7514i")
            except:
                time.sleep(60)
                stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                            ["tests/front_end_test/testcases.py::test_continuous_button_7514i"], "auto_front_end_test",
                                            "dcn7514i")
            net = ekt_net.EktNetClient('192.168.1.24', 9999)

            lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
            if lock_state == "1":
                pass
            elif lock_state == "0":
                write_test_result("../../ekt_log/test_result_sfu.txt",
                                  (
                                          "dvbc_1_dynamic_range_awng_max_level: current_time:{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, {}".format(
                                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                              str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                                              str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])),
                                              "锁台失败") + "\n"))
                continue
            elif lock_state == "2":
                write_test_result("../../ekt_log/test_result_sfu.txt",
                                  (
                                          "dvbc_1_dynamic_range_awng_max_level: current_time:{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, {}".format(
                                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                              str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                                              str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])),
                                              "频点不支持") + "\n"))
                PARAMETER[1] = "Frequency points are not supported"
                write_json_file("../../ekt_json/dvbc_1_dynamic_range_awng_max_level.json", load_dict)
                dvbc_1_dynamic_range_awng_max_level_json_to_csv("../../ekt_json/dvbc_1_dynamic_range_awng_max_level.json",
                                                                "../../ekt_test_report/dvbc_1_dynamic_range_awng_max_level.csv")
                continue
            else:
                write_test_result("../../ekt_log/test_result_sfu.txt", ("出错了" + "\n"))
                continue

            start_data_result, mosaic_result = mosaic_algorithm(sfu_ip, str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])), "-10")
            print (
                "dvbc_1_dynamic_range_awng_max_level: current_time:{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, 马赛克检测结果：{}".format(
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                    str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])),
                    start_data_result.get("detect_mosic_result")))
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              "dvbc_1_dynamic_range_awng_max_level: current_time:{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, 马赛克检测结果：{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                  str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                                  str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])),
                                  start_data_result.get("detect_mosic_result")) + "\n")

            PARAMETER[1] = mosaic_result
            write_json_file("../../ekt_json/dvbc_1_dynamic_range_awng_max_level.json", load_dict)
            dvbc_1_dynamic_range_awng_max_level_json_to_csv("../../ekt_json/dvbc_1_dynamic_range_awng_max_level.json",
                                                            "../../ekt_test_report/dvbc_1_dynamic_range_awng_max_level.csv")

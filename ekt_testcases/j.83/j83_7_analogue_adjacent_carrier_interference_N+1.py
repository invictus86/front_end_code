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
from ekt_lib.threshold_algorithm_SFU import iterate_to_find_threshold_step_by_step_dvbs2
from ekt_lib.ekt_utils import write_test_result, read_ekt_config_data, write_json_file, read_json_file, find_level_offset_by_frequency, \
    j83_7_analogue_adjacent_carrier_interference_N_1_json_to_csv

MODULATION_64QAM = "J64"
MODULATION_256QAM = "J256"

SYMBOL_RATE_5057 = ["5.057e6", "5057"]
SYMBOL_RATE_5361 = ["5.361e6", "5361"]

PARAMETER_LIST = [
    [MODULATION_64QAM, SYMBOL_RATE_5057, 21],
    [MODULATION_256QAM, SYMBOL_RATE_5361, 11],
]

FREQUENCY_LIST = [60, 474, 666, 852]

my_file = Path("../../ekt_json/j83_7_analogue_adjacent_carrier_interference_N_1.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    list_test_parame_result = []

    for PARAMETER in PARAMETER_LIST:
        list_test_result = []
        for FREQUENCY in FREQUENCY_LIST:
            list_test_result.append([FREQUENCY, None])
        list_test_parame_result.append([PARAMETER[0], PARAMETER[1], PARAMETER[2], list_test_result])
    dict_test_parame_result["test_parame_result"] = list_test_parame_result

    write_json_file("../../ekt_json/j83_7_analogue_adjacent_carrier_interference_N_1.json", dict_test_parame_result)

if __name__ == '__main__':
    """
    测试流程:
    ①重置设备
    ②选择 TSPLAYER
    ③播放流文件
    ④设置modulation,symbol_rate, CN, frequency,input_signal_level
    ⑤机顶盒应用中进行锁台并确认锁台成功  （针对stb-tester发送post请求运行testcase）
    ⑤依次修改可变参数,判断机顶盒画面是否含有马赛克并记录结果
    """
    load_dict = read_json_file("../../ekt_json/j83_7_analogue_adjacent_carrier_interference_N_1.json")
    sfu_ip = ekt_cfg.SFU_IP
    specan = Ektsfu(sfu_ip)
    specan.preset_instrument()
    specan = Ektsfu(sfu_ip)
    specan.set_modulation_modulation_source("DTV")
    specan = Ektsfu(sfu_ip)
    specan.set_modulation_modulation_standard_dvt("J83B")
    specan = Ektsfu(sfu_ip)
    specan.set_player_timing_openfile(r"E:\333\DIVER.GTS")
    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_input_source_j83b("TSPLayer")
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_rf("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_noise_noise_noise("OFF")
    # specan = Ektsfu(sfu_ip)
    # specan.set_noise_noise_awgn("ON")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_modulator("OFF")
    specan = Ektsfu(sfu_ip)
    specan.set_impairments_baseband("OFF")

    specan = Ektsfu(sfu_ip)
    specan.set_interferer_source("ATVPr")
    specan = Ektsfu(sfu_ip)
    specan.set_interferer_reference("LEV")
    specan = Ektsfu(sfu_ip)
    specan.set_interferer_level("-25")
    specan = Ektsfu(sfu_ip)
    specan.set_interferer_frequency_offset(str(5.25))

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
        # CN = LOCK_PARAMETER[2]

        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_constellation_j83b(MODULATION)
        # specan = Ektsfu(sfu_ip)
        # specan.set_digitaltv_coding_symbolrate_j83b(SYMBOL_RATE[0])
        # specan = Ektsfu(sfu_ip)
        # specan.set_noise_awgn_cn(str(CN))

        for PARAMETER in LOCK_PARAMETER[3]:
            if PARAMETER[1] == None:
                pass
            else:
                continue

            FREQUENCY_LEVEL_OFFSET = [PARAMETER[0], find_level_offset_by_frequency("ANNEXB_FREQUENCY_LEVEL_OFFSET", PARAMETER[0])]

            specan = Ektsfu(sfu_ip)
            specan.set_frequency_frequency_frequency(str(FREQUENCY_LEVEL_OFFSET[0]) + "MHz")
            specan = Ektsfu(sfu_ip)
            specan.set_level_level_offset(str(FREQUENCY_LEVEL_OFFSET[1]))
            specan = Ektsfu(sfu_ip)
            specan.set_level_level_level("dBm", str("%.2f" % ((-25) - FREQUENCY_LEVEL_OFFSET[1])))

            net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
            net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": str(FREQUENCY_LEVEL_OFFSET[0])}))
            time.sleep(1)
            del net
            net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
            net.send_data(json.dumps({"cmd": "set_symbol_rate_data", "symbol_rate": str(SYMBOL_RATE[1])}))
            time.sleep(1)
            del net
            net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
            net.send_data(json.dumps({"cmd": "set_modulation_data", "modulation": str(MODULATION)}))
            time.sleep(1)
            del net

            """
            触发stb-tester进行频率和符号率设置
            """
            stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                        ekt_cfg.DVB_J83_LOCK_FUNCTION, ekt_cfg.DVB_J83_CATEGORY, ekt_cfg.DVB_J83_REMOTE)

            net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)

            lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
            if lock_state == "1":
                pass
            elif lock_state == "0":
                write_test_result("../../ekt_log/test_result_sfu.txt",
                                  (
                                          "j83_7_analogue_adjacent_carrier_interference_N_1: current_time:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, {}".format(
                                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                              str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                                              str("%.2f" % ((-25) - FREQUENCY_LEVEL_OFFSET[1])),
                                              "Lock fail") + "\n"))
                continue
            elif lock_state == "2":
                write_test_result("../../ekt_log/test_result_sfu.txt",
                                  (
                                          "j83_7_analogue_adjacent_carrier_interference_N_1: current_time:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, {}".format(
                                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                              str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                                              str("%.2f" % ((-25) - FREQUENCY_LEVEL_OFFSET[1])),
                                              "Frequency points are not supported") + "\n"))
                PARAMETER[1] = "Frequency points are not supported"
                write_json_file("../../ekt_json/j83_7_analogue_adjacent_carrier_interference_N_1.json", load_dict)
                j83_7_analogue_adjacent_carrier_interference_N_1_json_to_csv(
                    "../../ekt_json/j83_7_analogue_adjacent_carrier_interference_N_1.json",
                    "../../ekt_test_report/j83_7_analogue_adjacent_carrier_interference_N_1.csv")
                continue
            else:
                write_test_result("../../ekt_log/test_result_sfu.txt", ("Lock state err" + "\n"))
                continue

            res, test_result = iterate_to_find_threshold_step_by_step_dvbs2(sfu_ip, (-25 - FREQUENCY_LEVEL_OFFSET[1]),
                                                                            level_offset=str(FREQUENCY_LEVEL_OFFSET[1]))
            print (
                "j83_7_analogue_adjacent_carrier_interference_N_1: current_time:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,{}".format(
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]), res))
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              "j83_7_analogue_adjacent_carrier_interference_N_1: current_time:{}, frequency:{} MHz,symbol_rate:{} Ksym/s, {}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                  str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]), res) + "\n")

            PARAMETER[1] = str(-25 - float(test_result))
            write_json_file("../../ekt_json/j83_7_analogue_adjacent_carrier_interference_N_1.json", load_dict)
            j83_7_analogue_adjacent_carrier_interference_N_1_json_to_csv(
                "../../ekt_json/j83_7_analogue_adjacent_carrier_interference_N_1.json",
                "../../ekt_test_report/j83_7_analogue_adjacent_carrier_interference_N_1.csv")

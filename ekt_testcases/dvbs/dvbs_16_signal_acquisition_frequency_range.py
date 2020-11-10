#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import datetime
import os, sys

parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parentdir)
from ekt_lib import ekt_net, ekt_cfg
from ekt_lib.ekt_sfe import Ektsfe
from pathlib2 import Path
from ekt_lib.ekt_stb_tester import stb_tester_execute_testcase
from ekt_lib.threshold_algorithm_SFE import mosaic_algorithm
from ekt_lib.ekt_utils import write_test_result, read_ekt_config_data, find_level_offset_by_frequency, write_json_file, read_json_file, \
    dvbs_signal_acquisition_frequency_range_json_to_csv

CODE_RATE_LIST = ["R1_2", "R2_3", "R3_4", "R5_6", "R7_8"]

MODULATION_QPSK = "S4"
LEVEL_OFFSET_950 = find_level_offset_by_frequency("DVBS_S2_FREQUENCY_LEVEL_OFFSET", 950)
LEVEL_50_950 = str("%.2f" % ((-50) - LEVEL_OFFSET_950))
LEVEL_OFFSET_1550 = find_level_offset_by_frequency("DVBS_S2_FREQUENCY_LEVEL_OFFSET", 1550)
LEVEL_50_1550 = str("%.2f" % ((-50) - LEVEL_OFFSET_1550))
LEVEL_OFFSET_2150 = find_level_offset_by_frequency("DVBS_S2_FREQUENCY_LEVEL_OFFSET", 2150)
LEVEL_50_2150 = str("%.2f" % ((-50) - LEVEL_OFFSET_2150))

SYMBOL_RATE_FREQUENCY_5M = ["5.000000e6", "05000", [["950", "951", LEVEL_50_950], ["950", "949", LEVEL_50_950],
                                                    ["1550", "1551", LEVEL_50_1550], ["1550", "1549", LEVEL_50_1550],
                                                    ["2150", "2151", LEVEL_50_2150], ["2150", "2149", LEVEL_50_2150]]]
SYMBOL_RATE_FREQUENCY_27_5M = ["27.500000e6", "27500",
                               [["950", "952.75", LEVEL_50_950], ["950", "947.25", LEVEL_50_950],
                                ["1550", "1552.75", LEVEL_50_1550], ["1550", "1547.25", LEVEL_50_1550],
                                ["2150", "2152.25", LEVEL_50_2150], ["2150", "2147.25", LEVEL_50_2150]]]
SYMBOL_RATE_FREQUENCY_45M = ["45.000000e6", "45000", [["950", "954.5", LEVEL_50_950], ["950", "945.5", LEVEL_50_950],
                                                      ["1550", "1554.5", LEVEL_50_1550], ["1550", "1545.5", LEVEL_50_1550],
                                                      ["2150", "2154.5", LEVEL_50_2150], ["2150", "2145.5", LEVEL_50_2150]]]

dict_config_data = {
    "SYMBOL_RATE_FREQUENCY": [SYMBOL_RATE_FREQUENCY_5M, SYMBOL_RATE_FREQUENCY_27_5M, SYMBOL_RATE_FREQUENCY_45M]}

my_file = Path("../../ekt_json/dvbs_16_signal_acquisition_frequency_range.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    list_test_parame_result = []

    dict_data = read_ekt_config_data("../../ekt_lib/ekt_config.json")
    DVBS_S2_FREQUENCY_LEVEL_OFFSET = dict_data.get("DVBS_S2_FREQUENCY_LEVEL_OFFSET")
    DVBS_QPSK_CODE_RATE_CN = dict_data.get("DVBS_QPSK_CODE_RATE_CN")

    for SYMBOL_RATE_FREQUENCY in dict_config_data.get("SYMBOL_RATE_FREQUENCY"):
        for FREQUENCY_OFFSET in SYMBOL_RATE_FREQUENCY[2]:
            list_test_result = []
            for code_rate_cn in CODE_RATE_LIST:
                list_test_result.append([code_rate_cn, None])
            list_test_parame_result.append([SYMBOL_RATE_FREQUENCY[0], SYMBOL_RATE_FREQUENCY[1], FREQUENCY_OFFSET, list_test_result])
    dict_test_parame_result["test_parame_result"] = list_test_parame_result

    write_json_file("../../ekt_json/dvbs_16_signal_acquisition_frequency_range.json", dict_test_parame_result)


def sfe_init_setting():
    """
    sfe init setting
    :return:
    """
    sfe_ip = ekt_cfg.SFE_IP
    specan = Ektsfe(sfe_ip)
    specan.clean_reset()
    specan = Ektsfe(sfe_ip)
    specan.preset_instrument()
    specan = Ektsfe(sfe_ip)
    specan.set_digitaltv_input_source("TSPL")
    specan = Ektsfe(sfe_ip)
    specan.set_digitaltv_input_load(r"D:\TSGEN\SDTV\DVB_25Hz\720_576i\LIVE\DIVER.GTS")


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
    load_dict = read_json_file("../../ekt_json/dvbs_16_signal_acquisition_frequency_range.json")
    sfe_ip = ekt_cfg.SFE_IP
    sfe_init_setting()

    for PARAMETER in load_dict.get("test_parame_result"):
        loop_lock_mark = False
        for check_list in PARAMETER[3]:
            if check_list[1] == None:
                loop_lock_mark = True
                break
        if loop_lock_mark == True:
            pass
        else:
            continue
        FREQUENCY_OFFSET = PARAMETER[2]
        SYMBOL_RATE_FREQUENCY = [PARAMETER[0], PARAMETER[1]]

        specan = Ektsfe(sfe_ip)
        specan.set_digitaltv_coding_symbolrate(SYMBOL_RATE_FREQUENCY[0])

        specan = Ektsfe(sfe_ip)
        specan.set_frequency_frequency_frequency(FREQUENCY_OFFSET[1] + "MHz")
        specan = Ektsfe(sfe_ip)
        specan.set_level_level_level(FREQUENCY_OFFSET[2] + " dBm")

        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": FREQUENCY_OFFSET[0]}))
        time.sleep(1)
        del net
        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        net.send_data(json.dumps({"cmd": "set_symbol_rate_data", "symbol_rate": str(SYMBOL_RATE_FREQUENCY[1])}))
        time.sleep(1)
        del net

        """
        触发stb-tester进行频率和符号率设置
        """
        stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                    ekt_cfg.DVB_S_LOCK_FUNCTION, ekt_cfg.DVB_S_CATEGORY, ekt_cfg.DVB_S_REMOTE)
        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
        if lock_state == "1":
            pass
        elif lock_state == "0":
            write_test_result("../../ekt_log/test_result_sfe.txt",
                              (
                                      "dvbs_16_signal_acquisition_frequency_range: current_time:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, {}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          FREQUENCY_OFFSET[1], SYMBOL_RATE_FREQUENCY[1],
                                          FREQUENCY_OFFSET[2], "Lock fail") + "\n"))
            continue
        else:
            write_test_result("../../ekt_log/test_result_sfe.txt", ("Lock state err" + "\n"))
            continue

        for code_rate_cn in PARAMETER[3]:
            if code_rate_cn[1] == None:
                pass
            else:
                continue

            specan = Ektsfe(sfe_ip)
            specan.set_digitaltv_coding_coderate(code_rate_cn[0])
            time.sleep(1)

            start_data_result, mosaic_result = mosaic_algorithm(sfe_ip, FREQUENCY_OFFSET[2], "-50")
            print (
                "dvbs_16_signal_acquisition_frequency_range: current_time:{}, coderate:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, Mosaic results:{}".format(
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn[0],
                    FREQUENCY_OFFSET[1], SYMBOL_RATE_FREQUENCY[1], FREQUENCY_OFFSET[2],
                    start_data_result.get("detect_mosic_result")))
            write_test_result("../../ekt_log/test_result_sfe.txt",
                              "dvbs_16_signal_acquisition_frequency_range: current_time:{}, coderate:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,level:{} dbm, Mosaic results:{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn[0],
                                  FREQUENCY_OFFSET[1], SYMBOL_RATE_FREQUENCY[1], FREQUENCY_OFFSET[2],
                                  start_data_result.get("detect_mosic_result")) + "\n")

            # 判断sfe是否在测试过程中重启，否则设置测试结果为none
            net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
            sfe_state = net.send_rec(json.dumps({"cmd": "get_sfe_state"}))
            if sfe_state == "crash":
                mosaic_result = None
                net.send_data(json.dumps({"cmd": "set_sfe_state", "sfe_state": "noral"}))
                time.sleep(0.5)
                del net
                sfe_init_setting()

            code_rate_cn[1] = mosaic_result
            write_json_file("../../ekt_json/dvbs_16_signal_acquisition_frequency_range.json", load_dict)
            dvbs_signal_acquisition_frequency_range_json_to_csv("../../ekt_json/dvbs_16_signal_acquisition_frequency_range.json",
                                                                "../../ekt_test_report/dvbs_16_signal_acquisition_frequency_range.csv")

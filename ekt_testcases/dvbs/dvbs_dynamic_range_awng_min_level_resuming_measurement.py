#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import json
import datetime
from ekt_lib import ekt_net, ekt_cfg
from ekt_lib.ekt_sfe import Ektsfe
from pathlib2 import Path
from ekt_lib.ekt_stb_tester import stb_tester_execute_testcase
from ekt_lib.threshold_algorithm_SFE import iterate_to_find_threshold_step_by_step
from ekt_lib.ekt_utils import write_test_result, read_ekt_config_data, write_json_file, read_json_file, \
    dvbs_dynamic_min_json_to_csv

my_file = Path("../../ekt_json/dvbs_dynamic_range_awng_min_level_resuming_measurement.json")
if my_file.exists():
    pass
else:
    SYMBOL_RATE_5M = ["5.000000e6", "05000"]
    SYMBOL_RATE_10M = ["10.000000e6", "10000"]
    SYMBOL_RATE_27_5M = ["27.500000e6", "27500"]
    SYMBOL_RATE_45M = ["45.000000e6", "45000"]

    dict_config_data = {
        "SYMBOL_RATE": [SYMBOL_RATE_5M, SYMBOL_RATE_10M, SYMBOL_RATE_27_5M, SYMBOL_RATE_45M]}

    dict_test_parame_result = {}
    list_test_parame_result = []

    dict_data = read_ekt_config_data("../../ekt_lib/ekt_config.json")
    DVBS_S2_FREQUENCY_LEVEL_OFFSET = dict_data.get("DVBS_S2_FREQUENCY_LEVEL_OFFSET")
    DVBS_QPSK_CODE_RATE_CN = dict_data.get("DVBS_QPSK_CODE_RATE_CN")

    for SYMBOL_RATE in dict_config_data.get("SYMBOL_RATE"):
        for FREQUENCY_LEVEL_OFFSET in DVBS_S2_FREQUENCY_LEVEL_OFFSET:
            list_test_result = []
            for code_rate_cn in DVBS_QPSK_CODE_RATE_CN:
                list_test_result.append([code_rate_cn, None])
            list_test_parame_result.append([SYMBOL_RATE, FREQUENCY_LEVEL_OFFSET, list_test_result])

    dict_test_parame_result["test_parame_result"] = list_test_parame_result
    print dict_test_parame_result

    write_json_file("../../ekt_json/dvbs_dynamic_range_awng_min_level_resuming_measurement.json",
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
    load_dict = read_json_file("../../ekt_json/dvbs_dynamic_range_awng_min_level_resuming_measurement.json")
    sfe_ip = "192.168.1.47"
    specan = Ektsfe(sfe_ip)
    specan.clean_reset()
    specan = Ektsfe(sfe_ip)
    specan.preset_instrument()
    # specan.timeout = 2000
    specan = Ektsfe(sfe_ip)
    specan.set_digitaltv_input_source("TSPL")
    specan = Ektsfe(sfe_ip)
    specan.set_digitaltv_input_load(r"D:\TSGEN\SDTV\DVB_25Hz\720_576i\LIVE\DIVER.GTS")

    dict_data = read_ekt_config_data("../../ekt_lib/ekt_config.json")
    DVBS_S2_FREQUENCY_LEVEL_OFFSET = dict_data.get("DVBS_S2_FREQUENCY_LEVEL_OFFSET")
    DVBS_QPSK_CODE_RATE_CN = dict_data.get("DVBS_QPSK_CODE_RATE_CN")
    # DVBS2_8PSK_CODE_RATE_CN = dict_data.get("DVBS2_8PSK_CODE_RATE_CN")

    for lock_parame_index in range(len(load_dict.get("test_parame_result"))):
        loop_lock_mark = False
        for check_list in load_dict.get("test_parame_result")[lock_parame_index][2]:
            if check_list[1] == None:
                loop_lock_mark = True
                break
        if loop_lock_mark == True:
            pass
        else:
            continue

        # del specan
        specan = Ektsfe(sfe_ip)
        specan.set_digitaltv_coding_symbolrate(load_dict.get("test_parame_result")[lock_parame_index][0][0])
        # for FREQUENCY_LEVEL_OFFSET in DVBS_S2_FREQUENCY_LEVEL_OFFSET:
        #     del specan
        specan = Ektsfe(sfe_ip)
        specan.set_frequency_frequency_frequency(
            str(load_dict.get("test_parame_result")[lock_parame_index][1][0]) + "MHz")
        specan = Ektsfe(sfe_ip)
        specan.set_level_level_level("-50 dBm")

        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(json.dumps({"cmd": "set_frequency_data",
                                  "frequency": str(load_dict.get("test_parame_result")[lock_parame_index][1][0])}))
        time.sleep(1)
        del net
        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(json.dumps({"cmd": "set_symbol_rate_data",
                                  "symbol_rate": str(load_dict.get("test_parame_result")[lock_parame_index][0][1])}))
        time.sleep(1)
        del net

        """
        触发stb-tester进行频率和符号率设置
        """
        stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                    ["tests/front_end_test/testcases.py::test_continuous_button"],
                                    "auto_front_end_test", "DSD4614iALM")
        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
        if lock_state == "1":
            pass
        elif lock_state == "0":
            write_test_result("../../ekt_log/test_result_sfe.txt",
                              (
                                      "dvbs_dynamic_range_awng_min_level: current_time:{}, frequency：{} MHz，symbol_rate：{} Ksym/s，{}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          str(load_dict.get("test_parame_result")[lock_parame_index][1][0]),
                                          str(load_dict.get("test_parame_result")[lock_parame_index][0][1]),
                                          "锁台失败") + "\n"))
            continue
        else:
            write_test_result("../../ekt_log/test_result_sfe.txt", ("出错了" + "\n"))
            continue

        for no_lock_parame_index in range(len(load_dict.get("test_parame_result")[lock_parame_index][2])):
            if load_dict.get("test_parame_result")[lock_parame_index][2][no_lock_parame_index][1] == None:
                pass
            else:
                continue
            specan = Ektsfe(sfe_ip)
            specan.set_level_level_level("-50 dBm")
            time.sleep(10)
            specan = Ektsfe(sfe_ip)
            specan.set_digitaltv_coding_coderate(
                load_dict.get("test_parame_result")[lock_parame_index][2][no_lock_parame_index][0][0])
            # try:
            res, test_result = iterate_to_find_threshold_step_by_step(sfe_ip,
                                                                      float((-70) -
                                                                            load_dict.get("test_parame_result")[
                                                                                lock_parame_index][2][
                                                                                no_lock_parame_index][0][1]),
                                                                      level_offset=str(
                                                                          load_dict.get("test_parame_result")[
                                                                              lock_parame_index][2][
                                                                              no_lock_parame_index][0][1]))
            print "dvbs_dynamic_range_awng_min_level: current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                load_dict.get("test_parame_result")[lock_parame_index][2][no_lock_parame_index][0][0],
                str(load_dict.get("test_parame_result")[lock_parame_index][1][0]),
                str(load_dict.get("test_parame_result")[lock_parame_index][0][1]), res)
            write_test_result("../../ekt_log/test_result_sfe.txt",
                              "dvbs_dynamic_range_awng_min_level: current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                  load_dict.get("test_parame_result")[lock_parame_index][2][no_lock_parame_index][
                                      0][0],
                                  str(load_dict.get("test_parame_result")[lock_parame_index][1][0]),
                                  str(load_dict.get("test_parame_result")[lock_parame_index][0][1]), res) + "\n")
            load_dict.get("test_parame_result")[lock_parame_index][2][no_lock_parame_index][1] = test_result
            write_json_file("../../ekt_json/dvbs_dynamic_range_awng_min_level_resuming_measurement.json",
                            load_dict)
            dvbs_dynamic_min_json_to_csv("../../ekt_json/dvbs_dynamic_range_awng_min_level_resuming_measurement.json",
                                         "../../ekt_test_report/dvbs_dynamic_range_awng_min_level_resuming_measurement.csv")

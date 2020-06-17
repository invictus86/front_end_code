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
from ekt_lib.threshold_algorithm_SFE import iterate_to_find_threshold_step_by_step, mosaic_algorithm
from ekt_lib.ekt_utils import write_test_result, read_ekt_config_data, write_json_file, read_json_file, \
    dvbs_dynamic_min_json_to_csv, dvbs_dynamic_min_json_class_test

SYMBOL_RATE_5M = ["5.000000e6", "05000"]
SYMBOL_RATE_10M = ["10.000000e6", "10000"]
SYMBOL_RATE_27_5M = ["27.500000e6", "27500"]
SYMBOL_RATE_45M = ["45.000000e6", "45000"]

dict_config_data = {
    "SYMBOL_RATE": [SYMBOL_RATE_5M, SYMBOL_RATE_10M, SYMBOL_RATE_27_5M, SYMBOL_RATE_45M]}

my_file = Path("../../ekt_json/dvbs_11_dynamic_range_awng_min_level.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    list_test_parame_result = []

    dict_data = read_ekt_config_data("../../ekt_lib/ekt_config.json")
    DVBS_S2_FREQUENCY_LEVEL_OFFSET = dict_data.get("DVBS_S2_FREQUENCY_LEVEL_OFFSET")
    DVBS_QPSK_CODE_RATE_CN = dict_data.get("DVBS_QPSK_CODE_RATE_CN")

    for SYMBOL_RATE in dict_config_data.get("SYMBOL_RATE"):
        for FREQUENCY_LEVEL_OFFSET in DVBS_S2_FREQUENCY_LEVEL_OFFSET:
            list_test_result = []
            for code_rate_cn in DVBS_QPSK_CODE_RATE_CN:
                list_test_result.append([code_rate_cn, None, None])
            list_test_parame_result.append([SYMBOL_RATE, FREQUENCY_LEVEL_OFFSET, list_test_result])
    dict_test_parame_result["test_parame_result"] = list_test_parame_result

    write_json_file("../../ekt_json/dvbs_11_dynamic_range_awng_min_level.json", dict_test_parame_result)

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
    # 将部分无需测试的点的json文件内容, 测试结果置为 NO NEED TEST
    dvbs_dynamic_min_json_class_test("../../ekt_json/dvbs_11_dynamic_range_awng_min_level.json")

    load_dict = read_json_file("../../ekt_json/dvbs_11_dynamic_range_awng_min_level.json")
    sfe_ip = "192.168.1.47"
    specan = Ektsfe(sfe_ip)
    specan.clean_reset()
    specan = Ektsfe(sfe_ip)
    specan.preset_instrument()
    specan = Ektsfe(sfe_ip)
    specan.set_digitaltv_input_source("TSPL")
    specan = Ektsfe(sfe_ip)
    specan.set_digitaltv_input_load(r"D:\TSGEN\SDTV\DVB_25Hz\720_576i\LIVE\DIVER.GTS")

    for PARAMETER in load_dict.get("test_parame_result"):
        loop_lock_mark = False
        for check_list in PARAMETER[2]:
            if check_list[1] == None:
                loop_lock_mark = True
                break
        if loop_lock_mark == True:
            pass
        else:
            continue

        SYMBOL_RATE = PARAMETER[0]
        FREQUENCY_LEVEL_OFFSET = PARAMETER[1]

        specan = Ektsfe(sfe_ip)
        specan.set_digitaltv_coding_symbolrate(SYMBOL_RATE[0])

        specan = Ektsfe(sfe_ip)
        specan.set_frequency_frequency_frequency(str(FREQUENCY_LEVEL_OFFSET[0]) + "MHz")
        specan = Ektsfe(sfe_ip)
        specan.set_level_level_level("-10 dBm")

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
                                    ekt_cfg.DVB_S_LOCK_FUNCTION, ekt_cfg.DVB_S_CATEGORY, ekt_cfg.DVB_S_REMOTE)
        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
        if lock_state == "1":
            pass
        elif lock_state == "0":
            write_test_result("../../ekt_log/test_result_sfe.txt",
                              (
                                      "dvbs_11_dynamic_range_awng_min_level: current_time:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,{}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]),
                                          "Lock fail") + "\n"))
            continue
        else:
            write_test_result("../../ekt_log/test_result_sfe.txt", ("Lock state err" + "\n"))
            continue
        for code_rate_cn in PARAMETER[2]:
            if code_rate_cn[1] == None:
                pass
            else:
                continue

            specan = Ektsfe(sfe_ip)
            specan.set_digitaltv_coding_coderate(code_rate_cn[0][0])
            specan = Ektsfe(sfe_ip)
            specan.set_level_level_level(str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])) + " dBm")
            time.sleep(5)

            _, mosaic_result = mosaic_algorithm(sfe_ip, str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])),
                                                str("%.2f" % ((-10) - FREQUENCY_LEVEL_OFFSET[1])))
            if mosaic_result == "Fail":
                mosaic_result = None

            code_rate_cn[2] = mosaic_result
            write_json_file("../../ekt_json/dvbs_11_dynamic_range_awng_min_level.json", load_dict)

            specan = Ektsfe(sfe_ip)
            specan.set_level_level_level("-50 dBm")

            res, test_result = iterate_to_find_threshold_step_by_step(sfe_ip,
                                                                      float((-70) - FREQUENCY_LEVEL_OFFSET[1]),
                                                                      level_offset=str(FREQUENCY_LEVEL_OFFSET[1]))
            print ("dvbs_11_dynamic_range_awng_min_level: current_time:{}, coderate:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn[0][0],
                str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]), res))
            write_test_result("../../ekt_log/test_result_sfe.txt",
                              "dvbs_11_dynamic_range_awng_min_level: current_time:{}, coderate:{}, frequency:{} MHz,symbol_rate:{} Ksym/s,{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), code_rate_cn[0][0],
                                  str(FREQUENCY_LEVEL_OFFSET[0]), str(SYMBOL_RATE[1]), res) + "\n")
            code_rate_cn[1] = test_result
            write_json_file("../../ekt_json/dvbs_11_dynamic_range_awng_min_level.json", load_dict)
            dvbs_dynamic_min_json_to_csv("../../ekt_json/dvbs_11_dynamic_range_awng_min_level.json",
                                         "../../ekt_test_report/dvbs_11_dynamic_range_awng_min_level.csv")

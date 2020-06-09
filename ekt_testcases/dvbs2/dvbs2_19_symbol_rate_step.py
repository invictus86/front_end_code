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
from ekt_lib.ekt_utils import write_test_result, find_level_offset_by_frequency, write_json_file, read_json_file, \
    dvbs2_19_symbol_rate_step_json_to_csv, generate_symbol_rate_list

CODE_RATE_3_4 = "R3_4"
MODULATION_8PSK = "S8"
FREQUENCY_1550 = "1550"
CN = "8.9"
LEVEL_OFFSET = find_level_offset_by_frequency("DVBS_S2_FREQUENCY_LEVEL_OFFSET", int(FREQUENCY_1550))
LEVEL_65 = str("%.2f" % ((-65) - LEVEL_OFFSET))

SYMBOL_RATE_LIST = generate_symbol_rate_list()

my_file = Path("../../ekt_json/dvbs2_19_symbol_rate_step.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    list_test_parame_result = []
    for SYMBOL_RATE in SYMBOL_RATE_LIST:
        list_test_parame_result.append([SYMBOL_RATE, None])
    dict_test_parame_result["test_parame_result"] = list_test_parame_result
    write_json_file("../../ekt_json/dvbs2_19_symbol_rate_step.json", dict_test_parame_result)

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
    load_dict = read_json_file("../../ekt_json/dvbs2_19_symbol_rate_step.json")
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
    specan.set_digitaltv_coding_constellation_dvbs2(MODULATION_8PSK)
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

    specan = Ektsfu(sfu_ip)
    specan.set_digitaltv_coding_coderate_dvbs2(CODE_RATE_3_4)
    time.sleep(1)
    specan = Ektsfu(sfu_ip)
    specan.set_noise_awgn_cn(CN)
    time.sleep(1)
    specan = Ektsfu(sfu_ip)
    specan.set_frequency_frequency_frequency(FREQUENCY_1550 + "MHz")
    time.sleep(1)
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_offset(str("-4.1"))
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_level("dBm", LEVEL_65)

    for PARAMETER in load_dict.get("test_parame_result"):
        if PARAMETER[1] == None:
            pass
        else:
            continue

        SYMBOL_RATE = PARAMETER[0]
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_symbolrate_dvbs2(SYMBOL_RATE[0])
        specan = Ektsfu(sfu_ip)
        specan.set_noise_settings_receiver("{}e6".format(str(SYMBOL_RATE[2] * 1.2)))

        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(json.dumps({"cmd": "set_frequency_data", "frequency": str(FREQUENCY_1550)}))
        time.sleep(1)
        del net
        net = ekt_net.EktNetClient('192.168.1.24', 9999)
        net.send_data(json.dumps({"cmd": "set_symbol_rate_data", "symbol_rate": str(SYMBOL_RATE[1])}))
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
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              (
                                      "dvbs2_19_symbol_rate_step: current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, {}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), CODE_RATE_3_4,
                                          FREQUENCY_1550, str(SYMBOL_RATE[1]), LEVEL_65, "锁台失败") + "\n"))
            continue
        else:
            write_test_result("../../ekt_log/test_result_sfu.txt", ("出错了" + "\n"))
            continue

        start_data_result, mosaic_result = mosaic_algorithm(sfu_ip, LEVEL_65, "-50")
        print (
        "dvbs2_19_symbol_rate_step: current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, 马赛克检测结果：{}".format(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), CODE_RATE_3_4,
            FREQUENCY_1550, str(SYMBOL_RATE[1]), LEVEL_65, start_data_result.get("detect_mosic_result")))
        write_test_result("../../ekt_log/test_result_sfu.txt",
                          "dvbs2_19_symbol_rate_step: current_time:{}, coderate：{}, frequency：{} MHz，symbol_rate：{} Ksym/s，level：{} dbm, 马赛克检测结果：{}".format(
                              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), CODE_RATE_3_4,
                              FREQUENCY_1550, str(SYMBOL_RATE[1]), LEVEL_65,
                              start_data_result.get("detect_mosic_result")) + "\n")

        PARAMETER[1] = mosaic_result
        write_json_file("../../ekt_json/dvbs2_19_symbol_rate_step.json", load_dict)
        dvbs2_19_symbol_rate_step_json_to_csv("../../ekt_json/dvbs2_19_symbol_rate_step.json",
                                          "../../ekt_test_report/dvbs2_19_symbol_rate_step.csv")

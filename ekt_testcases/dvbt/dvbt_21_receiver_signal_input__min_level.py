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
from ekt_lib.threshold_algorithm_SFU import iterate_to_find_threshold_step_by_step
from ekt_lib.ekt_utils import write_test_result, read_ekt_config_data, write_json_file, read_json_file, \
    dvbt_21_receiver_signal_input__min_level_json_to_csv, dvbt_21_receiver_signal_input__min_level_json_class_test

MODULATION_QPSK = "T4"
MODULATION_16QAM = "T16"
MODULATION_64QAM = "T64"

CODE_RATE_1_2 = "R1_2"
CODE_RATE_2_3 = "R2_3"
CODE_RATE_3_4 = "R3_4"
CODE_RATE_5_6 = "R5_6"
CODE_RATE_7_8 = "R7_8"

GUARD_G1_4 = "G1_4"
GUARD_G1_8 = "G1_8"

MODULATION_CODERATE_7M_SPEC_LIST = [
    [MODULATION_QPSK, CODE_RATE_1_2, GUARD_G1_4, -93.6],
    [MODULATION_QPSK, CODE_RATE_2_3, GUARD_G1_4, -91.8],
    [MODULATION_QPSK, CODE_RATE_3_4, GUARD_G1_4, -90.8],
    [MODULATION_QPSK, CODE_RATE_5_6, GUARD_G1_4, -89.8],
    [MODULATION_QPSK, CODE_RATE_7_8, GUARD_G1_4, -89.0],
    [MODULATION_16QAM, CODE_RATE_1_2, GUARD_G1_4, -87.9],
    [MODULATION_16QAM, CODE_RATE_2_3, GUARD_G1_4, -85.6],
    [MODULATION_16QAM, CODE_RATE_3_4, GUARD_G1_4, -84.1],
    [MODULATION_16QAM, CODE_RATE_5_6, GUARD_G1_4, -83.1],
    [MODULATION_16QAM, CODE_RATE_7_8, GUARD_G1_4, -82.7],
    [MODULATION_64QAM, CODE_RATE_1_2, GUARD_G1_4, -82.2],
    [MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_4, -80.0],
    [MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, -80.0],
    [MODULATION_64QAM, CODE_RATE_3_4, GUARD_G1_4, -78.5],
    [MODULATION_64QAM, CODE_RATE_5_6, GUARD_G1_4, -77.1],
    [MODULATION_64QAM, CODE_RATE_7_8, GUARD_G1_4, -76.2]]

MODULATION_CODERATE_8M_SPEC_LIST = [
    [MODULATION_QPSK, CODE_RATE_1_2, GUARD_G1_4, -93.1],
    [MODULATION_QPSK, CODE_RATE_2_3, GUARD_G1_4, -91.3],
    [MODULATION_QPSK, CODE_RATE_3_4, GUARD_G1_4, -90.3],
    [MODULATION_QPSK, CODE_RATE_5_6, GUARD_G1_4, -89.3],
    [MODULATION_QPSK, CODE_RATE_7_8, GUARD_G1_4, -88.5],
    [MODULATION_16QAM, CODE_RATE_1_2, GUARD_G1_4, -87.4],
    [MODULATION_16QAM, CODE_RATE_2_3, GUARD_G1_4, -85.1],
    [MODULATION_16QAM, CODE_RATE_3_4, GUARD_G1_4, -83.6],
    [MODULATION_16QAM, CODE_RATE_5_6, GUARD_G1_4, -82.6],
    [MODULATION_16QAM, CODE_RATE_7_8, GUARD_G1_4, -82.2],
    [MODULATION_64QAM, CODE_RATE_1_2, GUARD_G1_4, -81.7],
    [MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_4, -79.5],
    [MODULATION_64QAM, CODE_RATE_2_3, GUARD_G1_8, -79.5],
    [MODULATION_64QAM, CODE_RATE_3_4, GUARD_G1_4, -78.0],
    [MODULATION_64QAM, CODE_RATE_5_6, GUARD_G1_4, -76.6],
    [MODULATION_64QAM, CODE_RATE_7_8, GUARD_G1_4, -75.7]]

my_file = Path("../../ekt_json/dvbt_21_receiver_signal_input__min_level.json")
if my_file.exists():
    pass
else:
    dict_test_parame_result = {}
    list_test_parame_result = []
    dict_data = read_ekt_config_data("../../ekt_lib/ekt_config.json")
    DVBT_T2_FREQUENCY_LEVEL_OFFSET = dict_data.get("DVBT_T2_FREQUENCY_LEVEL_OFFSET")

    for FREQUENCY_LEVEL_OFFSET in DVBT_T2_FREQUENCY_LEVEL_OFFSET:
        list_test_result = []
        if FREQUENCY_LEVEL_OFFSET[0] < 400:
            CURRENT_MODULATION__CODERATE_SPEC_LIST = MODULATION_CODERATE_7M_SPEC_LIST
        else:
            CURRENT_MODULATION__CODERATE_SPEC_LIST = MODULATION_CODERATE_8M_SPEC_LIST

        for MODULATION_CODERATE_SPEC in CURRENT_MODULATION__CODERATE_SPEC_LIST:
            list_test_result.append(
                [MODULATION_CODERATE_SPEC[0], MODULATION_CODERATE_SPEC[1], MODULATION_CODERATE_SPEC[2], MODULATION_CODERATE_SPEC[3], None])
        list_test_parame_result.append([FREQUENCY_LEVEL_OFFSET, list_test_result])

    dict_test_parame_result["test_parame_result"] = list_test_parame_result
    write_json_file("../../ekt_json/dvbt_21_receiver_signal_input__min_level.json",
                    dict_test_parame_result)

if __name__ == '__main__':
    """
    测试流程:
    ①重置设备
    ②选择 TSPLAYER
    ③播放流文件
    ④设置code_rate,modulation,bandwidth,guard, frequency,input_signal_level
    ⑤机顶盒应用中进行锁台并确认锁台成功  （针对stb-tester发送post请求运行testcase）
    ⑤依次修改可变参数,判断机顶盒画面是否含有马赛克并记录结果
    """
    # 将部分无需测试的点的json文件内容, 测试结果置为 NO NEED TEST
    dvbt_21_receiver_signal_input__min_level_json_class_test("../../ekt_json/dvbt_21_receiver_signal_input__min_level.json")

    load_dict = read_json_file("../../ekt_json/dvbt_21_receiver_signal_input__min_level.json")
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
    specan.set_digitaltv_coding_fftmode_dvbt("M8K")

    for FREQUENCY_LEVEL_OFFSET in load_dict.get("test_parame_result"):
        loop_lock_mark = False
        for PARAMETER in FREQUENCY_LEVEL_OFFSET[1]:
            if PARAMETER[4] == None:
                loop_lock_mark = True
                break
        if loop_lock_mark == True:
            pass
        else:
            continue

        if FREQUENCY_LEVEL_OFFSET[0][0] < 400:
            CURRENT_BANDWIDTH = 7
        else:
            CURRENT_BANDWIDTH = 8

        specan = Ektsfu(sfu_ip)
        specan.set_frequency_frequency_frequency(str(int(FREQUENCY_LEVEL_OFFSET[0][0])) + "MHz")
        specan = Ektsfu(sfu_ip)
        specan.set_digitaltv_coding_channelbandwidth_dvbt("BW_{}".format(str(CURRENT_BANDWIDTH)))
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_offset(str(FREQUENCY_LEVEL_OFFSET[0][1]))
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_level("dBm", "-60")
        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        net.send_data(
            json.dumps({"cmd": "set_frequency_data", "frequency": str(int(FREQUENCY_LEVEL_OFFSET[0][0]))}))
        time.sleep(1)
        del net
        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        net.send_data(json.dumps({"cmd": "set_bandwidth_data", "bandwidth": str(CURRENT_BANDWIDTH)}))
        time.sleep(1)
        del net
        """
        触发stb-tester进行频率和符号率设置
        """
        stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                    ekt_cfg.DVB_T_LOCK_FUNCTION, ekt_cfg.DVB_T_CATEGORY, ekt_cfg.DVB_T_REMOTE)
        net = ekt_net.EktNetClient(ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT)
        lock_state = net.send_rec(json.dumps({"cmd": "get_lock_state"}))
        if lock_state == "1":
            pass
        elif lock_state == "0":
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              (
                                      "dvbt_21_receiver_signal_input__min_level: current_time:{}, frequency:{} MHz,bandwidth:{} Ksym/s, {}".format(
                                          datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          str(FREQUENCY_LEVEL_OFFSET[0][0]),
                                          str(CURRENT_BANDWIDTH), "Lock fail") + "\n"))
            continue
        else:
            write_test_result("../../ekt_log/test_result_sfu.txt", ("Lock state err" + "\n"))
            continue

        for MODULATION_CODERATE_SPEC in FREQUENCY_LEVEL_OFFSET[1]:
            if MODULATION_CODERATE_SPEC[4] == None:
                pass
            else:
                continue
            specan = Ektsfu(sfu_ip)
            specan.set_level_level_level("dBm", "-60")
            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_coding_constellation_dvbt(MODULATION_CODERATE_SPEC[0])
            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_coding_coderate_dvbt(MODULATION_CODERATE_SPEC[1])
            specan = Ektsfu(sfu_ip)
            specan.set_digitaltv_coding_guard_dvbt(MODULATION_CODERATE_SPEC[2])

            res, test_result = iterate_to_find_threshold_step_by_step(sfu_ip,
                                                         float("%.2f" % ((MODULATION_CODERATE_SPEC[3]) -
                                                                         FREQUENCY_LEVEL_OFFSET[0][1] + 5)),
                                                         level_offset=str(FREQUENCY_LEVEL_OFFSET[0][1]))
            print ("dvbt_21_receiver_signal_input__min_level: current_time:{}, modulation: {},coderate:{}, guard:{}, frequency:{} MHz,bandwidth:{} MHZ,{}".format(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), MODULATION_CODERATE_SPEC[0],
                MODULATION_CODERATE_SPEC[1], MODULATION_CODERATE_SPEC[2],
                str(FREQUENCY_LEVEL_OFFSET[0][0]), str(CURRENT_BANDWIDTH), res))
            write_test_result("../../ekt_log/test_result_sfu.txt",
                              "dvbt_21_receiver_signal_input__min_level: current_time:{}, modulation: {}, coderate:{}, guard:{},frequency:{} MHz,bandwidth:{} MHZ,{}".format(
                                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                  MODULATION_CODERATE_SPEC[0], MODULATION_CODERATE_SPEC[1],
                                  MODULATION_CODERATE_SPEC[2],
                                  str(FREQUENCY_LEVEL_OFFSET[0][0]), str(CURRENT_BANDWIDTH), res) + "\n")

            MODULATION_CODERATE_SPEC[4] = test_result
            write_json_file("../../ekt_json/dvbt_21_receiver_signal_input__min_level.json",
                            load_dict)
            dvbt_21_receiver_signal_input__min_level_json_to_csv(
                "../../ekt_json/dvbt_21_receiver_signal_input__min_level.json",
                "../../ekt_test_report/dvbt_21_receiver_signal_input__min_level.csv")

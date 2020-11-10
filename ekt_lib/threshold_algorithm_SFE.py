#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from ekt_stb_tester import stb_tester_execute_testcase
from ekt_image_classification import gevent_image_classification
from ekt_sfe import Ektsfe
from ekt_utils import write_test_result
import time
import logging
import ekt_cfg
import json
import os

current_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename='../ekt_log/sfe.log',
                    filemode='a',  ##模式,有w和a,w就是写模式,每次都会重新写日志,覆盖之前的日志
                    # a是追加模式,默认如果不写的话,就是追加模式
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')  # 日志格式


def mosaic_algorithm(sfe_ip, test_level_data, can_play_data):
    """
    Determine whether test level contains Mosaic or not
    :param sfe_ip:sfe ip
    :param test_level_data:test level
    :param can_play_data:can play level
    :return:mosaic_result
    """
    specan = Ektsfe(sfe_ip)
    specan.set_level_level_level(str(test_level_data) + " dBm")
    print ("set_level_level_level:{}".format(str(test_level_data) + " dBm"))
    logging.info("set_level_level_level:{}".format(str(test_level_data) + " dBm"))
    time.sleep(ekt_cfg.WAIT_FOR_INSTRUMENT_TIME)
    res = stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                      ["tests/front_end_test/testcases.py::test_recored"],
                                      "auto_front_end_test", "DSD4614iALM")
    print (res)
    write_test_result("{}/ekt_log/mosic_result.txt".format(current_path),
                      (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + ": " + str(res) + "\r\n")
    if res == False:
        mosaic_algorithm_result = {
            "detect_motion_result": False,
            "detect_mosic_result": "Fail",
            "msg": "picture not move"
        }
        logging.info("level:{}, Mosaic results:fail".format(test_level_data))
        specan = Ektsfe(sfe_ip)
        specan.set_level_level_level(str(can_play_data) + " dBm")
        return mosaic_algorithm_result, "Fail"
    elif res == True:
        dict_result, mosaic_result = gevent_image_classification(ekt_cfg.CAPTURE_NUM, ekt_cfg.STB_TESTER_IP)
        # specan = Ektsfe(sfe_ip)
        # specan.set_level_level_level(str(can_play_data) + " dBm")
        print (dict_result, mosaic_result)
        write_test_result("{}/ekt_log/mosic_result.txt".format(current_path),
                          (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + ": " + json.dumps(
                              dict_result) + "   " + mosaic_result + "\r\n")
        mosaic_algorithm_result = {
            "detect_motion_result": True,
            "detect_mosic_result": mosaic_result,
            "msg": dict_result
        }
        logging.info("level:{}, Mosaic results:{}".format(test_level_data, mosaic_result))
        return mosaic_algorithm_result, mosaic_result


def iterate_to_find_threshold_step_by_step(sfe_ip, start_num, level_offset="0"):
    """
    iterate to find threshold
    :param sfe_ip:sfe ip
    :param start_num: test level
    :param level_offset: level offset
    :return:threshild level
    """
    start_data_result, _ = mosaic_algorithm(sfe_ip, start_num, start_num)
    if start_data_result.get("detect_mosic_result") == "Pass":
        pass
    else:
        return json.dumps(
            {"threshold_algorithm_result": False, "msg": "The initial value is outside the Mosaic threshold:{}".format(start_num)},
            ensure_ascii=False), None
    while True:
        # step = 10
        step = 3
        # step = 4.5
        step_num = start_num - step
        step_num_data_result, _ = mosaic_algorithm(sfe_ip, step_num, start_num)
        if step_num_data_result.get("detect_mosic_result") == "Pass":
            start_num = step_num
        elif step_num_data_result.get("detect_mosic_result") == "Fail":
            print ("{} appear Mosaic".format(step_num))
            break
    while True:
        # step = 2
        # step = 1.5
        step = 1
        step_num = start_num - step
        step_num_data_result, _ = mosaic_algorithm(sfe_ip, step_num, start_num)
        if step_num_data_result.get("detect_mosic_result") == "Pass":
            start_num = step_num
        elif step_num_data_result.get("detect_mosic_result") == "Fail":
            print ("{} appear Mosaic".format(step_num))
            break
    while True:
        step = 0.5
        step_num = start_num - step
        step_num_data_result, _ = mosaic_algorithm(sfe_ip, step_num, start_num)
        if step_num_data_result.get("detect_mosic_result") == "Pass":
            start_num = step_num
        elif step_num_data_result.get("detect_mosic_result") == "Fail":
            print ("{} appear Mosaic".format(step_num))
            break
    print ("The threshold: {}".format(str("%.2f" % (float(start_num) + float(level_offset)))))
    return "The threshold: {}".format(str("%.2f" % (float(start_num) + float(level_offset)))), str(
        "%.2f" % (float(start_num) + float(level_offset)))


if __name__ == '__main__':
    sfe_ip = ekt_cfg.SFE_IP
    # specan = Ektsfe(net)
    # mosaic_algorithm(specan, "-77 dBm")
    # iterate_to_find_threshold_step_by_step(sfe_ip, -60)
    # iterate_to_find_threshold(sfe_ip, -60, -100)

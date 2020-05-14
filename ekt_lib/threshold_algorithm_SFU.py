#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from ekt_stb_tester import stb_tester_detect_motion
from ekt_image_capture import capture_image
from ekt_image_classification import image_classification
from ekt_sfu import Ektsfu
import time
import logging
import ekt_cfg
import json

logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename='../ekt_log/sfu.log',
                    filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )


def mosaic_algorithm(sfu_ip, test_level_data, can_play_data):
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_level("dBm", str(test_level_data))
    print "设置set_level_level_level:{}".format(str(test_level_data) + " dBm")
    logging.info("设置set_level_level_level:{}".format(str(test_level_data) + " dBm"))
    time.sleep(5)
    res = stb_tester_detect_motion(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                   ["tests/front_end_test/testcases.py::test_recored"],
                                   "auto_front_end_test", "DSD4614iALM")
    print res
    if res == False:
        mosaic_algorithm_result = {
            "detect_motion_result": False,
            "detect_mosic_result": True,
            "msg": "picture not move"
        }
        logging.info("level:{}, 马赛克结果:true".format(test_level_data))
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_level("dBm", str(can_play_data))
        return mosaic_algorithm_result
    elif res == True:
        list_image = capture_image(ekt_cfg.CAPTURE_NUM, ekt_cfg.STB_TESTER_IP)
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_level("dBm", str(can_play_data))
        dict_result, mosaic_result = image_classification(list_image)
        print dict_result, mosaic_result
        mosaic_algorithm_result = {
            "detect_motion_result": True,
            "detect_mosic_result": mosaic_result,
            "msg": dict_result
        }
        logging.info("level:{}, 马赛克结果:{}".format(test_level_data, mosaic_result))
        return mosaic_algorithm_result


def threshold_algorithm(sfu_ip, start_data, end_data):
    """
    算法步骤：
    ①判断起始数据start_data 对应画面无马赛克
    ②判断终止数据end_data   对应画面有马赛克
    ③根据步进值对起始与终止数据进行调整并判断画面是否含有马赛克
    ④返回马赛克与非马赛克的区间
    Find the critical value
    :param start_data:
    :param end_data:
    :param step_data:
    :return:
    """
    step_data = round((start_data + end_data) / 2, 1)
    step_data_result = mosaic_algorithm(sfu_ip, step_data, start_data)
    if step_data_result.get("detect_mosic_result") is False:
        return {"threshold_algorithm_result": False,
                "step_range": [step_data, end_data]}
    elif step_data_result.get("detect_mosic_result") is True:
        return {"threshold_algorithm_result": True,
                "step_range": [start_data, step_data]}


def iterate_to_find_threshold(sfu_ip, start_num, end_num, level_offset="0"):
    start_data_result = mosaic_algorithm(sfu_ip, start_num, start_num)
    end_data_result = mosaic_algorithm(sfu_ip, end_num, start_num)
    if start_data_result.get("detect_mosic_result") is False and end_data_result.get("detect_mosic_result") is True:
        pass
    else:
        print json.dumps({"threshold_algorithm_result": False, "msg": "初始值处于马赛克阈值外"}, ensure_ascii=False)
        return json.dumps({"threshold_algorithm_result": False, "msg": "初始值处于马赛克阈值外"}, ensure_ascii=False)
    while True:
        # ekt_cfg.TEST_LEVLE_PRECISION 测试level 精度
        if start_num - end_num >= ekt_cfg.TEST_LEVLE_PRECISION:
            print "start_num:{},  end_num:{}".format(start_num, end_num)
            dict_threshold_algorithm_result = threshold_algorithm(sfu_ip, start_num, end_num)
            [start_num, end_num] = dict_threshold_algorithm_result.get("step_range")
        elif start_num - end_num - ekt_cfg.TEST_LEVLE_PRECISION < 0.000001:
            print "阈值为: {}".format(str("%.2f" % (float(start_num) + float(level_offset))))
            return "阈值为: {}".format(str("%.2f" % (float(start_num) + float(level_offset))))
        else:
            print " start_num - end_num 小于 0.1"
            return start_num, end_num


def jest_test(net, num):
    specan = Ektsfu(net)
    specan.set_level_level_level("dBm", str(num))
    time.sleep(5)


if __name__ == '__main__':
    sfu_ip = "192.168.1.50"
    # specan = Ektsfu(net)
    # mosaic_algorithm(specan, "-77 dBm")
    iterate_to_find_threshold(sfu_ip, -60, -80)

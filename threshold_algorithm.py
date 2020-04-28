#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from ekt_stb_tester import stb_tester_detect_motion
from ekt_image_capture import capture_image
from ekt_image_classification import image_classification
from ekt_sfe import Ektsfe
import time


def mosaic_algorithm(net, test_level_data):
    specan = Ektsfe(net)
    specan.set_level_level_level(str(test_level_data) + " dBm")
    del specan
    print "设置set_level_level_level:{}".format(str(test_level_data) + " dBm")
    time.sleep(5)
    res = stb_tester_detect_motion("http://192.168.1.154", "7dbb2a3",
                                   ["tests/front_end_test/testcases.py::test_recored"],
                                   "auto_front_end_test", "DSD4614iALM")
    print res
    if res == False:
        mosaic_algorithm_result = {
            "detect_motion_result": False,
            "detect_mosic_result": True,
            "msg": "picture not move"
        }
        return mosaic_algorithm_result
    elif res == True:
        num = 50
        list_image = capture_image(num, "192.168.1.154")
        dict_result, mosaic_result = image_classification(list_image)
        print dict_result, mosaic_result
        mosaic_algorithm_result = {
            "detect_motion_result": True,
            "detect_mosic_result": mosaic_result,
            "msg": dict_result
        }
        return mosaic_algorithm_result


# def threshold_algorithm(net, start_data, end_data, step_data):
#     """
#     算法步骤：
#     ①判断起始数据start_data 对应画面无马赛克
#     ②判断终止数据end_data   对应画面有马赛克
#     ③根据步进值对起始与终止数据进行调整并判断画面是否含有马赛克
#     ④返回马赛克与非马赛克的区间
#
#     Find the critical value
#     :param start_data:
#     :param end_data:
#     :param step_data:
#     :return:
#     """
#     if start_data - end_data > 2 * step_data:
#         pass
#     else:
#         return {"threshold_algorithm_result": False,
#                 "msg": "起始值与终止值小于两倍步进"}
#     start_data_result = mosaic_algorithm(net, start_data)
#     end_data_result = mosaic_algorithm(net, end_data)
#     if start_data_result.get("detect_mosic_result") is False and end_data_result.get("detect_mosic_result") is True:
#         pass
#     else:
#         return {"threshold_algorithm_result": False,
#                 "msg": "初始值处于马赛克阈值外"}
#     start_data_step = start_data - step_data
#     end_data_step = start_data + step_data
#     start_data_step_result = mosaic_algorithm(net, start_data_step)
#     end_data_step_result = mosaic_algorithm(net, end_data_step)
#     if start_data_step_result.get("detect_mosic_result") is False and end_data_step_result.get(
#             "detect_mosic_result") is True:
#         return {"threshold_algorithm_result": True,
#                 "msg": [start_data_step, end_data_step]}
#     elif start_data_step_result.get("detect_mosic_result") is False and end_data_step_result.get(
#             "detect_mosic_result") is False:
#         return {"threshold_algorithm_result": True,
#                 "msg": [end_data_step, end_data]}
#     elif start_data_step_result.get("detect_mosic_result") is True and end_data_step_result.get(
#             "detect_mosic_result") is True:
#         return {"threshold_algorithm_result": True,
#                 "msg": [start_data, start_data_step]}
#     elif start_data_step_result.get("detect_mosic_result") is True and end_data_step_result.get(
#             "detect_mosic_result") is False:
#         # 需确认是否需要二次重测
#         return {"threshold_algorithm_result": False,
#                 "msg": "系统错误"}

def threshold_algorithm(net, start_data, end_data, step_data):
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
    if start_data - end_data > 2 * step_data:
        pass
    else:
        return {"threshold_algorithm_result": False,
                "msg": "起始值与终止值小于两倍步进"}
    start_data_result = mosaic_algorithm(net, start_data)
    end_data_result = mosaic_algorithm(net, end_data)
    if start_data_result.get("detect_mosic_result") is False and end_data_result.get("detect_mosic_result") is True:
        pass
    else:
        return {"threshold_algorithm_result": False,
                "msg": "初始值处于马赛克阈值外"}
    start_data_step = start_data - step_data
    end_data_step = start_data + step_data
    start_data_step_result = mosaic_algorithm(net, start_data_step)
    end_data_step_result = mosaic_algorithm(net, end_data_step)
    if start_data_step_result.get("detect_mosic_result") is False and end_data_step_result.get(
            "detect_mosic_result") is True:
        return {"threshold_algorithm_result": True,
                "msg": [start_data_step, end_data_step]}
    elif start_data_step_result.get("detect_mosic_result") is False and end_data_step_result.get(
            "detect_mosic_result") is False:
        return {"threshold_algorithm_result": True,
                "msg": [end_data_step, end_data]}
    elif start_data_step_result.get("detect_mosic_result") is True and end_data_step_result.get(
            "detect_mosic_result") is True:
        return {"threshold_algorithm_result": True,
                "msg": [start_data, start_data_step]}
    elif start_data_step_result.get("detect_mosic_result") is True and end_data_step_result.get(
            "detect_mosic_result") is False:
        # 需确认是否需要二次重测
        return {"threshold_algorithm_result": False,
                "msg": "系统错误"}


def iterate_to_find_threshold(net, start_num, end_num):
    step_data = round((start_num - end_num) / 4, 2)
    # print step_data
    # print type(step_data)
    # print '*****'
    # print start_data - end_data
    if start_num - end_num > 0.1:
        # start_data = start_num - step_data
        # end_data = end_num + step_data
        # print_num(start_data, end_data)
        # start_num, end_num = threshold_algorithm(specan, start_num, end_num, step_data)
        dict_threshold_algorithm_result = threshold_algorithm(net, start_num, end_num, step_data)
        if dict_threshold_algorithm_result.get("threshold_algorithm_result") == False:
            print "threshold_algorithm 异常"
        else:
            [start_num, end_num] = dict_threshold_algorithm_result.get("msg")

            iterate_to_find_threshold(net, start_num, end_num)
    else:
        print " start_num - end_num 小于 0.1"
        return start_num, end_num


def print_num(start_data, end_data):
    print start_data, end_data, round((start_data - end_data) / 4, 1)

    step_data = round((start_data - end_data) / 4, 2)
    # step_data = round((start_data - end_data) / 4, 1)
    if start_data - end_data > 0.1:
        start_data = start_data - step_data
        end_data = end_data + step_data
        print_num(start_data, end_data)
    else:
        return start_data, end_data


def jest_test(net, num):
    specan = Ektsfe(net)
    specan.set_level_level_level(str(num) + " dBm")
    del specan
    time.sleep(5)


if __name__ == '__main__':
    # end_data = -90
    # start_data = -60
    # print_num(start_data, end_data)
    net = "192.168.1.47"
    # specan = Ektsfe(net)
    # mosaic_algorithm(specan, "-77 dBm")
    # iterate_to_find_threshold(net, -60, -90)

    # jest_test(net, -60)
    # jest_test(net, -65)
    # jest_test(net, -70)
    # jest_test(net, -75)
    # jest_test(net, -80)
    # jest_test(net, -75)
    # jest_test(net, -70)
    # jest_test(net, -65)
    # jest_test(net, -60)
    jest_test(net, -60)
    jest_test(net, -90)
    jest_test(net, -70)
    jest_test(net, -80)
    jest_test(net, -72)
    jest_test(net, -78)
    jest_test(net, -74)
    jest_test(net, -76)

    # jest_test(net, -100)
    # jest_test(net, 0)
    # jest_test(net, -100)
    # jest_test(net, 0)

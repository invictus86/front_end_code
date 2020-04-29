#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from ekt_stb_tester import stb_tester_detect_motion
from ekt_image_capture import capture_image
from ekt_image_classification import image_classification
from ekt_sfe import Ektsfe
import time
import logging

logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename='front_end_test.log',
                    filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )


def mosaic_algorithm(net, test_level_data):
    specan = Ektsfe(net)
    specan.set_level_level_level(str(test_level_data) + " dBm")
    del specan
    print "设置set_level_level_level:{}".format(str(test_level_data) + " dBm")
    logging.info("设置set_level_level_level:{}".format(str(test_level_data) + " dBm"))
    time.sleep(5)
    res = stb_tester_detect_motion("http://192.168.1.154", "5e9b253",
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
        return mosaic_algorithm_result
    elif res == True:
        # num = 50
        num = 10
        list_image = capture_image(num, "192.168.1.154")
        specan.set_level_level_level("-31" + " dBm")
        dict_result, mosaic_result = image_classification(list_image)
        print dict_result, mosaic_result
        mosaic_algorithm_result = {
            "detect_motion_result": True,
            "detect_mosic_result": mosaic_result,
            "msg": dict_result
        }
        logging.info("level:{}, 马赛克结果:{}".format(test_level_data, mosaic_result))
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

def threshold_algorithm(net, start_data, end_data):
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
    step_data_result = mosaic_algorithm(net, step_data)
    if step_data_result.get("detect_mosic_result") is False:
        return {"threshold_algorithm_result": False,
                "step_range": [step_data, end_data]}
    elif step_data_result.get("detect_mosic_result") is True:
        return {"threshold_algorithm_result": True,
                "step_range": [start_data, step_data]}


# def iterate_to_find_threshold(net, start_num, end_num):
#     step_data = round((start_num - end_num) / 4, 2)
#     # print step_data
#     # print type(step_data)
#     # print '*****'
#     # print start_data - end_data
#     if start_num - end_num > 0.1:
#         # start_data = start_num - step_data
#         # end_data = end_num + step_data
#         # print_num(start_data, end_data)
#         # start_num, end_num = threshold_algorithm(specan, start_num, end_num, step_data)
#         dict_threshold_algorithm_result = threshold_algorithm(net, start_num, end_num, step_data)
#         if dict_threshold_algorithm_result.get("threshold_algorithm_result") == False:
#             print "threshold_algorithm 异常"
#         else:
#             [start_num, end_num] = dict_threshold_algorithm_result.get("msg")
#
#             iterate_to_find_threshold(net, start_num, end_num)
#     else:
#         print " start_num - end_num 小于 0.1"
#         return start_num, end_num

def iterate_to_find_threshold(net, start_num, end_num):
    start_data_result = mosaic_algorithm(net, start_num)
    end_data_result = mosaic_algorithm(net, end_num)
    if start_data_result.get("detect_mosic_result") is False and end_data_result.get("detect_mosic_result") is True:
        pass
    else:
        return {"threshold_algorithm_result": False,
                "msg": "初始值处于马赛克阈值外"}
    while True:
        if start_num - end_num > 0.1:
            print "start_num:{},  end_num:{}".format(start_num, end_num)
            dict_threshold_algorithm_result = threshold_algorithm(net, start_num, end_num)
            [start_num, end_num] = dict_threshold_algorithm_result.get("step_range")
        elif start_num - end_num == 0.1:
            start_num_resutl = mosaic_algorithm(net, start_num)
            end_num_resutl = mosaic_algorithm(net, end_num)
            if start_num_resutl.get("detect_mosic_result") is False and end_num_resutl.get("detect_mosic_result") is True:
                print "阈值为: {}".format(start_num)
                return start_num
            elif start_num_resutl.get("detect_mosic_result") is True and end_num_resutl.get("detect_mosic_result") is False:
                print "阈值为: {}".format(end_num)
                return end_num
            else:
                print "阈值错误"
                break
        else:
            print " start_num - end_num 小于 0.1"
            return start_num, end_num

    # step_data = round((start_num - end_num) / 4, 2)
    # # print step_data
    # # print type(step_data)
    # # print '*****'
    # # print start_data - end_data
    # if start_num - end_num > 0.1:
    #     # start_data = start_num - step_data
    #     # end_data = end_num + step_data
    #     # print_num(start_data, end_data)
    #     # start_num, end_num = threshold_algorithm(specan, start_num, end_num, step_data)
    #     dict_threshold_algorithm_result = threshold_algorithm(net, start_num, end_num, step_data)
    #     if dict_threshold_algorithm_result.get("threshold_algorithm_result") == False:
    #         print "threshold_algorithm 异常"
    #     else:
    #         [start_num, end_num] = dict_threshold_algorithm_result.get("msg")
    #
    #         iterate_to_find_threshold(net, start_num, end_num)
    # else:
    #     print " start_num - end_num 小于 0.1"
    #     return start_num, end_num


def print_num(start_data, end_data):
    print start_data, end_data, round((start_data - end_data) / 4, 2)

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
    iterate_to_find_threshold(net, -70, -80)

    # jest_test(net, -60)
    # jest_test(net, -65)
    # jest_test(net, -70)
    # jest_test(net, -75)
    # jest_test(net, -80)
    # jest_test(net, -75)
    # jest_test(net, -70)
    # jest_test(net, -65)
    # jest_test(net, -60)
    # jest_test(net, -60)
    # jest_test(net, -90)
    # jest_test(net, -70)
    # jest_test(net, -80)
    # jest_test(net, -72)
    # jest_test(net, -78)
    # jest_test(net, -74)
    # jest_test(net, -76)

    # jest_test(net, -100)
    # jest_test(net, 0)
    # jest_test(net, -100)
    # jest_test(net, 0)
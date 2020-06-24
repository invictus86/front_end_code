#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from ekt_stb_tester import stb_tester_execute_testcase
from ekt_image_capture import capture_image
from ekt_image_classification import image_classification
from ekt_sfu import Ektsfu
import time
import logging
import ekt_cfg
import json

logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename='../ekt_log/sfu.log',
                    filemode='a',  ##模式,有w和a,w就是写模式,每次都会重新写日志,覆盖之前的日志
                    # a是追加模式,默认如果不写的话,就是追加模式
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )


def mosaic_algorithm(sfu_ip, test_level_data, can_play_data):
    """
    judge if test level contains mosaics
    :param sfu_ip: sfu ip
    :param test_level_data: test level
    :param can_play_data:   can play level
    :return:mosaic_algorithm_result, mosaic_result
    """
    specan = Ektsfu(sfu_ip)
    specan.set_level_level_level("dBm", str(test_level_data))
    print ("set_level_level_level:{}".format(str(test_level_data) + " dBm"))
    logging.info("set_level_level_level:{}".format(str(test_level_data) + " dBm"))
    time.sleep(5)
    res = stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                      ["tests/front_end_test/testcases.py::test_recored"],
                                      "auto_front_end_test", "DSD4614iALM")
    print (res)
    if res == False:
        mosaic_algorithm_result = {
            "detect_motion_result": False,
            "detect_mosic_result": "Fail",
            "msg": "picture not move"
        }
        logging.info("level:{}, Mosaic results:fail".format(test_level_data))
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_level("dBm", str(can_play_data))
        return mosaic_algorithm_result, "Fail"
    elif res == True:
        list_image = capture_image(ekt_cfg.CAPTURE_NUM, ekt_cfg.STB_TESTER_IP)
        specan = Ektsfu(sfu_ip)
        specan.set_level_level_level("dBm", str(can_play_data))
        dict_result, mosaic_result = image_classification(list_image)
        print (dict_result, mosaic_result)
        mosaic_algorithm_result = {
            "detect_motion_result": True,
            "detect_mosic_result": mosaic_result,
            "msg": dict_result
        }
        logging.info("level:{}, Mosaic results:{}".format(test_level_data, mosaic_result))
        return mosaic_algorithm_result, mosaic_result


def mosaic_algorithm_noise_cn(sfu_ip, test_cn_data, can_play_data):
    """
    judge if test CN contains mosaics
    :param sfu_ip: sfu ip
    :param test_cn_data:  test CN
    :param can_play_data: can play CN
    :return:mosaic_algorithm_result
    """
    specan = Ektsfu(sfu_ip)
    specan.set_noise_awgn_cn(str(test_cn_data))
    print ("set_noise_awgn_cn:{}".format(str(test_cn_data)))
    logging.info("set_noise_awgn_cn:{}".format(str(test_cn_data)))
    time.sleep(5)
    res = stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                      ["tests/front_end_test/testcases.py::test_recored"],
                                      "auto_front_end_test", "DSD4614iALM")
    print (res)
    if res == False:
        mosaic_algorithm_result = {
            "detect_motion_result": False,
            "detect_mosic_result": "Fail",
            "msg": "picture not move"
        }
        logging.info("noise_cn:{}, Mosaic results:fail".format(test_cn_data))
        specan = Ektsfu(sfu_ip)
        specan.set_noise_awgn_cn(str(can_play_data))
        return mosaic_algorithm_result
    elif res == True:
        list_image = capture_image(ekt_cfg.CAPTURE_NUM, ekt_cfg.STB_TESTER_IP)
        specan = Ektsfu(sfu_ip)
        specan.set_noise_awgn_cn(str(can_play_data))
        dict_result, mosaic_result = image_classification(list_image)
        print (dict_result, mosaic_result)
        mosaic_algorithm_result = {
            "detect_motion_result": True,
            "detect_mosic_result": mosaic_result,
            "msg": dict_result
        }
        logging.info("noise_cn:{}, Mosaic results:{}".format(test_cn_data, mosaic_result))
        return mosaic_algorithm_result


def mosaic_algorithm_fading_att(sfu_ip, test_att_data, can_play_data):
    """
    judge if test att contains mosaics
    :param sfu_ip: sfu ip
    :param test_att_data: test
    :param can_play_data:
    :return:mosaic_algorithm_result
    """
    specan = Ektsfu(sfu_ip)
    specan.set_fading_profile_pathloss("3", "1", "{} dB".format(str(test_att_data)))
    print ("set_fading_att:{}".format(str(test_att_data)))
    logging.info("set_fading_att:{}".format(str(test_att_data)))
    time.sleep(5)
    res = stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                      ["tests/front_end_test/testcases.py::test_recored"],
                                      "auto_front_end_test", "DSD4614iALM")
    print (res)
    if res == False:
        mosaic_algorithm_result = {
            "detect_motion_result": False,
            "detect_mosic_result": "Fail",
            "msg": "picture not move"
        }
        logging.info("noise_cn:{}, Mosaic results:fail".format(test_att_data))
        specan = Ektsfu(sfu_ip)
        specan.set_fading_profile_pathloss("3", "1", "{} dB".format(str(can_play_data)))
        return mosaic_algorithm_result
    elif res == True:
        list_image = capture_image(ekt_cfg.CAPTURE_NUM, ekt_cfg.STB_TESTER_IP)
        specan = Ektsfu(sfu_ip)
        specan.set_fading_profile_pathloss("3", "1", "{} dB".format(str(can_play_data)))
        dict_result, mosaic_result = image_classification(list_image)
        print (dict_result, mosaic_result)
        mosaic_algorithm_result = {
            "detect_motion_result": True,
            "detect_mosic_result": mosaic_result,
            "msg": dict_result
        }
        logging.info("noise_cn:{}, Mosaic results:{}".format(test_att_data, mosaic_result))
        return mosaic_algorithm_result


def mosaic_algorithm_interferer_attenuation(sfu_ip, test_attenuation_data, can_play_data):
    """
    judge if test attenuation contains mosaics
    :param sfu_ip:
    :param test_attenuation_data:
    :param can_play_data:
    :return: mosaic_algorithm_result
    """
    specan = Ektsfu(sfu_ip)
    specan.set_interferer_attenuation(str(test_attenuation_data))
    print ("set_noise_awgn_cn:{}".format(str(test_attenuation_data)))
    logging.info("set_noise_awgn_cn:{}".format(str(test_attenuation_data)))
    time.sleep(5)
    res = stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                      ["tests/front_end_test/testcases.py::test_recored"],
                                      "auto_front_end_test", "DSD4614iALM")
    print (res)
    if res == False:
        mosaic_algorithm_result = {
            "detect_motion_result": False,
            "detect_mosic_result": "Fail",
            "msg": "picture not move"
        }
        logging.info("noise_cn:{}, Mosaic results:fail".format(test_attenuation_data))
        specan = Ektsfu(sfu_ip)
        specan.set_noise_awgn_cn(str(can_play_data))
        return mosaic_algorithm_result
    elif res == True:
        list_image = capture_image(ekt_cfg.CAPTURE_NUM, ekt_cfg.STB_TESTER_IP)
        specan = Ektsfu(sfu_ip)
        specan.set_noise_awgn_cn(str(can_play_data))
        dict_result, mosaic_result = image_classification(list_image)
        print (dict_result, mosaic_result)
        mosaic_algorithm_result = {
            "detect_motion_result": True,
            "detect_mosic_result": mosaic_result,
            "msg": dict_result
        }
        logging.info("noise_cn:{}, Mosaic results:{}".format(test_attenuation_data, mosaic_result))
        return mosaic_algorithm_result


def iterate_to_find_threshold_step_by_step_dvbs2(sfu_ip, start_num, level_offset="0"):
    """
    iterate level to find threshold,it used for dvbs2
    :param sfu_ip: sfu ip
    :param start_num: start test level
    :param level_offset: level offset
    :return: test_message , threshold level value
    """
    start_data_result, _ = mosaic_algorithm(sfu_ip, start_num, start_num)
    if start_data_result.get("detect_mosic_result") == "Pass":
        pass
    else:
        return json.dumps({"threshold_algorithm_result": False, "msg": "The initial value is outside the Mosaic threshold:{}".format(start_num)},
                          ensure_ascii=False), None
    while True:
        step = 10
        step_num = start_num - step
        step_num_data_result, _ = mosaic_algorithm(sfu_ip, step_num, start_num)
        if step_num_data_result.get("detect_mosic_result") == "Pass":
            start_num = step_num
        elif step_num_data_result.get("detect_mosic_result") == "Fail":
            print ("{} appear Mosaic".format(step_num))
            break
    while True:
        # step = 1
        step = 2
        step_num = start_num - step
        step_num_data_result, _ = mosaic_algorithm(sfu_ip, step_num, start_num)
        if step_num_data_result.get("detect_mosic_result") == "Pass":
            start_num = step_num
        elif step_num_data_result.get("detect_mosic_result") == "Fail":
            print ("{} appear Mosaic".format(step_num))
            break
    while True:
        # step = 0.3
        step = 0.5
        step_num = start_num - step
        step_num_data_result, _ = mosaic_algorithm(sfu_ip, step_num, start_num)
        if step_num_data_result.get("detect_mosic_result") == "Pass":
            start_num = step_num
        elif step_num_data_result.get("detect_mosic_result") == "Fail":
            print ("{} appear Mosaic".format(step_num))
            break
    print ("The threshold: {}".format(str("%.2f" % (float(start_num) + float(level_offset)))))
    return "The threshold: {}".format(str("%.2f" % (float(start_num) + float(level_offset)))), str(
        "%.2f" % (float(start_num) + float(level_offset)))


def iterate_to_find_threshold_step_by_step(sfu_ip, start_num, level_offset="0"):
    """
    iterate level to find threshold,it used for dvbt/dvbt2
    :param sfu_ip: sfu ip
    :param start_num: start test level
    :param level_offset: level offset
    :return: test_message , threshold level value
    """
    start_data_result, _ = mosaic_algorithm(sfu_ip, start_num, start_num)
    if start_data_result.get("detect_mosic_result") == "Pass":
        pass
    else:
        return json.dumps({"threshold_algorithm_result": False, "msg": "The initial value is outside the Mosaic threshold:{}".format(start_num)},
                          ensure_ascii=False), None
    while True:
        step = 3
        step_num = start_num - step
        step_num_data_result, _ = mosaic_algorithm(sfu_ip, step_num, start_num)
        if step_num_data_result.get("detect_mosic_result") == "Pass":
            start_num = step_num
        elif step_num_data_result.get("detect_mosic_result") == "Fail":
            print ("{} appear Mosaic".format(step_num))
            break
    while True:
        step = 1
        step_num = start_num - step
        step_num_data_result, _ = mosaic_algorithm(sfu_ip, step_num, start_num)
        if step_num_data_result.get("detect_mosic_result") == "Pass":
            start_num = step_num
        elif step_num_data_result.get("detect_mosic_result") == "Fail":
            print ("{} appear Mosaic".format(step_num))
            break
    while True:
        step = 0.1
        step_num = start_num - step
        step_num_data_result, _ = mosaic_algorithm(sfu_ip, step_num, start_num)
        if step_num_data_result.get("detect_mosic_result") == "Pass":
            start_num = step_num
        elif step_num_data_result.get("detect_mosic_result") == "Fail":
            print ("{} appear Mosaic".format(step_num))
            break
    print ("The threshold: {}".format(str("%.2f" % (float(start_num) + float(level_offset)))))
    return "The threshold: {}".format(str("%.2f" % (float(start_num) + float(level_offset)))), str(
        "%.2f" % (float(start_num) + float(level_offset)))


def iterate_to_find_threshold_interferer_attenuation_step_by_step(sfu_ip, start_num):
    """
    iterate attenuation to find threshold,it used for dvbt/dvbt2
    :param sfu_ip: sfu ip
    :param start_num: start test attenuation
    :return: test_message , threshold attenuation value
    """
    start_data_result = mosaic_algorithm_interferer_attenuation(sfu_ip, start_num, start_num)
    if start_data_result.get("detect_mosic_result") == "Pass":
        pass
    else:
        return json.dumps({"threshold_algorithm_result": False, "msg": "The initial value is outside the Mosaic threshold:{}".format(start_num)},
                          ensure_ascii=False), None
    while True:
        step = 1
        step_num = start_num - step
        step_num_data_result = mosaic_algorithm_interferer_attenuation(sfu_ip, step_num, start_num)
        if step_num_data_result.get("detect_mosic_result") == "Pass":
            start_num = step_num
        elif step_num_data_result.get("detect_mosic_result") == "Fail":
            print ("{} appear Mosaic".format(step_num))
            break
    # while True:
    #     step = 0.1
    #     step_num = start_num - step
    #     step_num_data_result = mosaic_algorithm_interferer_attenuation(sfu_ip, step_num, start_num)
    #     if step_num_data_result.get("detect_mosic_result") is False:
    #         start_num = step_num
    #     elif step_num_data_result.get("detect_mosic_result") is True:
    #         print("{} appear Mosaic".format(step_num))
    #         break
    print ("The threshold: {}".format(str("%.2f" % float(start_num))))
    return "The threshold: {}".format(str("%.2f" % float(start_num))), str("%.2f" % float(start_num))


def iterate_to_find_threshold_noise_cn_step_by_step(sfu_ip, start_num):
    """
    iterate CN to find threshold
    :param sfu_ip:sfu ip
    :param start_num:start test CN
    :return:test_message , threshold CN value
    """
    start_data_result = mosaic_algorithm_noise_cn(sfu_ip, start_num, start_num)
    if start_data_result.get("detect_mosic_result") == "Pass":
        pass
    else:
        return json.dumps({"threshold_algorithm_result": False, "msg": "The initial value is outside the Mosaic threshold:{}".format(start_num)},
                          ensure_ascii=False), None
    while True:
        # step = 1
        step = 2
        step_num = start_num - step
        step_num_data_result = mosaic_algorithm_noise_cn(sfu_ip, step_num, start_num)
        if step_num_data_result.get("detect_mosic_result") == "Pass":
            start_num = step_num
        elif step_num_data_result.get("detect_mosic_result") == "Fail":
            print ("{} appear Mosaic".format(step_num))
            break
    while True:
        # step = 0.1
        step = 0.5
        step_num = start_num - step
        step_num_data_result = mosaic_algorithm_noise_cn(sfu_ip, step_num, start_num)
        if step_num_data_result.get("detect_mosic_result") == "Pass":
            start_num = step_num
        elif step_num_data_result.get("detect_mosic_result") == "Fail":
            print("{} appear Mosaic".format(step_num))
            break
    print ("The threshold: {}".format(str("%.2f" % float(start_num))))
    return "The threshold: {}".format(str("%.2f" % float(start_num))), str("%.2f" % float(start_num))


def iterate_to_find_threshold_fading_att_step_by_step(sfu_ip, start_num):
    """
    iterate att to find threshold
    :param sfu_ip: sfu ip
    :param start_num: start test att
    :return: test_message , threshold att value
    """
    start_data_result = mosaic_algorithm_fading_att(sfu_ip, start_num, start_num)
    if start_data_result.get("detect_mosic_result") == "Pass":
        pass
    else:
        return json.dumps({"threshold_algorithm_result": False, "msg": "The initial value is outside the Mosaic threshold:{}".format(start_num)},
                          ensure_ascii=False), None
    while True:
        step = 1
        step_num = start_num - step
        step_num_data_result = mosaic_algorithm_fading_att(sfu_ip, step_num, start_num)
        if step_num_data_result.get("detect_mosic_result") == "Pass":
            start_num = step_num
        elif step_num_data_result.get("detect_mosic_result") == "Fail":
            print ("{} appear Mosaic".format(step_num))
            break
        if start_num == 0:
            break
    # while True:
    #     step = 0.1
    #     step_num = start_num - step
    #     step_num_data_result = mosaic_algorithm_fading_att(sfu_ip, step_num, start_num, channel_x, channel_y)
    #     if step_num_data_result.get("detect_mosic_result") is False:
    #         start_num = step_num
    #     elif step_num_data_result.get("detect_mosic_result") is True:
    #         print("{} appear Mosaic".format(step_num))
    #         break
    print ("The threshold: {}".format(str("%.2f" % float(start_num))))
    return "The threshold: {}".format(str("%.2f" % float(start_num))), str("%.2f" % float(start_num))


if __name__ == '__main__':
    sfu_ip = "192.168.1.50"
    # specan = Ektsfu(net)
    # mosaic_algorithm(specan, "-77 dBm")
    iterate_to_find_threshold_step_by_step(sfu_ip, -85)
    # iterate_to_find_threshold(sfu_ip, -60, -80)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import cv2
import ekt_image_capture
import ekt_cfg
import time
import os
import logging

current_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename='{}/ekt_log/ekt_image_classification.log'.format(current_path),
                    filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )


def image_classification(list_image):
    """
    image classification
    :param :list_image: list of image that need to classify
    :return:dict_result: classification result
    """
    result_list = []
    dict_result = {}
    for image in list_image:
        img_str = cv2.imencode('.jpg', image)[1].tostring()
        # params 为GET参数 data 为POST Body
        while True:
            try:
                result = requests.post('http://127.0.0.1:24401/', params={'threshold': 0.1}, data=img_str).json()
                break
            except:
                time.sleep(60)
                print("ekt_image_classification  connection error")
                logging.info('ekt_image_classification  connection error')

        # print result
        result_list.append(result["results"][0]["label"])

    for key in result_list:
        dict_result[key] = dict_result.get(key, 0) + 1
    # print dict_result.get("mosaic")
    # if dict_result.get("mosaic") == None or dict_result.get("mosaic") == 1:
    if dict_result.get("mosaic") == None or dict_result.get("mosaic") <= ekt_cfg.ERR_MOSIC_NUM:
        # mosaic_result = False
        mosaic_result = "Pass"
    else:
        # print dict_result.get("mosaic")
        # mosaic_result = True
        mosaic_result = "Fail"
    return dict_result, mosaic_result
    # return dict_result


if __name__ == '__main__':
    # start_time = time.time()
    num = 50
    list_image = ekt_image_capture.capture_image(num, "192.168.1.154")
    print (list_image)
    dict_result, mosaic_result = image_classification(list_image)
    # end_time = time.time()
    # print end_time-start_time
    print (dict_result, mosaic_result)

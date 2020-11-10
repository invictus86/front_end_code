#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import cv2
import ekt_image_capture
import ekt_cfg
import time
import os
import logging
from gevent import monkey
import gevent
import datetime

current_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename='{}/ekt_log/ekt_image_classification.log'.format(current_path),
                    filemode='a',  ##模式,有w和a,w就是写模式,每次都会重新写日志,覆盖之前的日志
                    # a是追加模式,默认如果不写的话,就是追加模式
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')  # 日志格式


def image_classification(list_image):
    """
    image classification
    :param :list_image: list of image that need to classify
    :return:dict_result: classification result
    """
    for image in list_image:
        img_str = cv2.imencode('.jpg', image)[1].tostring()
        # params 为GET参数 data 为POST Body
        while True:
            try:
                result = requests.post('http://{}:24401/'.format(ekt_cfg.EASYEDGE_IP), params={'threshold': 0.1}, data=img_str).json()
                # dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                # print dt_ms
                # if result["results"][0]["label"] == "no_mosaic":
                #     t = time.time()
                #     current_time = int(round(t * 1000))
                #     cv2.imwrite('{}/image/no_mosaic/{}.png'.format(current_path, str(current_time)), image)
                # elif result["results"][0]["label"] == "mosaic":
                #     t = time.time()
                #     current_time = int(round(t * 1000))
                #     cv2.imwrite('{}/image/mosaic/{}.png'.format(current_path, str(current_time)), image)
                break
            except:
                time.sleep(5)
                print("ekt_image_classification  connection error")
                logging.info('ekt_image_classification  connection error')
        # print result
        return result["results"][0]["label"]


list_data = []


def get_single_image_classification(stb_tetser_ip):
    global list_data
    num = 1
    list_image = ekt_image_capture.capture_image(num, stb_tetser_ip)
    image_result = image_classification(list_image)
    list_data.append(image_result)
    return image_result


def gevent_image_classification(num, stb_tetser_ip):
    global list_data
    dict_result = {}
    monkey.patch_all()
    list_gevent = []
    for i in range(num):
        list_gevent.append(gevent.spawn(get_single_image_classification, stb_tetser_ip))
    gevent.joinall(list_gevent)

    for key in list_data:
        dict_result[key] = dict_result.get(key, 0) + 1
    if dict_result.get("mosaic") == None or dict_result.get("mosaic") <= ekt_cfg.ERR_MOSIC_NUM:
        mosaic_result = "Pass"
    else:
        mosaic_result = "Fail"
    list_data = []
    return dict_result, mosaic_result


if __name__ == '__main__':
    start_time = time.time()
    num = 12
    stb_tetser_ip = "192.168.1.155"
    data1, data2 = gevent_image_classification(num, stb_tetser_ip)
    print data1, data2
    print time.time() - start_time
    # data3, data4 = gevent_image_classification(num, stb_tetser_ip)
    # print data3, data4
    # print time.time() - start_time
    # data5, data6 = gevent_image_classification(num, stb_tetser_ip)
    # print data5, data6
    # print time.time() - start_time

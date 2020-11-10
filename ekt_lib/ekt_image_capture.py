#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import cv2
import numpy
import time
import os
import logging
import datetime

current_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename='{}/ekt_log/ekt_image_capture.log'.format(current_path),
                    filemode='a',  ##模式,有w和a,w就是写模式,每次都会重新写日志,覆盖之前的日志
                    # a是追加模式,默认如果不写的话,就是追加模式
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')  # 日志格式


def capture_image(num, ip):
    """
    capture stb image use stb_tester
    :param num: Screenshot number
    :param ip: stb_tester ip
    :return: list_image: list of image ,Format for numpy
    """
    list_image = []
    for i in range(num):
        while True:
            try:
                result = requests.get("http://{}/api/v1/device/screenshot.png".format(ip))
                # dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                # print dt_ms
                break
            except:
                time.sleep(60)
                print("ekt_image_capture  Request error")
                logging.info("ekt_image_capture  Request error")
        image = cv2.imdecode(numpy.frombuffer(result.content, dtype='uint8'), 1)
        list_image.append(image)
    return list_image


if __name__ == '__main__':
    start_time = time.time()
    list_image = capture_image(20, "192.168.1.155")
    print(list_image)
    end_time = time.time()
    print start_time
    print end_time
    print end_time - start_time

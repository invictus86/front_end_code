#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import cv2
import numpy
import time

start_time = time.time()


def capture_image(num, ip):
    """
    capture stb image use stb_tester
    :param num: Screenshot number
    :param ip: stb_tester ip
    :return: list_image: list of image ,Format for numpy
    """
    list_image = []
    for i in range(num):
        result = requests.get("http://{}/api/v1/device/screenshot.png".format(ip))
        image = cv2.imdecode(numpy.frombuffer(result.content, dtype='uint8'), 1)
        list_image.append(image)
    return list_image


if __name__ == '__main__':
    list_image = capture_image(50, "192.168.1.154")
    print list_image
# end_time = time.time()
# print start_time
# print end_time
# print end_time-start_time
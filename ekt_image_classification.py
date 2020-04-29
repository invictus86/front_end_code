#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import cv2
import time
import ekt_image_capture


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
        result = requests.post('http://127.0.0.1:24401/', params={'threshold': 0.1}, data=img_str).json()
        # print result
        result_list.append(result["results"][0]["label"])

    for key in result_list:
        dict_result[key] = dict_result.get(key, 0) + 1
    # print dict_result.get("mosaic")
    # if dict_result.get("mosaic") == None or dict_result.get("mosaic") == 1:
    if dict_result.get("mosaic") == None or dict_result.get("mosaic") <= 6:
        mosaic_result = False
    else:
        print dict_result.get("mosaic")
        mosaic_result = True
    return dict_result, mosaic_result
    # return dict_result


if __name__ == '__main__':
    # start_time = time.time()
    num = 50
    list_image = ekt_image_capture.capture_image(num, "192.168.1.154")
    print list_image
    dict_result, mosaic_result = image_classification(list_image)
    # end_time = time.time()
    # print end_time-start_time
    print dict_result, mosaic_result

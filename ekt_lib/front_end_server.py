#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import base64
import json
import socket
import cv2
import logging
import numpy as np
import threading
import datetime
import os
import ekt_cfg

current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename='{}/ekt_log/front_end_server.log'.format(current_path),
                    filemode='a',  ##模式,有w和a,w就是写模式,每次都会重新写日志,覆盖之前的日志
                    # a是追加模式,默认如果不写的话,就是追加模式
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')  # 日志格式


class FrontEndServer():
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def read_image_file(self, image_name):
        img = cv2.imread(image_name, 1)
        shape = np.shape(img)
        img = np.array(img)
        img = img.tostring()
        img = base64.b64encode(img)

        data = {"img": img, "shape": shape}
        image_json = json.dumps(data, encoding='utf-8')
        return image_json

    def response(self):
        server = self.server
        server.bind((ekt_cfg.FRONT_END_SERVER_IP, ekt_cfg.FRONT_END_SERVER_PORT))
        server.listen(5)
        frequency = None
        bandwidth = None
        symbol_rate = None
        modulation = None
        lock_state = None
        sfe_state = "noral"
        strength_num = None
        quality_num = None
        stb_tester_run_state = "2"
        while True:
            conn, addr = server.accept()
            print ("%s connected" % (conn))
            while True:
                try:
                    data = conn.recv(1024)
                    print (type(data), "\n", data)
                    dict_data = json.loads(data)
                    if not data:
                        # print "%s disconnected"%conn
                        break
                    elif dict_data.get("cmd") == "set_frequency_data":
                        frequency = dict_data.get("frequency")
                        result = conn.send("set frequency data : {} ok ".format(frequency))
                        print ("result:", result, "current_time:{}, set frequency data : {} ok ".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), frequency))
                    elif dict_data.get("cmd") == "get_frequency_data":
                        result = conn.send(str(frequency))
                        print ("result:", result, "current_time:{}, get frequency data : {} ok ".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), frequency))
                    elif dict_data.get("cmd") == "set_symbol_rate_data":
                        symbol_rate = dict_data.get("symbol_rate")
                        result = conn.send("set symbol_rate data : {} ok ".format(symbol_rate))
                        print ("result:", result, "current_time:{}, set symbol_rate data : {} ok ".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), symbol_rate))
                    elif dict_data.get("cmd") == "get_symbol_rate_data":
                        result = conn.send(str(symbol_rate))
                        print ("result:", result, "current_time:{}, get symbol_rate data : {} ok ".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), symbol_rate))
                    elif dict_data.get("cmd") == "set_lock_state":
                        lock_state = dict_data.get("lock_state")
                        result = conn.send("set lock_state data : {} ok ".format(lock_state))
                        print ("result:", result, "current_time:{}, set lock_state data : {} ok ".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), lock_state))
                    elif dict_data.get("cmd") == "get_lock_state":
                        result = conn.send(lock_state)
                        print ("result:", result, "current_time:{}, get lock_state data : {} ok ".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), lock_state))
                    elif dict_data.get("cmd") == "set_stb_tester_run_state":
                        stb_tester_run_state = dict_data.get("stb_tester_run_state")
                        result = conn.send("set lock_state data : {} ok ".format(stb_tester_run_state))
                        print ("result:", result, "current_time:{}, set stb_tester run state : {} ok ".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), stb_tester_run_state))
                    elif dict_data.get("cmd") == "get_stb_tester_run_state":
                        result = conn.send(stb_tester_run_state)
                        print ("result:", result, "current_time:{}, get stb_tester run state : {} ok ".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), stb_tester_run_state))
                    elif dict_data.get("cmd") == "set_bandwidth_data":
                        bandwidth = dict_data.get("bandwidth")
                        result = conn.send("set bandwidth data : {} ok ".format(bandwidth))
                        print ("result:", result, "current_time:{}, set bandwidth data : {} ok ".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), bandwidth))
                    elif dict_data.get("cmd") == "get_bandwidth_data":
                        result = conn.send(str(bandwidth))
                        print ("result:", result, "current_time:{}, get bandwidth data : {} ok ".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), bandwidth))
                    elif dict_data.get("cmd") == "set_stb_crash":
                        result = conn.send("set stb crash state:ok ")
                        print ("result:", result, "current_time:{}, set stb crash state:ok ".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                        logging.info('set stb crash state:ok')
                    elif dict_data.get("cmd") == "set_strength_quality":
                        strength_num = dict_data.get("strength_num")
                        quality_num = dict_data.get("quality_num")
                        result = conn.send(
                            "set strength_num: {} ,quality_num: {} ok".format(strength_num, quality_num))
                        print ("result:", result, "current_time:{}, set strength_num: {} ,quality_num: {} ok ".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), strength_num, quality_num))
                    elif dict_data.get("cmd") == "get_strength_quality":
                        strength_quality_data = {"strength_num": strength_num, "quality_num": quality_num}
                        result = conn.send(json.dumps(strength_quality_data))
                        print ("result:", result, "current_time:{}, get strength_quality_data : {}  ok ".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), strength_quality_data))
                    elif dict_data.get("cmd") == "set_modulation_data":
                        modulation = dict_data.get("modulation")
                        result = conn.send("set modulation data : {} ok ".format(modulation))
                        print ("result:", result, "current_time:{}, set modulation data : {} ok ".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), modulation))
                    elif dict_data.get("cmd") == "get_modulation_data":
                        result = conn.send(str(modulation))
                        print ("result:", result, "current_time:{}, get modulation data : {} ok ".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), modulation))
                    elif dict_data.get("cmd") == "set_sfe_state":
                        sfe_state = dict_data.get("sfe_state")
                        result = conn.send("set sfe_state data : {} ok ".format(sfe_state))
                        print ("result:", result, "current_time:{}, set sfe_state data : {} ok ".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), sfe_state))
                    elif dict_data.get("cmd") == "get_sfe_state":
                        result = conn.send(sfe_state)
                        print ("result:", result, "current_time:{}, get sfe_state data : {} ok ".format(
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), sfe_state))
                    else:
                        print (data)
                        print ("unknown message")
                except:
                    break


if __name__ == '__main__':
    fes = FrontEndServer()
    # rvt.read_cfg_file()
    t = threading.Thread(target=fes.response)
    t.setDaemon(True)
    t.start()
    try:
        print ('Enter "Ctrl + C" to exit ')
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        print ("program exited")
        sys.exit(0)

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

logging.basicConfig(level=logging.NOTSET)
log = logging.getLogger("RVTserver")

# get local ip
addrs = socket.getaddrinfo(socket.gethostname(), None)
for item in addrs:
    if str(item[-1][0])[0:3] == "192":
        ip = str(item[-1][0])
        print "current ip is : {}".format(ip)

port = 9999


class RVTserver():
    # image_file, cfg_file = find_image_or_cfg_file()

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.img_json = None
        self.app_image = "./image_file/application.png"
        self.lock_success_image = "./image_file/lock_success.png"
        self.lock_fail_image = "./image_file/lock_fail.png"
        self.front_end_cfg_file = "./image_file/front_end_cfg.json"

    def read_image_file(self, image_name):
        img = cv2.imread(image_name, 1)
        shape = np.shape(img)
        img = np.array(img)
        img = img.tostring()
        img = base64.b64encode(img)

        data = {"img": img, "shape": shape}
        # print len(data), "lenth"
        image_json = json.dumps(data, encoding='utf-8')
        # print len(self.img_json)
        return image_json

    def read_cfg_file(self):
        with open(self.front_end_cfg_file, 'r') as f:
            dict_data = json.load(f, "utf-8")
            json_data = json.dumps(dict_data)
            self.json_data = json_data
            print json_data

    def response(self):
        server = self.server
        server.bind((ip, port))
        server.listen(5)
        image_app = self.read_image_file(self.app_image)
        image_lock_success = self.read_image_file(self.lock_success_image)
        image_lock_fail = self.read_image_file(self.lock_fail_image)
        frequency = None
        symbol_rate = None
        while True:
            conn, addr = server.accept()
            print "%s connected" % (conn)
            while True:
                try:
                    data = conn.recv(1024)
                    print type(data), "\n", data
                    dict_data = json.loads(data)
                    print dict_data
                    if not data:
                        # print "%s disconnected"%conn
                        break
                    elif dict_data.get("cmd") == "app_image":
                        result = conn.send(image_app)
                        print "result:", result, "send image app ok!"
                    elif dict_data.get("cmd") == "lock_success_image":
                        result = conn.send(image_lock_success)
                        print "result:", result, "send image lock success ok!"
                    elif dict_data.get("cmd") == "lock_fail_image":
                        result = conn.send(image_lock_fail)
                        print "result:", result, "send image lock fail ok!"
                    elif dict_data.get("cmd") == "read_json_data":
                        result = conn.send(str(self.json_data))
                        print "result:", result, "send read json data ok!"
                    elif dict_data.get("cmd") == "set_frequency_data":
                        print "*" * 50
                        frequency = dict_data.get("frequency")
                        result = conn.send("set frequency data : {} ok ".format(frequency))
                        print "result:", result, "set frequency data : {} ok ".format(frequency)
                    elif dict_data.get("cmd") == "get_frequency_data":
                        result = conn.send(str(frequency))
                        print "result:", result, "get frequency data : {} ok ".format(frequency)
                    elif dict_data.get("cmd") == "set_symbol_rate_data":
                        symbol_rate = dict_data.get("symbol_rate")
                        result = conn.send("set symbol_rate data : {} ok ".format(symbol_rate))
                        print "result:", result, "set symbol_rate data : {} ok ".format(symbol_rate)
                    elif dict_data.get("cmd") == "get_symbol_rate_data":
                        result = conn.send(str(symbol_rate))
                        print "result:", result, "get symbol_rate data : {} ok ".format(symbol_rate)
                    else:
                        print data
                        print "unknown message"
                except:
                    break


if __name__ == '__main__':
    rvt = RVTserver()
    rvt.read_cfg_file()
    t = threading.Thread(target=rvt.response)
    t.setDaemon(True)
    t.start()
    try:
        print 'Enter "Ctrl + C" to exit '
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        print "program exited"
        sys.exit(0)

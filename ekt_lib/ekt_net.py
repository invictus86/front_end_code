"""

version v0.1
author: kim.tang@ekt-digital.com
history:
v0.1:
init release
"""

import os
import sys
import socket
import string
import time


class NetError(Exception):
    """
    exception for net module command execute fail.
    """
    def __init__(self, desc):
        super(NetError, self).__init__()
        self.desc = desc

    def __str__(self):
        return "%s" % self.desc


class EktNetClient(object):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def __del__(self):
        self.sock.close()
        # print "EktNetClient exit"

    def connect(self):
        try:
            self.sock.connect((self.ip, self.port))
        except IOError, e:
            print 'there is error: ', e
            # raise NetError('init', 'cannot connect the server.')

    def send_data(self, data):
        try:
            self.sock.sendall(data)
        except IOError, e:
            print 'cannot send data ', e
            raise NetError('send', e)

    def rec_data(self):
        time.sleep(1)
        return self.sock.recv(1024)

    def send_rec(self, cmd):
        self.send_data(cmd)
        # print "send cmd=%s" % (cmd)
        data = self.sock.recv(1024)
        return data

    def __cmd_data(self, cmd , paras):
        data = ":" + cmd + " " + paras + "\r\n"
        try:
            self.sock.sendall(data)
        except IOError, e:
            print 'cannot send data ', e
            # raise NetError(e)

    def send_ok(self, cmd, paras):
        i = 1
        data = ":" + cmd + " " + "SUCCESS"
        self.__cmd_data(cmd, paras)
        while(i > 0):
            try:
                ret = self.rec_data()
            except socket.error, e:
                time.sleep(1)
                ret = None

            i -= 1
            if ret is None:
                continue

            if data in ret:
                #print "send cmd ok, send_data=%s, ret=%s" % (data, ret)
                return True, ret
            else:
                print "send cmd fail, send_data=%s, ret=%s" % (data, ret)
                raise NetError(ret)

        if i==0:
            raise NetError('send data timeout')
        else:
            return True

if __name__ == '__main__':
    pass
    # test1()

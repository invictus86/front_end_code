"""
version v0.1
author: kim.tang@ekt-digital.com
history:
v0.1:
init release
"""

import time
import ekt_net


class EktRelay(object):
    def __init__(self, ip="192.168.1.252", port=1030):
        self.ip = ip
        self.port = port
        self.sock = ekt_net.EktNetClient(self.ip, self.port)

    def __del__(self):
        del self.sock

    def relay_on_12v(self):
        """
        open a relay.
        :param id: int
            1, the first relay.
            2, the second relay.
        :return:
        """
        paras = bytearray.fromhex('48 3A 01 70 02 01 00 00 45 44')
        self.sock.send_data(paras)

    def relay_off_12v(self):
        """
        close a relay.
        :param id: see 'relay_on'
        :return:
        """
        paras = bytearray.fromhex('48 3A 01 70 02 00 00 00 45 44')
        self.sock.send_data(paras)

    def relay_on_sfe(self):
        """
        open a relay.
        :param id: int
            1, the first relay.
            2, the second relay.
        :return:
        """
        paras = bytearray.fromhex('48 3A 01 70 01 01 00 00 45 44')
        self.sock.send_data(paras)

    def relay_off_sfe(self):
        """
        close a relay.
        :param id: see 'relay_on'
        :return:
        """
        paras = bytearray.fromhex('48 3A 01 70 01 00 00 00 45 44')
        self.sock.send_data(paras)


if __name__ == '__main__':
    en = EktRelay()
    en.relay_off_sfe()
    time.sleep(5)
    en.relay_on_sfe()
    time.sleep(180)

print("Test Ctypes")
from ctypes import *

# lib = CDLL(r"H:\dll_calling\rssfu_64.dll")
lib = WinDLL(r"./rssfu_64.dll")
point_data = ""
res = lib.rssfu_init('TCPIP::192.168.1.50::INSTR', False, False, byref(point_data))
print(res)
# lib.TestCtypes()
#
# print(dllObj.rssfu_ConfigureDVBT2TransmissionL1T2Version("1", 2))

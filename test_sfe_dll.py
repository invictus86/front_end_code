print("Test Ctypes")
from ctypes import *

# lib = CDLL(r"H:\dll_calling\rssfu_64.dll")
lib = WinDLL(r"./rssfe_64.dll")
point_data = c_char_p(b"")
# point_data = None
res = lib.rssfe_init('TCPIP::192.168.1.47::INSTR', False, False, byref(point_data))
# res = lib.rssfe_init('TCPIP::192.168.1.47::INSTR', False, False)
print(res)
# lib.TestCtypes()
#
# print(dllObj.rssfu_ConfigureDVBT2TransmissionL1T2Version("1", 2))

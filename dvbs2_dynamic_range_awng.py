#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ekt_sfu
import time

CODE_RATE_1_2 = "R1_2"
CODE_RATE_2_3 = "R2_3"
CODE_RATE_3_4 = "R3_4"
CODE_RATE_5_6 = "R5_6"
CODE_RATE_7_8 = "R7_8"
CODE_RATE_8_9 = "R8_9"

MODULATION_QPSK = "S4"
MODULATION_8PSK = "S8"
MODULATION_16QAM = "S16"

SYMBOL_RATE_5M = "5.000000e6"
SYMBOL_RATE_10M = "10.000000e6"
SYMBOL_RATE_45M = "45.000000e6"
SYMBOL_RATE_27_5M = "27.500000e6"

FREQUENCY_950M = "950 MHz"
FREQUENCY_1550M = "1550 MHz"
FREQUENCY_2147M = "2147 MHz"

SYMBOL_TATE_LIST = [str(i) + ".000000e6" for i in range(5, 46)]
FREQUENCY_LIST = [str(i) + " MHz" for i in range(950, 2150, 20)]
FREQUENCY_LIST.append("2147 MHz")


def set_dvbs2_fixed_parameter(specan):
    specan.set_modulation_modulation_source("DTV")
    specan.set_modulation_modulation_standard_dvt("DVS2")

    specan.set_frequency_frequency_frequency("1000 MHz")
    time.sleep(5)
    specan.set_frequency_frequency_offset("0 Hz")
    specan.set_frequency_frequency_channel("0")

    specan.set_frequency_sweep_start("100 MHz")
    specan.set_frequency_sweep_stop("200 MHz")
    specan.set_frequency_sweep_center("150 MHz")
    specan.set_frequency_sweep_span("100 MHz")
    specan.set_frequency_sweep_spacing("LIN")
    specan.set_frequency_sweep_step("1 MHz")
    specan.set_frequency_sweep_dwell("100 ms")
    specan.set_frequency_sweep_mode("AUTO")
    specan.set_frequency_sweep_state("CW")

    specan.set_level_level_level("dBm", 0)
    specan.set_level_level_rf("ON")
    specan.set_level_level_offset("0")
    specan.set_level_level_userlimit("20")
    specan.set_level_level_mode("AUTO")
    specan.set_level_alc_state("OFF")


def set_dvbs_variable_parameter(specan, code_rate, modulation, symbol_rate, frequency, input_signal_level):
    specan.set_digitaltv_coding_constellation(modulation)
    specan.set_digitaltv_coding_coderate(code_rate)
    specan.set_digitaltv_coding_symbolrate(symbol_rate)
    specan.set_frequency_frequency_frequency(frequency)
    specan.set_level_level_level(input_signal_level)


if __name__ == '__main__':
    """
    测试流程：
    ①重置设备
    ②选择 TSPLAYER
    ③播放流文件
    ④设置code_rate，modulation，symbol_rate，frequency，input_signal_level
    ⑤机顶盒应用中进行锁台并确认锁台成功  （针对stb-tester发送post请求运行testcase，由于每款机顶盒界面、锁台操作不同，
    是否需要对testcase与PC端做参数交互？）
    ⑤依次修改可变参数，判断机顶盒画面是否含有马赛克并记录结果
    """
    net = "192.168.1.50"
    specan = ekt_sfu.Ektsfe(net)
    specan.preset_instrument()
    specan.set_digitaltv_input_source_dvbs2("TSPL")
    specan.set_player_timing_openfile(r"E:\333\HEVC\1280x720p_hevc_aac.ts")
    set_dvbs2_fixed_parameter(specan)

    # set_dvbs_variable_parameter(specan, "R1_2", "S4", "5.000000e6", "950 MHz", "-87 dBm")
    # set_dvbs_variable_parameter(specan, "R3_4", "S4", "5.000000e6", "1550 MHz", "-70 dBm")
    # time.sleep(5)
    # list_input_signal_level = ["-87 dBm", "-96 dBm", "-84 dBm"]
    # for level in list_input_signal_level:
    #     specan.set_level_level_level(level)
    #     time.sleep(10)

    # for symbol_rate in SYMBOL_TATE_LIST:
    #     specan.set_digitaltv_coding_symbolrate(symbol_rate)
    #     time.sleep(5)

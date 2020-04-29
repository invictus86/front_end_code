#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ekt_sfu
import time
import json

AWGN_ON = "ON"
AWGN_OFF = "OFF"

CODE_RATE_1_4 = "R1_4"
CODE_RATE_1_3 = "R1_3"
CODE_RATE_2_5 = "R2_5"
CODE_RATE_1_2 = "R1_2"
CODE_RATE_3_5 = "R3_5"
CODE_RATE_2_3 = "R2_3"
CODE_RATE_3_4 = "R3_4"
CODE_RATE_4_5 = "R4_5"
CODE_RATE_5_6 = "R5_6"
CODE_RATE_6_7 = "R6_7"
CODE_RATE_7_8 = "R7_8"
CODE_RATE_8_9 = "R8_9"
CODE_RATE_9_10 = "R9_10"

MODULATION_QPSK = "S4"
MODULATION_8PSK = "S8"
MODULATION_16QAM = "S16"

SYMBOL_RATE_5M = "5.000000e6"
SYMBOL_RATE_10M = "10.000000e6"
SYMBOL_RATE_27_5M = "27.500000e6"
SYMBOL_RATE_45M = "45.000000e6"

FREQUENCY_950M = "950 MHz"
FREQUENCY_1550M = "1550 MHz"
FREQUENCY_2147M = "2147 MHz"

AWGN_LIST = [AWGN_ON, AWGN_OFF]
SYMBOL_RATE_LIST = [SYMBOL_RATE_5M, SYMBOL_RATE_10M, SYMBOL_RATE_27_5M, SYMBOL_RATE_45M]
MODULATION_LIST = [MODULATION_QPSK, MODULATION_8PSK]

SYMBOL_TATE_LIST = [str(i) + ".000000e6" for i in range(5, 46)]
FREQUENCY_LIST = [str(i) + " MHz" for i in range(950, 2150, 20)]
FREQUENCY_LIST.append("2147 MHz")

#    DVBS2   QPSK
dict_config_data = {
    "MODULATION": [MODULATION_QPSK, MODULATION_8PSK],
    "CODE_RATE_DVBS2_QPSK": [CODE_RATE_1_2, CODE_RATE_3_5, CODE_RATE_2_3, CODE_RATE_3_4, CODE_RATE_4_5, CODE_RATE_5_6,
                             CODE_RATE_8_9, CODE_RATE_9_10],
    "CODE_RATE_DVBS2_8PSK": [CODE_RATE_3_5, CODE_RATE_2_3, CODE_RATE_3_4, CODE_RATE_5_6, CODE_RATE_8_9, CODE_RATE_9_10],
    "SYMBOL_RATE": [SYMBOL_RATE_5M, SYMBOL_RATE_27_5M, SYMBOL_RATE_45M],

}


def read_ekt_config_data(file_path):
    with open(file_path, 'r') as f:
        dict_data = json.load(f, "utf-8")
        # print dict_data
        # print type(dict_data)
        return dict_data


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

    specan.set_level_level_rf("ON")
    specan.set_level_level_userlimit("20")
    specan.set_level_level_mode("AUTO")
    specan.set_level_settings_unit("DBM")
    specan.set_level_level_offset("0")
    specan.set_level_alc_state("OFF")
    specan.set_level_level_level("dBm", 0)

    specan.set_modulation_modulation_modulation("ON")
    specan.set_modulation_modulation_source("DTV")
    specan.set_modulation_modulation_standard_dvt("DVS2")
    specan.set_modulation_modulation_spectrum("NORMal")
    specan.set_modulation_settings_level("AUTO")
    specan.set_modulation_settings_factor("6")
    specan.set_modulation_settings_filtering("OFF")
    specan.set_modulation_settings_mode("NRWN")
    specan.set_modulation_settings_output("OFF")

    specan.set_digitaltv_input_source_dvbs2("TSPL")
    specan.set_digitaltv_coding_symbolrate_dvbs2("31.711e6")
    specan.set_digitaltv_coding_constellation_dvbs2("S8")
    specan.set_digitaltv_coding_rolloff_dvbs2("0.15")
    specan.set_digitaltv_coding_coderate_dvbs2("R1_2")
    specan.set_digitaltv_coding_fecframe_dvbs2("NORM")
    specan.set_digitaltv_coding_pilots_dvbs2("OFF")

    specan.set_digitaltv_special_settings_dvbs2("ON")

    specan.set_digitaltv_phasenoise_phasenoise_dvbs2("ON")
    specan.set_digitaltv_phasenoise_shape_dvbs2("SHA1")
    specan.set_digitaltv_phasenoise_magnitude_dvbs2("32")

    specan.set_digitaltv_settings_tspacket_dvbs2("H184")
    specan.set_digitaltv_settings_pidpacket_dvbs2("NULL")
    specan.set_digitaltv_settings_payloadtest_dvbs2("PRBS")

    specan.set_interferer_source("ATVPr")
    specan.set_impairments_modulator("ON")
    specan.set_impairments_baseband("OFF")
    specan.set_impairments_optimize("ON")

    specan.set_noise_noise_noise("ADD")
    specan.set_noise_noise_awgn("ON")
    specan.set_noise_awgn_cn("20")

    specan.set_noise_settings_bandwith("ON")
    specan.set_noise_settings_receiver("7.5e6")


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
    可变参数设置顺序
    ①AWGN_LIST
    ②SYMBOL_RATE_LIST
    ③MODULATION_LIST
    ④CODE_RATE 和 CN
    ⑤FREQUENCY 和 OFFSET
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

    dict_data = read_ekt_config_data("./ekt_config.json")
    DVBS_S2_FREQUENCY_LEVEL_OFFSET = dict_data.get("DVBS_S2_FREQUENCY_LEVEL_OFFSET")
    DVBS2_QPSK_CODE_RATE_CN = dict_data.get("DVBS2_QPSK_CODE_RATE_CN")
    DVBS2_8PSK_CODE_RATE_CN = dict_data.get("DVBS2_8PSK_CODE_RATE_CN")

    for AWGN in AWGN_LIST:
        specan.set_noise_noise_awgn(AWGN)
        for SYMBOL_RATE in SYMBOL_RATE_LIST:
            specan.set_digitaltv_coding_symbolrate(SYMBOL_RATE)
            for MODULATION in MODULATION_LIST:
                specan.set_digitaltv_coding_constellation(MODULATION)
                if MODULATION == MODULATION_QPSK:
                    for i in range(len(DVBS2_QPSK_CODE_RATE_CN)):
                        specan.set_digitaltv_coding_coderate(DVBS2_QPSK_CODE_RATE_CN[i][0])
                        specan.set_noise_awgn_cn(str(DVBS2_QPSK_CODE_RATE_CN[i][1]))
                        for FREQUENCY_LEVEL_OFFSET in DVBS_S2_FREQUENCY_LEVEL_OFFSET:
                            specan.set_frequency_frequency_frequency(str(FREQUENCY_LEVEL_OFFSET[0]) + "MHz")
                            specan.set_level_level_offset(str(FREQUENCY_LEVEL_OFFSET[1]))
                            """
                            进行机顶盒的频率修改或其他参数的修改
                            读取误码率或者判断机顶盒是否含有马赛克
                            """
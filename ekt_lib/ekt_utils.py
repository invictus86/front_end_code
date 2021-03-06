#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import json
import pandas as pd


def set_dvbs2_fixed_parameter(specan):
    """
    DVB-S2 set example
    :param specan:
    :return:
    """
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


def write_test_result(file_path, content):
    """
    write content to file
    :param file_path:  file path
    :param content: content
    :return:
    """
    with open(file_path, "a") as f:
        f.write(content)


def read_ekt_config_data(file_path):
    """
    read ekt_config.json and return the dict data
    :param file_path: ekt_config.json file path
    :return: dict data
    """
    with open(file_path, 'r') as f:
        dict_data = json.load(f, "utf-8")
        return dict_data


def generate_symbol_rate_list():
    """
    test cases generate symbol rate list
    :return: symbol rate list
    """
    SYMBOL_TATE_LIST = []
    for i in range(5, 46):
        if i < 10:
            SYMBOL_TATE_LIST.append([str(i) + ".000000e6", "0{}000".format(i), i])
        else:
            SYMBOL_TATE_LIST.append([str(i) + ".000000e6", "{}000".format(i), i])
    return SYMBOL_TATE_LIST


def find_level_offset_by_frequency(frequency_offset_type, frequency):
    """
    find level offset by frequency from ekt_config.json
    :param frequency_offset_type: the type of frequency offset
    :param frequency: the frequency you want to use
    :return: frequency level offset
    """
    dict_data = read_ekt_config_data("../../ekt_lib/ekt_config.json")
    FREQUENCY_LEVEL_OFFSET_LIST = dict_data.get(frequency_offset_type)
    for FREQUENCY_LEVEL_OFFSET in FREQUENCY_LEVEL_OFFSET_LIST:
        if FREQUENCY_LEVEL_OFFSET[0] == frequency:
            return FREQUENCY_LEVEL_OFFSET[1]


def read_json_file(file_path):
    """
    read json file from file path
    :param file_path:
    :return:
    """
    with open(file_path, 'r') as load_f:
        load_dict = json.load(load_f)
    return load_dict


def get_ldata_from_lf_fftsize(lf, fftsize):
    """
    get ldata from lf and fftsize
    :param lf:l_f data
    :param fftsize:fftsize_tyoe
    :return:ldata
    """
    dict_fftsize_diffence = {
        "M1K": 16,
        "M2K": 8,
        "M4K": 4,
        "M8K": 2,
        "M8E": 2,
        "M16K": 1,
        "M16E": 1,
        "M32K": 1,
        "M32E": 1
    }
    ldata = lf - dict_fftsize_diffence.get(fftsize)
    return ldata


def write_json_file(file_path, load_dict):
    """
    write json file from file path
    :param file_path:the path of file
    :param load_dict:dict data you want to write
    :return:
    """
    with open(file_path, "w") as dump_f:
        json.dump(load_dict, dump_f)


def dvbs_dynamic_max_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[2]:
            if count == 0:
                list_required_data.append([i[0][1], i[1][0], j[0][0], j[1]])
            else:
                list_required_data.append(["", "", j[0][0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data, columns=['symbol_rate', 'frequency', 'code_rate', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbc_1_dynamic_range_awng_max_level_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[3]:
            if count == 0:
                list_required_data.append([i[0], i[1][1], i[2], j[0][0], j[1]])
            else:
                list_required_data.append(['', '', '', j[0][0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data, columns=['modulation', 'symbol_rate', 'CN', 'frequency', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbc_1_dynamic_range_awng_min_level_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[3]:
            if count == 0:
                list_required_data.append([i[0], i[1][1], i[2], j[0][0], j[1], j[2], j[3]])
            else:
                list_required_data.append(['', '', '', j[0][0], j[1], j[2], j[3]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['modulation', 'symbol_rate', 'CN', 'frequency', 'min_RF_level', "max_RF_result(-10db)",
                                    "sensitivity_outcome"])
    pd_data.to_csv(csv_path, index=None)


def dvbc_2_channel_bandwidth_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[3], i[4][1], i[5]])
    pd_data = pd.DataFrame(list_required_data, columns=['frequency', 'modulation', 'symbol_rate', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbc_3_cn_test_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[3]:
            if count == 0:
                list_required_data.append([i[0], i[1][1], i[2], j[0], j[1]])
            else:
                list_required_data.append(['', '', '', j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data, columns=['modulation', 'symbol_rate', 'spec', 'frequency', 'noise_cn'])
    pd_data.to_csv(csv_path, index=None)


def dvbc_4_symbol_rate_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[6]:
            if count == 0:
                list_required_data.append([i[0], i[1], i[4], i[5], j[0][1], j[1]])
            else:
                list_required_data.append(['', '', '', '', j[0][1], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['modulation', 'frequency', 'level', 'cn', 'symbol_rate', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbc_5_IQ_inverted_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[4]:
            if count == 0:
                list_required_data.append([i[0], i[1][1], i[2], i[3], j[0], j[1]])
            else:
                list_required_data.append(['', '', '', '', j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['modulation', 'symbol_rate', 'level', 'cn', 'frequency', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbc_7_analogue_adjacent_carrier_interference_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[3]:
            if count == 0:
                list_required_data.append([i[0], i[1][1], i[2], j[0], j[1]])
            else:
                list_required_data.append(['', '', '', j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['modulation', 'symbol_rate', 'spec', 'frequency', 'level'])
    pd_data.to_csv(csv_path, index=None)


def dvbc_7_analogue_adjacent_carrier_interference_N_1_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[3]:
            if count == 0:
                list_required_data.append([i[0], i[1][1], i[2], j[0], j[1]])
            else:
                list_required_data.append(['', '', '', j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['modulation', 'symbol_rate', 'spec', 'frequency', 'level'])
    pd_data.to_csv(csv_path, index=None)


def dvbc_8_symbol_error_rate_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[2]:
            if count == 0:
                list_required_data.append([i[0][0], i[0][1], i[1], j[0], j[1]])
            else:
                list_required_data.append(['', '', '', j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['sfu_symbol_rate', 'stb_symbol_rate', 'frequency', 'modulation', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbc_9_frequency_error_rate_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[2]:
            if count == 0:
                list_required_data.append([i[0][1], i[1][0], i[1][1], j[0], j[1]])
            else:
                list_required_data.append(['', '', '', j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['symbol_rate', 'stb_frequency', 'sfu_frequency', 'modulation', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbc_10_frequency_capture_range_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[2]:
            if count == 0:
                list_required_data.append([i[0][1], i[1][0], i[1][1], j[0], j[1]])
            else:
                list_required_data.append(['', '', '', j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['symbol_rate', 'stb_frequency', 'sfu_frequency', 'modulation', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def j83_1_dynamic_range_awng_max_level_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[3]:
            if count == 0:
                list_required_data.append([i[0], i[1][1], i[2], j[0][0], j[1]])
            else:
                list_required_data.append(['', '', '', j[0][0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data, columns=['modulation', 'symbol_rate', 'CN', 'frequency', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def j83_1_dynamic_range_awng_min_level_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[3]:
            if count == 0:
                list_required_data.append([i[0], i[1][1], i[2], j[0][0], j[1]])
            else:
                list_required_data.append(['', '', '', j[0][0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data, columns=['modulation', 'symbol_rate', 'CN', 'frequency', 'level'])
    pd_data.to_csv(csv_path, index=None)


def j83_2_channel_bandwidth_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[3], i[4][1], i[5]])
    pd_data = pd.DataFrame(list_required_data, columns=['frequency', 'modulation', 'symbol_rate', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def j83_3_cn_test_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[3]:
            if count == 0:
                list_required_data.append([i[0], i[1][1], i[2], j[0], j[1]])
            else:
                list_required_data.append(['', '', '', j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data, columns=['modulation', 'symbol_rate', 'spec', 'frequency', 'noise_cn'])
    pd_data.to_csv(csv_path, index=None)


def j83_5_IQ_inverted_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[4]:
            if count == 0:
                list_required_data.append([i[0], i[1][1], i[2], i[3], j[0], j[1]])
            else:
                list_required_data.append(['', '', '', '', j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['modulation', 'symbol_rate', 'level', 'cn', 'frequency', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def j83_7_analogue_adjacent_carrier_interference_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[3]:
            if count == 0:
                list_required_data.append([i[0], i[1][1], i[2], j[0], j[1]])
            else:
                list_required_data.append(['', '', '', j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['modulation', 'symbol_rate', 'spec', 'frequency', 'level'])
    pd_data.to_csv(csv_path, index=None)


def j83_7_analogue_adjacent_carrier_interference_N_1_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[3]:
            if count == 0:
                list_required_data.append([i[0], i[1][1], i[2], j[0], j[1]])
            else:
                list_required_data.append(['', '', '', j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['modulation', 'symbol_rate', 'spec', 'frequency', 'level'])
    pd_data.to_csv(csv_path, index=None)


def j83_8_symbol_error_rate_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[2]:
            if count == 0:
                list_required_data.append([i[0][0], i[0][1], i[1], j[0], j[1]])
            else:
                list_required_data.append(['', '', '', j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['sfu_symbol_rate', 'stb_symbol_rate', 'frequency', 'modulation', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def j83_9_frequency_error_rate_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[2]:
            if count == 0:
                list_required_data.append([i[0][1], i[1][0], i[1][1], j[0], j[1]])
            else:
                list_required_data.append(['', '', '', j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['symbol_rate', 'stb_frequency', 'sfu_frequency', 'modulation', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def j83_10_frequency_capture_range_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[2]:
            if count == 0:
                list_required_data.append([i[0][1], i[1][0], i[1][1], j[0], j[1]])
            else:
                list_required_data.append(['', '', '', j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['symbol_rate', 'stb_frequency', 'sfu_frequency', 'modulation', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbs_dynamic_min_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[2]:
            if j[1] == "NO NEED TEST":
                continue
            if count == 0:
                list_required_data.append([i[0][1], i[1][0], j[0][0], j[1], j[2], j[3]])
            else:
                list_required_data.append(["", "", j[0][0], j[1], j[2], j[3]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['symbol_rate', 'frequency', 'code_rate', 'min_RF_level', "max_RF_result(-10db)", "sensitivity_outcome"])
    pd_data.to_csv(csv_path, index=None)


def dvbs_dynamic_min_json_class_test(json_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    for i in list_data:
        for j in i[2]:
            if i[1][0] not in [950, 1550, 2150] and (j[0][0] != "R7_8" or i[0][1] != "45000"):
                j[1] = "NO NEED TEST"
                j[2] = "NO NEED TEST"
                j[3] = "NO NEED TEST"
    write_json_file(json_path, load_dict)


def dvbs_signal_acquisition_frequency_range_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[3]:
            if count == 0:
                list_required_data.append([i[1], i[2][0], i[2][1], j[0], j[1]])
            else:
                list_required_data.append(["", "", "", j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data, columns=['symbol_rate', 'frequency', 'sfu_frequency', 'code_rate', 'level'])
    pd_data.to_csv(csv_path, index=None)


def dvbs_signal_tracking_frequency_range_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[3]:
            if count == 0:
                list_required_data.append([i[1], i[2][0], i[2][1], j[0], j[1]])
            else:
                list_required_data.append(["", "", "", j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data, columns=['symbol_rate', 'frequency', 'sfu_frequency', 'code_rate', 'level'])
    pd_data.to_csv(csv_path, index=None)


def dvbs_symbol_err_rate_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[1]:
            if count == 0:
                list_required_data.append([i[0][0], i[0][1], j[0], j[1]])
            else:
                list_required_data.append(["", "", j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data, columns=['sfu_symbol_rate', 'stb_symbol_rate', 'code_rate', 'test_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbs_symbol_rate_step_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0][0], i[0][1], i[1]])
    pd_data = pd.DataFrame(list_required_data, columns=['sfu_symbol_rate', 'stb_symbol_rate', 'test_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbs2_18_dynamic_range_awng_max_level_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[2]:
            if count == 0:
                list_required_data.append([i[0][1], i[1][0], j[0], j[1][0], j[2]])
            else:
                list_required_data.append(["", "", j[0], j[1][0], j[2]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data, columns=['symbol_rate', 'frequency', 'modulation', 'code_rate', 'level'])
    pd_data.to_csv(csv_path, index=None)


def dvbs2_18_dynamic_min_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[2]:
            if j[2] == "NO NEED TEST":
                continue
            if count == 0:
                list_required_data.append([i[0][1], i[1][0], j[0], j[1][0], j[2], j[3], j[4]])
            else:
                list_required_data.append(["", "", j[0], j[1][0], j[2], j[3], j[4]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['symbol_rate', 'frequency', 'modulation', 'code_rate', 'min_RF_level', "max_RF_result(-10db)",
                                    "sensitivity_outcome"])
    pd_data.to_csv(csv_path, index=None)


def dvbs2_18_dynamic_min_json_class_test(json_path):
    """
    json to csv
    :param json_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    for i in list_data:
        for j in i[2]:
            if i[1][0] not in [950, 1550, 2150] and (j[1][0] != "R9_10" or i[0][1] != "45000" or j[0] != "S8"):
                j[2] = "NO NEED TEST"
                j[3] = "NO NEED TEST"
    write_json_file(json_path, load_dict)


def dvbs2_19_symbol_rate_step_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0][0], i[0][1], i[1]])
    pd_data = pd.DataFrame(list_required_data, columns=['sfu_symbol_rate', 'stb_symbol_rate', 'test_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbs2_22_phase_distortion_test_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[2]:
            if count == 0:
                list_required_data.append([i[0][1], i[1][0], j[0], j[1]])
            else:
                list_required_data.append(["", "", j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data, columns=['stb_symbol_rate', 'frequency', 'code_rate', 'test_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbs2_23_amplitude_distortion_test_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[2]:
            if count == 0:
                list_required_data.append([i[0][1], i[1][0], j[0], j[1]])
            else:
                list_required_data.append(["", "", j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data, columns=['stb_symbol_rate', 'frequency', 'code_rate', 'test_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbs2_24_symbol_err_rate_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[1]:
            if count == 0:
                list_required_data.append([i[0][0], i[0][1], j[0][0], j[1]])
            else:
                list_required_data.append(["", "", j[0][0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data, columns=['sfu_symbol_rate', 'stb_symbol_rate', 'code_rate', 'test_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbs2_25_signal_acquisition_frequency_range_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[3]:
            if count == 0:
                list_required_data.append([i[1], i[2][0], i[2][1], j[0][0], j[1]])
            else:
                list_required_data.append(["", "", "", j[0][0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data, columns=['symbol_rate', 'frequency', 'sfu_frequency', 'code_rate', 'level'])
    pd_data.to_csv(csv_path, index=None)


def dvbs2_26_signal_tracking_frequency_range_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[3]:
            if count == 0:
                list_required_data.append([i[1], i[2][0], i[2][1], j[0][0], j[1]])
            else:
                list_required_data.append(["", i[2][0], i[2][1], j[0][0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data, columns=['symbol_rate', 'frequency', 'sfu_frequency', 'code_rate', 'level'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_4_centre_frequencies_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[1], i[2]])
    pd_data = pd.DataFrame(list_required_data, columns=['frequency', 'bandwidth', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_5_frequency_offset_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[1], i[2], i[3]])
    pd_data = pd.DataFrame(list_required_data, columns=['frequency', 'bandwidth', 'offset', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_6_signal_bandwidth_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[1], i[2]])
    pd_data = pd.DataFrame(list_required_data, columns=['frequency', 'bandwidth', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_7_modes_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[1], i[2], i[3], i[4]])
    pd_data = pd.DataFrame(list_required_data, columns=['fft_size', 'modulation', 'code_rate', 'guard', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_13_verification_strength_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[1]:
            if count == 0:
                list_required_data.append([i[0][0], i[0][1], i[0][2], i[0][3], i[0][4], j[0], j[1]])
            else:
                list_required_data.append(["", "", "", "", "", j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['modulation', 'code_rate', 'guard', 'bandwidth', 'frequency', 'level', 'strength'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_14_verification_quality_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[4]:
            if count == 0:
                list_required_data.append([i[0], i[1], i[2], i[3], j[0], j[1]])
            else:
                list_required_data.append(["", "", "", "", j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['modulation', 'code_rate', 'guard', 'fft_mode', 'CN', 'quality'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_15_changes_modulation_parameters_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[1], i[2], i[3], i[4]])
    pd_data = pd.DataFrame(list_required_data,
                           columns=['fftmode', 'modulation', 'code_rate', 'guard', 'test_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_19_gaussian_channel_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[1]:
            if j[4] == "NO NEED TEST":
                continue
            if count == 0:
                list_required_data.append([i[0][0], j[0], j[1], j[2], j[3], j[4], j[5]])
            else:
                list_required_data.append(["", j[0], j[1], j[2], j[3], j[4], j[5]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['frequency', 'modulation', 'code_rate', 'guard', 'spec', 'min_noise_level', 'sensitivity_outcome'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_19_gaussian_channel_json_class_test(json_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    for i in list_data:
        for j in i[1]:
            if i[0][0] not in [177.5, 198.5, 226.5, 474.0, 522.0, 570.0, 618.0, 666.0, 714.0, 762.0, 810.0, 858.0] and (
                    j[0] != "T64" or j[1] != "R7_8" or j[2] != "G1_4"):
                j[4] = "NO NEED TEST"
    write_json_file(json_path, load_dict)


def dvbt_20_performance_0db_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[4]:
            if count == 0:
                list_required_data.append([i[0], i[3], j[0], j[1], j[2], j[3], j[4], j[5]])
            else:
                list_required_data.append(["", "", j[0], j[1], j[2], j[3], j[4], j[5]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['frequency', 'bandwidth', 'pilot', 'modulation', 'code_rate', 'guard', 'spec_noise',
                                    'noise'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_21_receiver_signal_input__min_level_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[1]:
            if j[4] == "NO NEED TEST":
                continue
            if count == 0:
                list_required_data.append([i[0][0], j[0], j[1], j[2], j[3], j[4], j[5]])
            else:
                list_required_data.append(["", j[0], j[1], j[2], j[3], j[4], j[5]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['frequency', 'modulation', 'code_rate', 'guard', 'spec', 'min_RF_level', 'sensitivity_outcome'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_21_receiver_signal_input__min_level_json_class_test(json_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    for i in list_data:
        for j in i[1]:
            if i[0][0] not in [177.5, 198.5, 226.5, 474.0, 522.0, 570.0, 618.0, 666.0, 714.0, 762.0, 810.0, 858.0] and (
                    j[0] != "T64" or j[1] != "R7_8" or j[2] != "G1_4"):
                j[4] = "NO NEED TEST"
    write_json_file(json_path, load_dict)


def dvbt_22_minimun_level_0db_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        for j in i[4]:
            count_j = 0
            for k in j[5]:
                if count_j == 0:
                    list_required_data.append([i[0], i[3], j[0], j[1], j[2], j[3], j[4], k[0], k[1]])
                else:
                    list_required_data.append(["", "", "", "", "", "", "", k[0], k[1]])
                count_j = count_j + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['frequency', 'bandwidth', 'pilot', 'modulation', 'code_rate', 'guard', 'spec_level',
                                    'fading',
                                    'level'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_24_receiver_maximum_level_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[1], i[2], i[3], i[4], i[5]])
    pd_data = pd.DataFrame(list_required_data,
                           columns=['fft_mode', 'modulation', 'code_rate', 'guard', 'spec_level', 'level'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_25_analogue_signal_other_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[2]:
            if count == 0:
                list_required_data.append([i[0], i[1], j[0], j[1], j[2], j[3], j[4]])
            else:
                list_required_data.append(["", "", j[0], j[1], j[2], j[3], j[4]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['frequency', 'spec', 'fft_mode', 'modulation', 'code_rate', 'guard', 'level'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_28_analogue_signal_other_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[3]:
            if count == 0:
                list_required_data.append([i[0], j[0], j[1], j[2], j[3], j[4], j[5]])
            else:
                list_required_data.append(["", j[0], j[1], j[2], j[3], j[4], j[5]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['frequency', 'fft_mode', 'modulation', 'code_rate', 'guard', 'spec', 'noise_cn'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_29_performance_time_varying_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]])
    pd_data = pd.DataFrame(list_required_data,
                           columns=['fft_mode', 'modulation', 'code_rate', 'guard', 'spec_noise', 'delay',
                                    "freq_sparation", 'noise_cn'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_30_synchronisation_varying_echo_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]])
    pd_data = pd.DataFrame(list_required_data,
                           columns=['fft_mode', 'modulation', 'code_rate', 'guard', 'spec_noise', 'delay',
                                    "freq_sparation", 'noise_cn'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_31_performance_SFN_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[5]:
            if count == 0:
                list_required_data.append([i[0], i[1], i[2], i[3], i[4], j[0], j[1], j[2], j[3], j[4], j[5], j[6]])
            else:
                list_required_data.append(["", "", "", "", "", j[0], j[1], j[2], j[3], j[4], j[5], j[6]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['fft_mode', 'modulation', 'code_rate', 'guard', 'spec', 'mian_att', 'mian_delay',
                                    'pre_att', 'pre_delay', 'post_att', 'post_delay', 'noise_cn'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_32_performance_SFN_inside_guard_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        for j in i[9]:
            count_j = 0
            for k in j[3]:
                if k[1] == "NO NEED TEST":
                    continue
                if count_j == 0:
                    list_required_data.append([i[0], i[3], i[4], i[5], i[6], i[7], i[8], j[0], j[1], j[2], k[0], k[1]])
                else:
                    list_required_data.append(['', '', '', '', '', '', '', j[0], j[1], j[2], k[0], k[1]])
                count_j = count_j + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['frequency', 'bandwidth', 'fft_mode', 'modulation', 'code_rate', 'guard', 'spec',
                                    'mian_att', 'mian_delay',
                                    'pre_delay', 'pre_att', 'noise_cn'])
    pd_data.to_csv(csv_path, index=None)


def dvbt_32_performance_SFN_inside_guard_json_class_test(json_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    for i in list_data:
        for j in i[9]:
            for k in j[3]:
                if k[0] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] and j[2] in [28, -28] and \
                        i[5] == "T64" and i[6] == "R2_3" and i[7] == "G1_8" and i[3] == 8:
                    continue

                if k[0] in [1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20] and j[2] in [1.95, 28, 90, 150, 190.0, 220.0,
                                                                                           -1.95, -28, -90, -150, -190.0, -220.0,
                                                                                           20, 70, 110.0, -20, -70, -90, -110.0,
                                                                                           252, -252, 126, -126]:
                    k[1] = "NO NEED TEST"
    write_json_file(json_path, load_dict)


def dvbt_33_performance_SFN_outside_guard_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[8]:
            if count == 0:
                list_required_data.append([i[0], i[3], i[4], i[5], i[6], i[7], j[0], j[1], j[2], j[3]])
            else:
                list_required_data.append(['', '', '', '', '', '', j[0], j[1], j[2], j[3]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['frequency', 'bandwidth', 'fft_mode', 'modulation', 'code_rate', 'guard',
                                    'mian_att', 'mian_delay', 'pre_delay', 'pre_att'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_34_centre_frequencies_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[1], i[2]])
    pd_data = pd.DataFrame(list_required_data, columns=['frequency', 'bandwidth', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_35_frequency_offset_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[1], i[2], i[3]])
    pd_data = pd.DataFrame(list_required_data, columns=['frequency', 'bandwidth', 'offset', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_36_signal_bandwidths_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[3], i[4], i[5], i[6], i[7], i[8], i[9]])
    pd_data = pd.DataFrame(list_required_data,
                           columns=['frequency', 'bandwidth', 'fft_size', 'modulation', 'pilot', 'code_rate', 'guard', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_37_modes_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[1], i[2], i[3], i[5], i[6]])
    pd_data = pd.DataFrame(list_required_data, columns=['modulation', 'code_rate', 'fft_size', 'pilot', 'guard', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_37_modes_supplument_1_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[1]])
    pd_data = pd.DataFrame(list_required_data, columns=['Rotation', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_37_modes_supplument_2_papr_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[1]])
    pd_data = pd.DataFrame(list_required_data, columns=['PAPR', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_37_modes_supplument_3_fft_pilot_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[1], i[2], i[3], i[5], i[6]])
    pd_data = pd.DataFrame(list_required_data, columns=['modulation', 'code_rate', 'fft_size', 'pilot', 'guard', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_44_normal_mode_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[3], i[4], i[5], i[6], i[7], i[8], i[9]])
    pd_data = pd.DataFrame(list_required_data,
                           columns=['frequency', 'bandwidth', 'fft_size', 'modulation', 'pilot', 'code_rate', 'guard', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_51_verification_strength_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[6]:
            if count == 0:
                list_required_data.append([i[0][0], i[1], i[2], i[3], i[4], i[5], j[0], j[1]])
            else:
                list_required_data.append(["", "", "", "", "", "", j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['frequency', 'modulation', 'pilot', 'code_rate', 'guard', 'bandwidth', 'level',
                                    'strength'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_52_verification_quality_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[5]:
            if count == 0:
                list_required_data.append([i[0], i[1], i[2], i[3], i[4], j[0], j[1]])
            else:
                list_required_data.append(["", "", "", "", "", j[0], j[1]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['modulation', 'pilot', 'code_rate', 'guard', 'bandwidth', 'CN', 'quality'])

    pd_data.to_csv(csv_path, index=None)


def dvbt2_53_changes_modulation_parameters_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[1], i[2], i[3], i[4], i[6], i[7]])
    pd_data = pd.DataFrame(list_required_data,
                           columns=['fft_size', 'modulation', 'pilot', 'code_rate', 'guard', 'rp_level', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_53_changes_modulation_supplement_2_PARP_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]])
    pd_data = pd.DataFrame(list_required_data,
                           columns=['fft_size', 'modulation', 'pilot', 'code_rate', 'guard', 'PAPR', 'rp_level', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_54_time_interleaving_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[1], i[2], i[3], i[4]])
    pd_data = pd.DataFrame(list_required_data,
                           columns=['type', 'length', 'block', 'l_f', 'mosic_result'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_57_gaussian_channel_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[1]:
            if j[3] == "NO NEED TEST":
                continue
            if count == 0:
                list_required_data.append([i[0][0], j[0], j[1], j[2], j[3], j[4]])
            else:
                list_required_data.append(["", j[0], j[1], j[2], j[3], j[4]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['frequency', 'modulation', 'code_rate', 'spec', 'min_test_value', 'sensitivity_outcome'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_57_gaussian_channel_json_class_test(json_path):
    """
    json class
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    for i in list_data:
        for j in i[1]:
            if i[0][0] not in [177.5, 198.5, 226.5, 474.0, 522.0, 570.0, 618.0, 666.0, 714.0, 762.0, 810.0, 858.0] and (
                    j[0] != "T256" or j[1] != "R5_6"):
                j[3] = "NO NEED TEST"
    write_json_file(json_path, load_dict)


def dvbt2_58_performance_0db_echo_channel_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[1]:
            if count == 0:
                list_required_data.append([i[0], j[0], j[1], j[2], j[3], j[4], j[5]])
            else:
                list_required_data.append(['', j[0], j[1], j[2], j[3], j[4], j[5]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data, columns=['frequency', 'modulation', 'pilot', 'code_rate', 'guard', 'spec', 'noise'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_60_minuimun_level_0db_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    i = list_data

    count = 0
    for j in i[2]:
        if count == 0:
            list_required_data.append([i[0], j[0], j[1], j[2], j[3], j[4], j[5], j[6], j[7], j[8]])
        else:
            list_required_data.append(["", j[0], j[1], j[2], j[3], j[4], j[5], j[6], j[7], j[8]])
        count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['frequency', 'fft_size', 'modulation', 'pilot', 'code_rate', 'guard', 'bandwidth',
                                    'spec', 'delay', 'level'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_62_maximum_level_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        list_required_data.append([i[0], i[1], i[2], i[3], i[4], i[5], i[6]])
    pd_data = pd.DataFrame(list_required_data,
                           columns=['fft_size', 'modulation', 'pilot', 'code_rate', 'guard', 'spec_level', 'level'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_65_co_channel_interference_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[3]:
            if count == 0:
                list_required_data.append([i[0], j[0], j[1], j[2], j[3], j[4], j[5], j[6]])
            else:
                list_required_data.append(["", j[0], j[1], j[2], j[3], j[4], j[5], j[6]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['frequency', 'fft_mode', 'modulation', "pilot", 'code_rate', 'guard', 'spec',
                                    'level'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_67_synchronisation_varying_echo_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[4]:
            if count == 0:
                list_required_data.append([i[0], i[3], j[0], j[1], j[2], j[3], j[4], j[6], j[7], j[8]])
            else:
                list_required_data.append(['', '', j[0], j[1], j[2], j[3], j[4], j[6], j[7], j[8]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['frequency', 'bandwidth', 'fft_mode', 'modulation', "pilot", 'code_rate', 'guard',
                                    'spec', 'delay',
                                    'noise_cn'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_68_performance_in_SFN_echo_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[10]:
            if count == 0:
                list_required_data.append(
                    [i[0], i[3], i[4], i[5], i[6], i[7], i[8], i[9], j[0], j[1], j[2], j[3], j[4], j[5], j[6]])
            else:
                list_required_data.append(["", "", "", "", "", "", "", "", j[0], j[1], j[2], j[3], j[4], j[5], j[6]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['frequency', 'bandwidth', 'fft_mode', 'modulation', "pilot", 'code_rate', 'guard',
                                    'spec', 'mian_att', 'mian_delay', 'pre_att', 'pre_delay', 'post_att', 'post_delay',
                                    'noise_cn'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_69_performance_in_SFN_inside_guard_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        for j in i[10]:
            count_j = 0
            for k in j[3]:
                if k[1] == "NO NEED TEST":
                    continue
                if count_j == 0:
                    list_required_data.append([i[0], i[3], i[4], i[5], i[6], i[7], i[8], i[9], j[0], j[1], j[2], k[0], k[1]])
                else:
                    list_required_data.append(['', '', '', '', '', '', '', '', j[0], j[1], j[2], k[0], k[1]])
                count_j = count_j + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['frequency', 'bandwidth', 'fft_size', 'modulation', "pilot", 'code_rate', 'guard', 'spec',
                                    'mian_att', 'mian_delay', 'pre_delay', 'pre_att', 'noise_cn'])
    pd_data.to_csv(csv_path, index=None)


def dvbt2_69_performance_in_SFN_inside_guard_json_class_test(json_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    for i in list_data:
        for j in i[10]:
            for k in j[3]:
                if k[0] in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] and j[2] in [256, -256] and \
                        i[5] == "T256" and i[6] == "PP2" and i[7] == "R3_4" and i[8] == "G1_8" and i[3] == 7:
                    continue

                if k[0] in [1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20] and j[2] in [1.95, 28, 90, 150, 190.0, 220.0,
                                                                                           -1.95, -28, -90, -150, -190.0, -220.0,
                                                                                           25, 50, 266.0, -25, -50, -266.0,
                                                                                           70, 320, 400.0, 448.0, -70, -320, -400.0, -448.0,
                                                                                           128, 256, 304, -128, -256, -304,
                                                                                           320, 416.0, 500, -320, -416.0, -500]:
                    k[1] = "NO NEED TEST"
    write_json_file(json_path, load_dict)


def dvbt2_70_performance_in_frequency_outside_json_to_csv(json_path, csv_path):
    """
    json to csv
    :param json_path:
    :param csv_path:
    :return:
    """
    load_dict = read_json_file(json_path)
    list_data = load_dict.get("test_parame_result")
    list_required_data = []
    for i in list_data:
        count = 0
        for j in i[9]:
            if count == 0:
                list_required_data.append([i[0], i[3], i[4], i[5], i[6], i[7], i[8], j[0], j[1], j[2], j[3]])
            else:
                list_required_data.append(['', '', '', '', '', '', '', j[0], j[1], j[2], j[3]])
            count = count + 1
    pd_data = pd.DataFrame(list_required_data,
                           columns=['frequency', 'bandwidth', 'fft_size', 'modulation', "pilot", 'code_rate', 'guard',
                                    'mian_att', 'mian_delay', 'pre_delay', 'pre_att'])
    pd_data.to_csv(csv_path, index=None)


if __name__ == '__main__':
    # result = find_level_offset_by_frequency("DVBS_S2_FREQUENCY_LEVEL_OFFSET", 1310)
    SYMBOL_TATE_LIST = generate_symbol_rate_list()
    print (SYMBOL_TATE_LIST)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import json


def set_dvbs_variable_parameter(specan, code_rate, modulation, symbol_rate, frequency, input_signal_level):
    specan.set_digitaltv_coding_constellation(modulation)
    specan.set_digitaltv_coding_coderate(code_rate)
    specan.set_digitaltv_coding_symbolrate(symbol_rate)
    specan.set_frequency_frequency_frequency(frequency)
    specan.set_level_level_level(input_signal_level)


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


def find_level_offset_by_frequency(frequency_offset_type, frequency):
    pass


def write_test_result(file_path, content):
    with open(file_path, "a") as f:
        f.write(content)


def read_ekt_config_data(file_path):
    with open(file_path, 'r') as f:
        dict_data = json.load(f, "utf-8")
        return dict_data

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import visa
import pyvisa
import logging
import time

# import VISAresourceExtentions

logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename='../ekt_log/sfe.log',
                    filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )


class Ektsfe(object):
    """
        SFE接口
    """

    def __init__(self, sfu_ip):
        rm = pyvisa.ResourceManager()
        specan = rm.open_resource('TCPIP::{}::INSTR'.format(sfu_ip))
        self.specan = specan
        del self.specan.timeout

    def set_frequency_frequency_frequency(self, frequency):
        """
         Setting the channel.
         example : Remote control command:
            FREQ 100 MHz
            FREQ:CW 100 MHz
            FREQ:ACT 100 MHz
        :return:
        """
        # self.specan.write('FREQ {}'.format(frequency))
        self.specan.write('FREQ:CW {}'.format(frequency))
        logging.info('FREQ:CW {}'.format(frequency))
        time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_frequency_frequency_channel(self, channel):
        """
         Setting the channel.  Channels can be selected in the range of  1 ... 100
         example : FREQ:CHAN 5
        :return:
        """
        self.specan.write('FREQ:CHAN {}'.format(channel))
        logging.info('FREQ:CHAN {}'.format(channel))
        time.sleep(1)
        del self.specan

    def set_frequency_settings_knobstepstate(self, state_type):
        """
         Activates a user-defined step size for varying the frequency value with the rotary knob.
         Not debugging through

          INCREMENT
          DECIMAL
         example : FREQ:STEP:MODE DEC|INCR
        :return:
        """
        self.specan.write('FREQ:STEP:MODE {}'.format(state_type))
        logging.info('FREQ:STEP:MODE {}'.format(state_type))
        time.sleep(1)
        del self.specan

    def set_frequency_settings_increment(self, frequency):
        """
         Activates a user-defined step size for varying the frequency value with the rotary knob.
         Not debugging through

          INCREMENT
          DECIMAL
         example : FREQ:STEP 50 kHz
        :return:
        """
        # self.specan.write('FREQ:STEP {}'.format(frequency))
        self.specan.write('FREQ:STEP 50 kHz')
        logging.info('FREQ:STEP 50 kHz')
        time.sleep(1)
        del self.specan

    def set_frequency_settings_channel(self, channel_num, frequency):
        """
         Sets the frequency of a channel.
        example : FREQ:CHAN:TAB:FREQ 5, 474 MHz
        :return:
        """
        self.specan.write('FREQ:CHAN:TABL:FREQ {}, {} MHz'.format(channel_num, frequency))
        logging.info('FREQ:CHAN:TABL:FREQ {}, {} MHz'.format(channel_num, frequency))
        time.sleep(1)
        del self.specan

    def set_level_level_level(self, level):
        """
         Sets the RF level of the RF output jack.
        example :POW -30 dBm
            POW:LEV -30 dBm
            POW:AMPL -30 dBm
            POW:IMM -30 dBm
        :return:
        """
        self.specan.write('POW:LEV {}'.format(level))
        logging.info('POW:LEV {}'.format(level))
        time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_level_level_rf(self, rf_type):
        """
         Switches the RF output on and off.
            OFF
            ON
        example :
            OUTP ON|OFF
            OUTP:STAT ON|OFF
        :return:
        """
        self.specan.write('OUTP {}'.format(rf_type))
        logging.info('OUTP {}'.format(rf_type))
        time.sleep(1)
        del self.specan

    def set_level_level_userlimit(self, limit_level):
        """
         Sets a user limit for the level.
        example :
            POW:LIM 30 dBm
            POW:LIM:AMPL 30 dBm
        :return:
        """
        self.specan.write('POW:LIM {}'.format(limit_level))
        logging.info('POW:LIM {}'.format(limit_level))
        time.sleep(1)
        del self.specan

    def set_level_level_mode(self, level_mode):
        """
         ATTENUATOR MODE is used to determine the mode of the attenuator. In the basic configuration of the R&S SFE,
         there are two possible choices: AUTO and FIXED.
             AUTO
             FIXED
        example :
            OUTP:AMOD AUTO|FIX
        :return:
        """
        self.specan.write('OUTP:AMOD {}'.format(level_mode))
        logging.info('OUTP:AMOD {}'.format(level_mode))
        time.sleep(1)
        del self.specan

    def set_level_settings_state(self, state_type):
        """
         Activates a user-defined step size for varying the level with the rotary knob.
            INCREMENT
            DECIMAL
        example :
            POW:STEP:MODE DEC|INCR
        :return:
        """
        self.specan.write('POW:STEP:MODE {}'.format(state_type))
        logging.info('POW:STEP:MODE {}'.format(state_type))
        time.sleep(1)
        del self.specan

    def set_level_settings_increment(self, state_type):
        """
         Sets a user-defined step size. This step size is used for entering the level with the rotary knob or the
         CURSOR UP and CURSOR DOWN keys. To enable variation of the level with this step size,
         it has to be activated with KNOB STEP STATE by switching to INCREMENT there.
        example :
            POW:STEP 1.5
        :return:
        """
        self.specan.write('POW:STEP {}'.format(state_type))
        logging.info('POW:STEP {}'.format(state_type))
        time.sleep(1)
        del self.specan

    def set_level_settings_unit(self, level_unit):
        """
         The units dBm, dBuV, dBmV and mV can be used as level

        example :
            UNIT:VOLT DBM|DBUV|DBMV|MV
        :return:
        """
        self.specan.write('UNIT:VOLT {}'.format(level_unit))
        logging.info('UNIT:VOLT {}'.format(level_unit))
        time.sleep(1)
        del self.specan

    def set_modulation_modulation_modulation(self, modulation_type):
        """
        ON  With modulation ON, all of the settings that concern the modulation (modulation menu, coding and noise) are accepted.
        When modulation is switched OFF, these settings are retained and they are restored when modulation is set back to ON.
        OFF With modulation OFF, a continuous wave (CW) carrier is output with the set frequency and level, and MOD OFF is displayed.
        example :
            MOD ON|OFF
            MOD:STAT ON|OFF
        :return:
        """
        self.specan.write('MOD {}'.format(modulation_type))
        logging.info('MOD {}'.format(modulation_type))
        time.sleep(1)
        del self.specan

    def set_modulation_modulation_source(self, source_type):
        """
        Selection of the signal source. The choices depend on the model and the available options.
        example :
            DM:SOUR DIGital
            DM:SOUR DTV
        :return:
        """
        self.specan.write('DM:SOUR {}'.format(source_type))
        logging.info('DM:SOUR {}'.format(source_type))
        time.sleep(1)
        del self.specan

    def set_modulation_modulation_spectrum(self, standard_type):
        """
        Using INVERTED, you can invert the output signal, i.e. the I and Q signals are exchanged.
        example :
            DM:POL INV|NORM
        :return:
        """
        self.specan.write('DM:POL {}'.format(standard_type))
        logging.info('DM:POL {}'.format(standard_type))
        time.sleep(1)
        del self.specan

    def set_digitaltv_input_source(self, source_type):
        """
        Selection SOURCE
        EXTERNAL
        TS PLAYER (option)
        TEST SIGNAL
        example :
            DVBS:SOUR EXT|TSPL|TEST
        :return:
        """
        self.specan.write('DVBS:SOUR {}'.format(source_type))
        logging.info('DVBS:SOUR {}'.format(source_type))
        time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_input_load(self, file_path):
        """
        Clicking this menu item opens a file dialog box in which you can select the desired player file.
        example :
            TSGEN:CONF:PLAY "D:\TSGEN\SDTV\DVB_25Hz\720_576i\LIVE\DIVER.GTS"
        :return:
        """
        self.specan.write(r'TSGEN:CONF:PLAY "{}"'.format(file_path))
        logging.info(r'TSGEN:CONF:PLAY "{}"'.format(file_path))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_input_stuffing(self, source_type):
        """
        If EXTERNAL is selected as the SOURCE, you can enable stuffing.
        example :
            DVBS:STUF ON|OFF
        :return:
        """
        self.specan.write('DVBS:STUF {}'.format(source_type))
        logging.info('DVBS:STUF {}'.format(source_type))
        time.sleep(1)
        del self.specan

    def set_digitaltv_coding_symbolrate(self, symbol_rate):
        """
        The symbol rate is between 0.1 MS/s and 45 MS/s with a resolution of 1 Hz. In the transmission spectrum, the symbol rate represents the 3 dB bandwidth.
        example :
            DVBS:SYMB 0.100000e6 ... 45.000000e6
        :return:
        """
        self.specan.write('DVBS:SYMB {}'.format(symbol_rate))
        logging.info('DVBS:SYMB {}'.format(symbol_rate))
        time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_constellation(self, constellation_type):
        """
        You can select QPSK, 8 PSK or 16 QAM as the constellation.
        example :
            DVBS:CONS S4|S8|S16
        :return:
        """
        self.specan.write('DVBS:CONS {}'.format(constellation_type))
        logging.info('DVBS:CONS {}'.format(constellation_type))
        time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_rolloff(self, rolloff_num):
        """
        The output signals are shaped as pulses by a FIR filter, yielding a root raised cosine characteristic. You can select 0.25 or 0.35 as the roll-off alpha factor.
        example :
            DVBS:ROLL 0.25|0.35
        :return:
        """
        self.specan.write('DVBS:ROLL {}'.format(rolloff_num))
        logging.info('DVBS:ROLL {}'.format(rolloff_num))
        time.sleep(1)
        del self.specan

    def set_digitaltv_coding_coderate(self, code_rate):
        """
        The constellation type determines the available code rates.

        Constellation     Available code rate
        QPSK              1/2, 2/3, 3/4, 5/6, 7/8
        8 PSK             2/3, 5/6, 8/9
        16 QAM            3/4, 7/8

        example :
            DVBS:RATE R1_2|R2_3|R3_4|R5_6|R7_8|R8_9
        :return:
        """
        self.specan.write('DVBS:RATE {}'.format(code_rate))
        logging.info('DVBS:RATE {}'.format(code_rate))
        time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_special_special(self, special_type):
        """
        ON/OFF toggle function.
            ON
            OFF
        example :
            DVBS:SETT ON
        :return:
        """
        self.specan.write('DVBS:SETT {}'.format(special_type))
        logging.info('DVBS:SETT {}'.format(special_type))
        time.sleep(1)
        del self.specan

    def set_digitaltv_settings_testtspacket(self, packet_type):
        """
        Selects the mode of the test TS packet.
            H184        Head / 184 payload
            S187        Sync / 187 payload
        example :
            DVBS:TSP S187
        :return:
        """
        self.specan.write('DVBS:TSP {}'.format(packet_type))
        logging.info('DVBS:TSP {}'.format(packet_type))
        time.sleep(1)
        del self.specan

    def set_digitaltv_settings_prbs(self, prbs_type):
        """
        Selects the mode of the PRBS.
            P23_1       2^23 - 1 (ITU-T O.151)
            P15_1       2^15 - 1 (ITU-T O.151)
        example :
            DVBS:PRBS P15_1
        :return:
        """
        self.specan.write('DVBS:PRBS {}'.format(prbs_type))
        logging.info('DVBS:PRBS {}'.format(prbs_type))
        time.sleep(1)
        del self.specan

    def preset_instrument(self):
        """
        Triggers a reset. The command has the same effect as pressing the PRESET key on the front panel
        example :
            SYST:PRES
        :return:
        """
        self.specan.write('SYST:PRES')
        logging.info(r'SYST:PRES')
        time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def query_opc(self):
        """
        """
        # self.specan.write('*OPC?')
        self.specan.query('*OPC?')
        time.sleep(1)
        del self.specan

    def clean_reset(self):
        """
        """
        self.specan.write('*RST;*CLS')
        time.sleep(1)
        # self.specan.close()
        del self.specan

    def set_cmd(self):
        """
        The constellation type determines the available code rates.

        Constellation     Available code rate
        QPSK              1/2, 2/3, 3/4, 5/6, 7/8
        8 PSK             2/3, 5/6, 8/9
        16 QAM            3/4, 7/8

        example :
            DVBS:RATE R1_2|R2_3|R3_4|R5_6|R7_8|R8_9
        :return:
        """
        # self.specan.write('*RST;*CLS')
        self.specan.timeout = 2000
        # self.specan.ext_error_checking()
        # self.specan.query('*OPC?')

    # def __del__(self):
    #     del self.specan


def _test_code():
    sfu_ip = "192.168.1.47"
    # sfu_ip = "192.168.1.50"
    # host = '127.0.0.1'
    # port = 8900
    specan = Ektsfe(sfu_ip)
    specan.set_frequency_frequency_frequency("101.001 MHz")
    # specan.set_frequency_frequency_channel("4")
    # specan.set_frequency_settings_knobstepstate("DEC")
    # specan.set_frequency_settings_increment("50 kHz")
    # specan.set_frequency_settings_channel("5", "474")
    # specan.set_level_level_level("-31 dBm")
    # specan.set_level_level_rf("OFF")
    # specan.set_level_level_userlimit("20 dBm")
    # specan.set_level_level_mode("AUTO")
    # specan.set_level_settings_unit("DBUV")
    # specan.set_modulation_modulation_modulation("ON")
    # specan.set_modulation_modulation_source("DTV")
    # specan.set_modulation_modulation_spectrum("NORM")
    # specan.set_digitaltv_input_source("EXT")
    # specan.set_digitaltv_input_stuffing("ON")
    # specan.set_digitaltv_coding_symbolrate("0.100000e6")
    # specan.set_digitaltv_coding_constellation("S8")
    # specan.set_digitaltv_coding_rolloff("0.25")
    # specan.set_digitaltv_coding_coderate("R8_9")
    # specan.set_digitaltv_input_load(r"D:\TSGEN\SDTV\DVB_25Hz\720_576i\LIVE\FACT_4M.GTS")
    # specan.preset_instrument()
    # specan.set_digitaltv_special_special("OFF")
    # specan.set_digitaltv_settings_testtspacket("H184")
    # specan.set_digitaltv_settings_prbs("P23_1")
    # specan.set_level_settings_state("DEC")
    # specan.set_level_settings_increment("2.5")
    # specan.set_cmd()
    # specan.clean_reset()
    # specan.set_digitaltv_input_load(r"D:\TSGEN\SDTV\DVB_25Hz\720_576i\LIVE\DIVER.GTS")
    # specan.query_opc()


if __name__ == '__main__':
    _test_code()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import visa
import pyvisa
import logging
import time


# import VISAresourceExtentions

logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename='sfe.log',
                    filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )

class Ektsfe(object):
    """

    """

    def __init__(self, net):
        rm = pyvisa.ResourceManager()
        specan = rm.open_resource('TCPIP::{}::INSTR'.format(net))
        self.specan = specan

    def query_instrument(self):
        """
         Query the Identification string
        :return:
        """
        print self.specan.query('*IDN?')

    def set_channel_output_frequency(self, channel_num, frequency):
        """
         Sets the frequency of a channel.
        :return:
        """
        self.specan.write('FREQ:CHAN:TABL:FREQ {}, {} MHz'.format(channel_num, frequency))

    def set_current_channel(self, channel_num):
        """
         Sets the channel of the RF output frequency
        :return:
        """
        self.specan.write('FREQ:CHAN {}'.format(channel_num))

    def query_bit_er_rate(self):
        """
         Sets the channel of the RF output frequency
        :return:
        """
        res = self.specan.write('READ:BER?')
        print res
        return res

    def query_power(self):
        """
         Sets the channel of the RF output frequency
        :return:
        """
        res = self.specan.write('READ?')
        print res
        return res

    def set_attenuation_signal(self):
        """
         Sets the channel of the RF output frequency
        :return:
        """
        self.specan.write('DM:IATT 44 dB')

    def set_absolute_level(self):
        """
         Sets the channel of the RF output frequency
        :return:
        """
        self.specan.write('DM:ILEV -10')

    def set_frequency_offset(self):
        """
         Sets the frequency offset of any add-on unit
        :return:
        """
        self.specan.write('FREQ:OFFS 000kHz')

    def set_coder_output_symbol_rate(self, symbol_rate):
        """
         Sets the coder output symbol rate
         Example:
         DVBS2:SYMB 31.711e6
         Sets the symbol rate to 31.711 MS/s.
        :return:
        """
        self.specan.write('DVBS2:SYMB {}'.format(symbol_rate))

    def set_dvbs2_modulation_mode(self, modulation_mode):
        """
         Sets the modulation mode (constellation) of the DVB-S2 signal.
         S4 : QPSK
         S8 : 8PSK
         A16 : 16APSK
         A32 : 32APSK
         example : DVBS2:CONS S8
        :return:
        """
        self.specan.write('DVBS2:CONS {}'.format(modulation_mode))

    def set_fec_frame_type(self, tyoe_fec):
        """
         Selects the type of FEC frame.
         "NORMAL"
            64800 bit
         "SHORT"
            16200 bit
         example : DVBS2:FECF NORM
        :return:
        """
        self.specan.write('DVBS2:FECF {}'.format(tyoe_fec))

    def set_switch_output_symbol(self, switch_pilot):
        """
         Switches pilot generation in the output symbols of the coder on or off.
         ON
         OFF
         example : DVBS2:PIL OFF
        :return:
        """
        self.specan.write('DVBS2:PIL {}'.format(switch_pilot))

    def set_coder_output_sysbol_filter(self, symbol_filter):
        """
         Determines the pulse shaping of the coder output symbol filter.
            0.15
            0.20
            0.25
            0.35
         example : DVBS2:ROLL 0.25
        :return:
        """
        self.specan.write('DVBS2:ROLL {}'.format(symbol_filter))

    def set_code_rate(self, code_rate):
        """
         Selects the puncturing (code rate) of the inner error protection block.
            R1_4
            R1_3
            R2_5
            R1_2
            R3_5
            R2_3
            R3_4
            R4_5
            R5_6
            R6_7
            R7_8
            R8_9
            R9_10
         example : DVBS2:RATE R8_9
        :return:
        """
        self.specan.write('DVBS2:RATE {}'.format(code_rate))

    def set_frequency_frequency_frequency(self, frequency):
        """

        Range: 300 kHz  to  3 GHz
        Increment: 0.01 Hz
        *RST:1000 MHz
        Default unit: Hz
        example : Remote control command:
            FREQ 100 MHz
            FREQ:CW 100 MHz
            FREQ:ACT 100 MHz
        :return:
        """
        # self.specan.write('FREQ {}'.format(frequency))
        self.specan.write('FREQ:CW {}'.format(frequency))

    def set_frequency_frequency_offset(self, frequency):
        """
        Sets the frequency offset of any add-on unit
        Range: -50 GHz  to  +50 GHz
        Increment: 0.01 Hz
        *RST:0 Hz
        Default unit: Hz
        example : Remote control command:
            FREQ:OFFS 500kHz
        :return:
        """
        # self.specan.write('FREQ {}'.format(frequency))
        self.specan.write('FREQ:OFFS {}'.format(frequency))

    def set_frequency_frequency_channel(self, channel):
        """
         Setting the channel.  Channels can be selected in the range of  1 ... 100
         example : FREQ:CHAN 5
        :return:
        """
        self.specan.write('FREQ:CHAN {}'.format(channel))

    def set_frequency_sweep_start(self, frequency):
        """
        Sets the start frequency.
        Range: 300 kHz  to  3 GHz
        Increment: 0.01 Hz
        *RST:100 MHz
        Default unit: Hz
         example : SWE:STARt 1 MHz
        :return:
        """
        self.specan.write('SWE:STARt {}'.format(frequency))

    def set_frequency_sweep_stop(self, frequency):
        """
        Sets the stop frequency for the sweep
        Increment: 0.01 Hz
        *RST:500 MHz
        Default unit: Hz
         example : SWE:STOP 2 GHz
        :return:
        """
        self.specan.write('SWE:STOP {}'.format(frequency))

    def set_frequency_sweep_center(self, frequency):
        """
        Sets the center frequency. The displayed values for the start and stop frequency will change accordingly.
        Range: 300e3  to  3e9 Hz
        Increment: 0.01 Hz
        *RST:300e6 Hz
        Default unit: Hz
         example : SWE:CENT 400 MHz
        :return:
        """
        self.specan.write('SWE:CENT {}'.format(frequency))

    def set_frequency_sweep_span(self, frequency):
        """
        The displayed values for the start and stop frequency will change accordingly..
        Range: 0  to  3 GHz
        Increment: 0.01 Hz
        *RST:400 MHz
        Default unit: Hz
         example : SWE:SPAN 200 MHz
        :return:
        """
        self.specan.write('SWE:SPAN {}'.format(frequency))

    def set_frequency_sweep_spacing(self, span_type):
        """
        Sets the type of progressive step size during the sweep.
        LINear     LOGarithmic
         example : SWE:SPAC LIN
        :return:
        """
        self.specan.write('SWE:SPAC {}'.format(span_type))

    def set_frequency_sweep_step(self, step_frequency):
        """
        Sets the step for a linear sweep.
        Increment: 0.1 Hz
        *RST:1 MHz
        Default unit: Hz
         example : SWE:STEP 2 MHz
        :return:
        """
        self.specan.write('SWE:STEP {}'.format(step_frequency))

    def set_frequency_sweep_dwell(self, dewll_time):
        """
        Sets the dwell time per frequency step of the sweep.
        Range: 10  to  10000 ms
        Increment: 0.1 ms
        *RST:25 ms
        Default unit: s
         example : SWE:DWEL 100 ms
        :return:
        """
        self.specan.write('SWE:DWEL {}'.format(dewll_time))

    def set_frequency_sweep_mode(self, mode_type):
        """
        not complate

        Sets the sweep mode
        AUTO
        MANual
        STEP
         example : SWE:MODE AUTO
        :return:
        """
        self.specan.write('SWE:MODE AUTO'.format(mode_type))
        # self.specan.write('SWE:MODE STEP')

    def set_frequency_sweep_state(self, state_type):
        """
        Determines the mode of the R&S SFU and also by what commands the output frequency is determined.

        CW|FIXed
        SWEep
         example : FREQ:MODE SWE
        :return:
        """
        self.specan.write('FREQ:MODE {}'.format(state_type))

    def set_frequency_sweep_reset(self):
        """
        Resets an active frequency sweep to the start frequency
         example : :SWE:RES
        :return:
        """
        self.specan.write(':SWE:RES')


    def set_level_level_level(self, level_unit,level_num):
        """
         Sets the RF output level in CW mode.
            Increment: 0.01 dB
            *RST:-99.9 dBm
            Default unit: dBm
        example :
            UNIT:VOLT dBm
            POW 15
        :return:
        """
        self.specan.write('UNIT:VOLT {}'.format(level_unit))
        self.specan.write('POW {}'.format(level_num))

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

    def set_level_level_offset(self, offset):
        """
         Sets the constant level offset of a follow-up attenuator/amplifie
            Increment: 0.01 dB
            *RST:0 dB
            Default unit: dB
        example :
            POW:OFFS 10
        :return:
        """
        self.specan.write('POW:OFFS {}'.format(offset))

    def set_level_level_userlimit(self, limit_level):
        """
        Limits the maximum RF output level in CW and sweep mode
            Increment: 0.01 dB
            *RST:+20 dBm
            Default unit: dBm
        example :
            PPOW:LIM 10
        :return:
        """
        self.specan.write('POW:LIM {}'.format(limit_level))

    def set_level_level_mode(self, level_mode):
        """
         Sets the mode of the attenuator on the RF output.
         there are two possible choices: AUTO and FIXED.
             AUTO
             FIXed
             NORMal
             HPOWer
        example :
            OUTP:AMOD FIX
        :return:
        """
        self.specan.write('OUTP:AMOD {}'.format(level_mode))

    def set_level_alc_state(self, state_type):
        """
         Switches the automatic level control on or off.
            ON         Internal level control is permanently activated.
            OFF        Internal level control is switched off.
            AUTO       Depending on operating status, internal level control is automatically switched on or off.
        example :
            POW:ALC ON
        :return:
        """
        self.specan.write('POW:ALC {}'.format(state_type))

    def set_level_settings_unit(self, level_unit):
        """
         Sets the units for power. It affects all commands that set power values.
         It has no effect on manual control and screen displays.
            DBM
            DBUV
            DBMV
            MV
        example :
            UNIT:VOLT DBM|DBUV|DBMV|MV
        :return:
        """
        self.specan.write('UNIT:VOLT {}'.format(level_unit))

    def set_modulation_modulation_modulation(self, modulation_type):
        """
        Switches the modulator on or off.
            ON        The modulated RF signal appears is output.
            OFF       A CW signal is output.
        example :
            MOD ON|OFF
        :return:
        """
        self.specan.write('MOD {}'.format(modulation_type))

    def set_modulation_modulation_source(self, source_type):
        """
        Selects the data source for the modulator or queries its setting.
            INTern
            ARB
            DIGital
            ANALog
            DIRect
            ATV
            DTV
            AUDio
        example :
            DM:SOUR DTV
        :return:
        """
        self.specan.write('DM:SOUR {}'.format(source_type))

    def set_modulation_modulation_standard_atv(self, standard_type):
        """
        Sets the analog transmission standard or queries its setting
        The multi ATV predefined option
            BGPR        B/G PREDEF.
            BGNPr       B/G N PREDEF.
            DKPR        D/K PREDEF.
            D1PR        D1 PREDEF.
            DCPR        D CHINA PREDEF.
            IPR         I PREDEF.
            I1PR        I1 PREDEF.
            MNPR        M/N PREDEF.
            LPR         L PREDEF.
            BGRE        B/G standard
            DKRE        D/K standard
            IRE         I standard
            MNRE        M/N standard
            LRE         L standard
        example :
            DM:ATV BGRE
        :return:
        """
        self.specan.write('DM:ATV {}'.format(standard_type))



def __del__(self):
    del self.specan


def _test_code():
    # net = "192.168.1.47"
    net = "192.168.1.50"
    # host = '127.0.0.1'
    # port = 8900
    specan = Ektsfe(net)
    # specan.set_channel_output_frequency("3", "555")
    # specan.set_current_channel("3")

    # specan.set_coder_output_symbol_rate("31.711e6")
    # specan.set_dvbs2_modulation_mode("S8")
    # specan.set_fec_frame_type("NORM")
    # specan.set_switch_output_symbol("OFF")
    # specan.set_code_rate("R2_3")
    # specan.set_coder_output_sysbol_filter("0.25")
    # specan.set_frequency_frequency_frequency("101 MHz")
    # specan.set_frequency_frequency_offset("500kHz")
    # specan.set_frequency_frequency_channel("4")
    # specan.set_frequency_sweep_start("1 MHz")
    # specan.set_frequency_sweep_stop("1 GHz")
    # specan.set_frequency_sweep_center("400 MHz")
    # specan.set_frequency_sweep_span("200 MHz")
    # specan.set_frequency_sweep_spacing("LOG")
    # specan.set_frequency_sweep_step("2 MHz")
    # specan.set_frequency_sweep_dwell("500 ms")
    # specan.set_frequency_sweep_mode("AUTO")
    # specan.set_frequency_sweep_state("CW")
    # specan.set_frequency_sweep_reset()
    # specan.set_level_level_level("dBm", 15)
    # specan.set_level_level_rf("OFF")
    # specan.set_level_level_userlimit("10")
    # specan.set_level_level_mode("FIX")
    # specan.set_level_settings_unit("DBM")
    # specan.set_level_alc_state("ON")
    # specan.set_modulation_modulation_modulation("ON")
    # specan.set_modulation_modulation_source("ATV")
    # specan.set_modulation_modulation_standard_atv("LPR")
    specan.set_cmd()


if __name__ == '__main__':
    _test_code()

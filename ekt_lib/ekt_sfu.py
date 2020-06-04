#!/usr/bin/env python
# -*- coding: utf-8 -*-
import visa
import pyvisa
import logging
import time
import os

# import VISAresourceExtentions

current_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename='{}/ekt_log/sfu.log'.format(current_path),
                    filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )


class Ektsfu(object):
    """

    """

    def __init__(self, sfu_ip):
        while True:
            try:
                rm = pyvisa.ResourceManager()
                specan = rm.open_resource('TCPIP::{}::INSTR'.format(sfu_ip))
                self.specan = specan
                del self.specan.timeout
                break
            except:
                print("SFU连接出错")
                logging.info('SFU连接出错')
                time.sleep(60)

    def set_frequency_frequency_frequency(self, frequency):
        """
        Sets the RF output frequency
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
        logging.info('FREQ:CW {}'.format(frequency))
        # time.sleep(2)
        self.specan.query('*OPC?')
        del self.specan

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
        self.specan.write('FREQ:OFFS {}'.format(frequency))
        logging.info('FREQ:OFFS {}'.format(frequency))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_frequency_frequency_channel(self, channel):
        """
         Setting the channel.  Channels can be selected in the range of  1 ... 100
         example :
            FREQ:CHAN 5
        :return:
        """
        self.specan.write('FREQ:CHAN {}'.format(channel))
        logging.info('FREQ:CHAN {}'.format(channel))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_frequency_sweep_start(self, frequency):
        """
        Sets the start frequency.
            Range: 300 kHz  to  3 GHz
            Increment: 0.01 Hz
            *RST:100 MHz
            Default unit: Hz
         example :
            SWE:STARt 1 MHz
        :return:
        """
        self.specan.write('SWE:STARt {}'.format(frequency))
        logging.info('SWE:STARt {}'.format(frequency))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_frequency_sweep_stop(self, frequency):
        """
        Sets the stop frequency for the sweep
            Increment: 0.01 Hz
            *RST:500 MHz
            Default unit: Hz
         example :
            SWE:STOP 2 GHz
        :return:
        """
        self.specan.write('SWE:STOP {}'.format(frequency))
        logging.info('SWE:STOP {}'.format(frequency))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_frequency_sweep_center(self, frequency):
        """
        Sets the center frequency. The displayed values for the start and stop frequency will change accordingly.
            Range: 300e3  to  3e9 Hz
            Increment: 0.01 Hz
            *RST:300e6 Hz
            Default unit: Hz
         example :
            SWE:CENT 400 MHz
        :return:
        """
        self.specan.write('SWE:CENT {}'.format(frequency))
        logging.info('SWE:CENT {}'.format(frequency))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_frequency_sweep_span(self, frequency):
        """
        The displayed values for the start and stop frequency will change accordingly..
            Range: 0  to  3 GHz
            Increment: 0.01 Hz
            *RST:400 MHz
            Default unit: Hz
         example :
            SWE:SPAN 200 MHz
        :return:
        """
        self.specan.write('SWE:SPAN {}'.format(frequency))
        logging.info('SWE:SPAN {}'.format(frequency))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_frequency_sweep_spacing(self, span_type):
        """
        Sets the type of progressive step size during the sweep.
            LINear
            LOGarithmic
         example :
            SWE:SPAC LIN
        :return:
        """
        self.specan.write('SWE:SPAC {}'.format(span_type))
        logging.info('SWE:SPAC {}'.format(span_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_frequency_sweep_step(self, step_frequency):
        """
        Sets the step for a linear sweep.
            Increment: 0.1 Hz
            *RST:1 MHz
            Default unit: Hz
         example :
            SWE:STEP 2 MHz
        :return:
        """
        self.specan.write('SWE:STEP {}'.format(step_frequency))
        logging.info('SWE:STEP {}'.format(step_frequency))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_frequency_sweep_dwell(self, dewll_time):
        """
        Sets the dwell time per frequency step of the sweep.
            Range: 10  to  10000 ms
            Increment: 0.1 ms
            *RST:25 ms
            Default unit: s
         example :
            SWE:DWEL 100 ms
        :return:
        """
        self.specan.write('SWE:DWEL {}'.format(dewll_time))
        logging.info('SWE:DWEL {}'.format(dewll_time))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_frequency_sweep_mode(self, mode_type):
        """
        not complate

        Sets the sweep mode
            AUTO
            MANual
            STEP
         example :
            SWE:MODE AUTO
        :return:
        """
        self.specan.write('SWE:MODE AUTO'.format(mode_type))
        logging.info('SWE:MODE AUTO'.format(mode_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan
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
        logging.info('FREQ:MODE {}'.format(state_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_frequency_sweep_reset(self):
        """
        Resets an active frequency sweep to the start frequency
         example : :SWE:RES
        :return:
        """
        self.specan.write(':SWE:RES')
        logging.info(':SWE:RES')
        # time.sleep(1)
        self.specan.query('*OPC?')
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
        # time.sleep(1)
        self.specan.query('*OPC?')
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
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_frequency_settings_channlfrequency(self, channel_name, channel_frequency):
        """
        Sets the frequency of a channel.
            Selects the channel.
                Range:      0  to  100
            Frequency of the selected channel.
                Range:      300 kHz  to  3 GHz
                Default unit:       Hz
         example :
            FREQ:CHAN:TABL:FREQ 5, 400 MHz
        :return:
        """
        self.specan.write('FREQ:CHAN:TABL:FREQ {}, {}'.format(channel_name, channel_frequency))
        logging.info('FREQ:CHAN:TABL:FREQ {}, {}'.format(channel_name, channel_frequency))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_level_level_level(self, level_unit, level_num):
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
        time.sleep(0.1)
        self.specan.write('POW {}'.format(level_num))
        # time.sleep(0.1)
        self.specan.query('*OPC?')
        del self.specan
        logging.info('UNIT:VOLT {}'.format(level_unit))
        logging.info('POW {}'.format(level_num))

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
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

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
        logging.info('POW:OFFS {}'.format(offset))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

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
        logging.info('POW:LIM {}'.format(limit_level))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

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
        logging.info('OUTP:AMOD {}'.format(level_mode))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

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
        logging.info('POW:ALC {}'.format(state_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

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
        logging.info('UNIT:VOLT {}'.format(level_unit))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

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
        logging.info('MOD {}'.format(modulation_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

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
        logging.info('DM:SOUR {}'.format(source_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

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
        logging.info('DM:ATV {}'.format(standard_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_modulation_modulation_standard_dvt(self, standard_type):
        """
        Sets the analog transmission standard or queries its setting
        The multi ATV predefined option
            DVBC
            DVBS
            DVBT
            VSB
            J83B
            ISDBt
            DMBT
            DMBH
            DTMB
            DVS2
            DIRectv
            TDMB
            MEDiaflo
            CMMB
            T2DVb
            ATSM
            C2DVb
        example :
            DM:TRAN DIR
        :return:
        """
        self.specan.write('DM:TRAN {}'.format(standard_type))
        logging.info('DM:TRAN {}'.format(standard_type))
        # time.sleep(3)
        self.specan.query('*OPC?')
        del self.specan

    def set_modulation_modulation_spectrum(self, spectrum_type):
        """
        Selects the polarity of the spectrum or queries its setting. Inverting the spectrum corresponds to
        swapping the I and Q signal.
            NORMal
            INVerted
        example :
            DM:POL INV
        :return:
        """
        self.specan.write('DM:POL {}'.format(spectrum_type))
        logging.info('DM:POL {}'.format(spectrum_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_modulation_settings_level(self, level_type):
        """
        Sets the gain of the I/Q modulator in relation to the analog I/Q signal
            AUTO
            DBM3
            DB0
            DB3
            DB6
        example :
            IQ:GAIN DB0
        :return:
        """
        self.specan.write('IQ:GAIN {}'.format(level_type))
        logging.info('IQ:GAIN {}'.format(level_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_modulation_settings_factor(self, factor_type):
        """
        Sets the crest factor of the external analog signal.
            Range:          0  to  30 dB
            Increment:      0.01 dB
            *RST:           6 dB
            Default unit:   dB
        example :
            IQ:CRES 10
        :return:
        """
        self.specan.write('IQ:CRES {}'.format(factor_type))
        logging.info('IQ:CRES {}'.format(factor_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_modulation_settings_filtering(self, filtering_type):
        """
        Activates the optimized settings for wideband modulation signals (> 10 MHz).
            ON
            OFF
        example :
            IQ:WBST ON
        :return:
        """
        self.specan.write('IQ:WBST {}'.format(filtering_type))
        logging.info('IQ:WBST {}'.format(filtering_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_modulation_settings_mode(self, mode_type):
        """
        Selects the mode of the digital input.
            WBNC        Wideband normal clock
            WBEC        Wideband ext. clock
            DIVN        Diversity / native
            NRWN        Narrow normal
            NWEC        Narrow ext. clock
            AUTO
        example :
            IQ:DINM WBEC
        :return:
        """
        self.specan.write('IQ:DINM {}'.format(mode_type))
        logging.info('IQ:DINM {}'.format(mode_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_modulation_settings_output(self, output_type):
        """
        This instruction selects the place in the signal path, which is made accessible over the DIG I/Q Out output.
            OFF
            AFC         AfterCoder
            AFFA        AfterFading
            AFN         AfterNoise
            AFB         AfterBasebandImpair
            ARB
            DIGital     IqDigitalIn
            ANALog      IqAnalogIn
            AFFB        AfterFadingB
            AUTO
        example :
            IQ:DOUTput AFFA
        :return:
        """
        self.specan.write('IQ:DOUTput {}'.format(output_type))
        logging.info('IQ:DOUTput {}'.format(output_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_input_source_dvbs2(self, source_type):
        """
        Selects the transport stream source for the DVB-S2 coder.
        EXTERNAL
        TS PLAYER (option)
        TEST SIGNAL
        example :
            DVBS2:SOUR EXT|TSPL|TEST
        :return:
        """
        self.specan.write('DVBS2:SOUR {}'.format(source_type))
        logging.info('DVBS2:SOUR {}'.format(source_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_symbolrate_dvbs2(self, symbol_rate):
        """
        Sets the coder output symbol rate
            *RST:       20.000e6 S/s
            Default unit:       S/s
        example :
            DVBS2:SYMB 31.711e6
        :return:
        """
        self.specan.write('DVBS2:SYMB {}'.format(symbol_rate))
        logging.info('DVBS2:SYMB {}'.format(symbol_rate))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_constellation_dvbs2(self, constellation_type):
        """
        Sets the modulation mode (constellation) of the DVB-S2 signal.
            S4      QPSK
            S8      8PSK
            A16     16APSK
            A32     32APSK
        example :
            DVBS2:CONS S8
        :return:
        """
        self.specan.write('DVBS2:CONS {}'.format(constellation_type))
        logging.info('DVBS2:CONS {}'.format(constellation_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_fecframe_dvbs2(self, fecframe_type):
        """
        Sets the length of the FEC frames
            "NORMAL"        64800 bit
            "SHORT"         16200 bit
        example :
            DVBS2:FECF NORM
        :return:
        """
        self.specan.write('DVBS2:FECF {}'.format(fecframe_type))
        logging.info('DVBS2:FECF {}'.format(fecframe_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_pilots_dvbs2(self, fecframe_type):
        """
        Switches pilot generation in the output symbols of the coder on or off.
            ON
            OFF
        example :
            DVBS2:PIL OFF
        :return:
        """
        self.specan.write('DVBS2:PIL {}'.format(fecframe_type))
        logging.info('DVBS2:PIL {}'.format(fecframe_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_rolloff_dvbs2(self, rolloff_num):
        """
       Determines the pulse shaping of the coder output symbol filter
            0.15
            0.20
            0.25
            0.35
        example :
            DVBS2:ROLL 0.25
        :return:
        """
        self.specan.write('DVBS2:ROLL {}'.format(rolloff_num))
        logging.info('DVBS2:ROLL {}'.format(rolloff_num))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_coderate_dvbs2(self, code_rate):
        """
        Selects the puncturing (code rate) of the inner error protection block
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
        example :
            DVBS2:RATE R8_9
        :return:
        """
        self.specan.write('DVBS2:RATE {}'.format(code_rate))
        logging.info('DVBS2:RATE {}'.format(code_rate))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_special_settings_dvbs2(self, setting_type):
        """
        Enables the special settings.
            ON
            OFF
        example :
            DVBS2:SETT ON
        :return:
        """
        self.specan.write('DVBS2:SETT {}'.format(setting_type))
        logging.info('DVBS2:SETT {}'.format(setting_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_phasenoise_phasenoise_dvbs2(self, phasenoise_type):
        """
        Activates the phase noise.
            ON
            OFF
        example :
            DVBS2:PHAS ON
        :return:
        """
        self.specan.write('DVBS2:PHAS {}'.format(phasenoise_type))
        logging.info('DVBS2:PHAS {}'.format(phasenoise_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_phasenoise_shape_dvbs2(self, shape_type):
        """
        Selects the shape of the phase noise.
            SHA1
            SHA2
            SHA3
        example :
            DVBS2:PHAS:SHAP SHA3
        :return:
        """
        self.specan.write('DVBS2:PHAS:SHAP {}'.format(shape_type))
        logging.info('DVBS2:PHAS:SHAP {}'.format(shape_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_phasenoise_magnitude_dvbs2(self, magnitude):
        """
        Selects the phase noise amplitude.
            Range:      0  to  255
            Increment:  1
            *RST:       0
        example :
            DVBS2:PHAS:MAGN 3
        :return:
        """
        self.specan.write('DVBS2:PHAS:MAGN {}'.format(magnitude))
        logging.info('DVBS2:PHAS:MAGN {}'.format(magnitude))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_tspacket_dvbs2(self, tspacket_type):
        """
        Selects the frame structure of the test TS packet.
            H184    Head / 184 payload
            S187    Sync / 187 payload
            H127    With AMC = DIRECTV
            P130    With AMC = DIRECTV
        example :
            DVBS2:TSP S187
        :return:
        """
        self.specan.write('DVBS2:TSP {}'.format(tspacket_type))
        logging.info('DVBS2:TSP {}'.format(tspacket_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_pidpacket_dvbs2(self, pidpacket_type):
        """
        Selects the "packet identifiers" of the test TS packet.
            NULL
            VARiable
        example :
            DVBS2:PIDT VAR
        :return:
        """
        self.specan.write('DVBS2:PIDT {}'.format(pidpacket_type))
        logging.info('DVBS2:PIDT {}'.format(pidpacket_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_pid_dvbs2(self, pid):
        """
        Queries the PID of the test TS packet or sets the PID for PIDtestpack = VAR.
            Range:
            #H0000  to  #H1FFF
        example :
            #H1ABC
        :return:
        """
        self.specan.write('#H{}'.format(pid))
        logging.info('#H{}'.format(pid))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_payloadtest_dvbs2(self, payloadtest_type):
        """
        Selects the payload in the test TS packets or in the null packets with stuffing = ON.
            PRBS
            H00     Hex 00
            HFF     Hex FF
            RAMP        Counter value; 0 to 187
            RMP2        Counter value; n to n+187, n is incremented each TS packet.
        example :
            DVBS2:PAYL HFF
        :return:
        """
        self.specan.write('DVBS2:PAYL {}'.format(payloadtest_type))
        logging.info('DVBS2:PAYL {}'.format(payloadtest_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_prbs_dvbs2(self, prbs_type):
        """
        Selects the type of PRBS in the payload range of the test TS packets if [SOURce][:IQCoder]:DVBS2:PAYLoad[?] = PRBS.
            P23_1        2^23 - 1 (ITU-T O.151)
            P15_1        2^15 - 1 (ITU-T O.151)
        example :
            DVBS2:PRBS P15_1
        :return:
        """
        self.specan.write('DVBS2:PRBS {}'.format(prbs_type))
        logging.info('DVBS2:PRBS {}'.format(prbs_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_interferer_source(self, interferer_type):
        """
        Selects the source of the interference signal.
            OFF
            ATVPr
            ARB
            DIGital
            ANALog
        example :
            DM:ISRC ARB
        :return:
        """
        self.specan.write('DM:ISRC {}'.format(interferer_type))
        logging.info('DM:ISRC {}'.format(interferer_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_interferer_addition(self, addition_type):
        """
        Sets the feed-in point for adding the interference signal.
            OFF
            BEFNoise    Before the noise.
            AFN     After the noise.
        example :
            DM:IADD AFN
        :return:
        """
        self.specan.write('DM:IADD {}'.format(addition_type))
        logging.info('DM:IADD {}'.format(addition_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_interferer_reference(self, reference_type):
        """
        Determines how the level of the interferer signal is set.
            LEV
            ATT
        example :
            DM:IREF ATT
        :return:
        """
        self.specan.write('DM:IREF {}'.format(reference_type))
        logging.info('DM:IREF {}'.format(reference_type))
        self.specan.query('*OPC?')
        del self.specan

    def set_interferer_attenuation(self, attenuation):
        """
        Sets the attenuation of the interference signal.
            Range:         -60  to  +60 dB
            Increment:      0.01 dB
            *RST:           20 dB
            Default unit:   dB
        example :
            DM:IATT 5 dB
        :return:
        """
        self.specan.write('DM:IATT {} dB'.format(attenuation))
        logging.info('DM:IATT {} dB'.format(attenuation))
        self.specan.query('*OPC?')
        del self.specan

    def set_interferer_level(self, level):
        """
        Sets the absolute level of the interferer signal.
            Range:          -70.00 dBm  to  +50.00 dBm
            Increment:      0.01 dBm
            *RST:           -30 dBm
            Default unit:   dBm
        example :
            DM:ILEV -10
        :return:
        """
        self.specan.write('DM:ILEV {}'.format(level))
        logging.info('DM:ILEV {}'.format(level))
        self.specan.query('*OPC?')
        del self.specan

    def set_interferer_frequency_offset(self, frequency):
        """
        Sets the frequency offset of the interferer signal in the baseband.
            Range:        -40.00 MHz  to  +40.00 MHz
            Increment:    0.1 Hz
            *RST:         0 Hz
            Default unit: Hz
        example :
            DM:IFR -1e6 HZ
        :return:
        """
        self.specan.write('DM:IFR {}e6 HZ'.format(frequency))
        logging.info('DM:IFR {}e6 HZ'.format(frequency))
        self.specan.query('*OPC?')
        del self.specan

    def set_interferer_singal_frequency_offset(self, frequency):
        """
        Sets the frequency offset of the useful signal in the baseband.
            Range:       -10.00 MHz  to  +10.00 MHz
            Increment:    0.1 Hz
            *RST:         0 Hz
            Default unit: Hz
        example :
            DM:SFR -1e6 Hz
        :return:
        """
        self.specan.write('DM:SFR {}e6 HZ'.format(frequency))
        logging.info('DM:SFR {}e6 HZ'.format(frequency))
        self.specan.query('*OPC?')
        del self.specan

    def set_impairments_modulator(self, modulator_type):
        """
        Activates or deactivates the three impairment or correction values LEAKage, QUADrature and IQRatio for the analog signal in the I/Q modulator.
            ON
            OFF
        example :
            IQ:IMP OFF
        :return:
        """
        self.specan.write('IQ:IMP {}'.format(modulator_type))
        logging.info('IQ:IMP {}'.format(modulator_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_impairments_modulator_quadrature(self, quadrature_num):
        """
        Sets the quadrature offset of I/Q modulation.
            Range:         -10.0  to  10.0 deg
            Increment:     0.02 deg
            *RST:          0 deg
            Default unit:  deg
        example :
            IQ:IMP:QUAD:ANGL -5DEG
        :return:
        """
        self.specan.write('IQ:IMP:QUAD:ANGL {}DEG'.format(quadrature_num))
        logging.info('IQ:IMP:QUAD:ANGL {}DEG'.format(quadrature_num))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_impairments_modulator_amplitude(self, amplitude_num):
        """
        Sets the ratio of I gain to Q gain (gain imbalance).
            Range:         -10  to  +10%
            Increment:      0.05%
            *RST:           0%
            Default unit:   %
        example :
            IQ:IMP:IQR 3 PCT
        :return:
        """
        self.specan.write('IQ:IMP:IQR {} PCT'.format(amplitude_num))
        logging.info('IQ:IMP:IQR {} PCT'.format(amplitude_num))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_impairments_baseband(self, baseband_type):
        """
        Activates (ON) or deactivates (OFF) the three impairment or correction values for the digital signal in the baseband:
            ON
            OFF
        example :
            BB:IMP OFF
        :return:
        """
        self.specan.write('BB:IMP {}'.format(baseband_type))
        logging.info('BB:IMP {}'.format(baseband_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_impairments_baseband_quadrature(self, quadrature_num):
        """
        Sets the quadrature offset of I/Q modulation.
            Range:           -10.0  to  10.0 deg
            Increment:       0.02 deg
            *RST:            0 deg
            Default unit:    deg
        example :
            BB:IMP:QUAD:ANGL -5DEG
        :return:
        """
        self.specan.write('BB:IMP:QUAD:ANGL {}DEG'.format(quadrature_num))
        logging.info('BB:IMP:QUAD:ANGL {}DEG'.format(quadrature_num))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_impairments_baseband_amplitude(self, amplitude_num):
        """
        Sets the ratio of I gain to Q gain (gain imbalance).
            Range:         -10  to  +10%
            Increment:      0.05%
            *RST:           0%
            Default unit:   %
        example :
            BB:IMP:IQR 3 PCT
        :return:
        """
        self.specan.write('BB:IMP:IQR {} PCT'.format(amplitude_num))
        logging.info('BB:IMP:IQR {} PCT'.format(amplitude_num))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_impairments_optimize(self, optimize_type):
        """
       Activates or deactivates internal compensation of signal distortions by the I/Q modulator.
            ON
            OFF
        example :
            BB:IMP:OPT:STAT ON
        :return:
        """
        self.specan.write('BB:IMP:OPT:STAT {}'.format(optimize_type))
        logging.info('BB:IMP:OPT:STAT {}'.format(optimize_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_noise_noise_noise(self, noise_type):
        """
        Switches the noise generator on or off or selects a signal.
            OFF
            ADD         Useful signal with noise
            ONLY        Pure noise signal
        example :
            NOIS ADD
        :return:
        """
        self.specan.write('NOIS {}'.format(noise_type))
        logging.info('NOIS {}'.format(noise_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_noise_noise_awgn(self, awgn_type):
        """
        Switches the Gaussian noise generator on or off.
        Only effective if "ADD" or "ONLY"

        not complete
            ON
            OFF
        example :
            NOIS:AWGN OFF
        :return:
        """
        self.specan.write('NOIS:AWGN {}'.format(awgn_type))
        logging.info('NOIS:AWGN {}'.format(awgn_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_noise_noise_impulsive(self, awgn_type):
        """
        Switches the impulsive noise generator on or off.
            ON
            OFF
        example :
            NOIS:IMP ON
        :return:
        """
        self.specan.write('NOIS:IMP {}'.format(awgn_type))
        logging.info('NOIS:IMP {}'.format(awgn_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_noise_noise_phase(self, phase_type):
        """
        Switches the phase noise generator on or off.
            ON
            OFF
        example :
            NOIS:PHAS ON
        :return:
        """
        self.specan.write('NOIS:PHAS {}'.format(phase_type))
        logging.info('NOIS:PHAS {}'.format(phase_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_noise_awgn_cn(self, cn):
        """
        Sets the carrier/noise ratio (C/N).
            Range:              -35.0  to  60.0 dB
            Increment:          0.1 dB
            *RST:               20 dB
            Default unit:       dB
        example :
            NOIS:CN 45
        :return:
        """
        self.specan.write('NOIS:CN {}'.format(cn))
        logging.info('NOIS:CN {}'.format(cn))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_noise_awgn_ebno(self, ebno):
        """
        This function queries the noise Eb/N0 ratio
        example :
            NOISe:EN?
        :return:
        """
        self.specan.write('NOIS:EN {}'.format(ebno))
        logging.info('NOIS:EN {}'.format(ebno))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_noise_impulsive_ci(self, ci_noise):
        """
        Sets the carrier/impulsive noise ratio (C/I).
            Range: -35.0  to  60.0 dB
            Increment: 0.1 dB
            *RST:20 dB
            Default unit: dB
        example :
            NOIS:IMP:CI 45
        :return:
        """
        self.specan.write('NOIS:IMP:CI {}'.format(ci_noise))
        logging.info('NOIS:IMP:CI {}'.format(ci_noise))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_noise_impulsive_frameduration(self, frameduration_type):
        """
        Sets the frame duration of the impulsive noise generator.
        Parameters:<num>
            0.010 s
            0.100 s
            1.000 s
            *RST:0.010 s
        example :
            NOIS:IMP:FRAM 0.1
            Sets frame duration of 100 ms.
        :return:
        """
        self.specan.write('NOIS:IMP:FRAM {}'.format(frameduration_type))
        logging.info('NOIS:IMP:FRAM {}'.format(frameduration_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_noise_settings_bandwith(self, switch_type):
        """
        Switches the bandwidth coupling on or off.
            Parameters:<bool>
            ON
            OFF
        example :
            NOIS:COUP ON
            Switches on bandwidth coupling.
        :return:
        """
        self.specan.write('NOIS:COUP {}'.format(switch_type))
        logging.info('NOIS:COUP {}'.format(switch_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_noise_settings_receiver(self, bandwidth):
        """
        Sets the equivalent receiver noise bandwidth for calculating the C/N ratio.
        Sets the (receiver) noise bandwidth.
            Range: 1e6  to  80e6 Hz
            Increment: 1 Hz
            *RST:10e6 Hz
            Default unit: Hz
        example :
            NOIS:BAND 7.5e6
        :return:
        """
        self.specan.write('NOIS:BAND {}'.format(bandwidth))
        logging.info('NOIS:BAND {}'.format(bandwidth))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_fading_state(self, state_type):
        """
        Activates fading simulation.
        Requires the R&S SFU-B30 and R&S SFU-K30 options.
        FSIMulator2 requires the R&S SFU-B31 option.
            ON
            OFF
        example :
            FSIM ON
        :return:
        """
        self.specan.write('FSIM {}'.format(state_type))
        logging.info('FSIM {}'.format(state_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_parameterset(self, parameterset_type):
        """
        Selects a predefined fading simulator setting which complies with the test specifications found in the common broadcast standards.
        Requires the R&S SFU-B30 and R&S SFU-K30 options.
        FSIMulator2 requires the R&S SFU-B31 option.
            <parameter>
            EASY3
            ECHO
            FX_echo
            PT_echo
            SFN_echo
            TU6
            TU6_
            RA4
            RA6
            RA6_
            RC6_anx_b
            RL6_anx_b
            RED_ht100
            ET50
            VALidate100
            RC12_anx_b
            RL12_anx_b
            TU3_12path
            TU50_12path
            HT100_12path
            RC20_anx_b
            RL20_anx_b
            HIC
            HNIC
            HPT
            HNPT
            AA_Static
            AB_Static
            AC_Static
            AD_Static
            AE_Static
            AF_Static
            AG_Static
            B_ECho
            C1_Random
            C2_Random
            C3_Random
            MBRai
            A_BRazil
            B_BRazil
            C_BRazil
            CS_Brazil
            CM_Brazil
            D_BRazil
            DM_Brazil
            E_BRazil
            D1CRc_dyn
            D2CRc_dyn
            D3CRc_dyn
            D4CRc_dyn
            AACats
            CHP1
            CHP2
            CHP3
            CHP4
            CHP5
            CHP6
            CHP7
            TU12
            IECP_62002
            PI
            PO
            VU
            MR
            DAB_
        example :
            FSIM:STAN TU6
            Selects settings in conformity with typical urban 6 (with 6 fading paths).
        :return:
        """
        self.specan.write('FSIM:STAN {}'.format(parameterset_type))
        logging.info('FSIM:STAN {}'.format(parameterset_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_configuration(self, configuration_type):
        """
        Sets the fading configuration.
        The allowed entries depend on the installed options.
        FSIMulator2 requires the R&S SFU-B31 option.
            BIRThdeath
            DELay
            D30Fine
            D50Fine
            MDELay
            P2DYn
        example :
            FSIM:CONF DEL
        :return:
        """
        self.specan.write('FSIM:CONF {}'.format(configuration_type))
        logging.info('FSIM:CONF {}'.format(configuration_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_state(self, group, path, state_type):
        """
        Activate or deactivate the selected path for the standard delay and fine delay 30 MHz / 50 MHz fading configurations.
            ON
            OFF
            Suffix:
            {1:2}       Fader A or B for fading split
            {1:8}       Path group; 1 to 8 for max. path, otherwise 1 to 4.
            {1:n}       Path 1 to n
        example :
            FSIM:DEL:GRO:PATH2:STAT ON
        :return:
        """
        self.specan.write('FSIM:DEL:GRO{}:PATH{}:STAT {}'.format(group, path, state_type))
        logging.info('FSIM:DEL:GRO{}:PATH{}:STAT {}'.format(group, path, state_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_profile(self, group, path, state_type):
        """
        Activate or deactivate the selected path for the standard delay and fine delay 30 MHz / 50 MHz fading configurations.
            PDOPpler
            SPATh
            RAYLeigh
            RICE
            CPHase
            GAU1
            GAU2
            GAUD
            GDOP
            G01
            G008
        Suffix:
        {1:2}       Fader A or B for fading split
        {1:8}       Path group; 1 to 8 for max. path, otherwise 1 to 4.
        {1:n}       Path 1 to n
        example :
            FSIM:DEL:GRO:PATH2:PROF RICE
        :return:
        """
        self.specan.write('FSIM:DEL:GRO{}:PATH{}:PROF {}'.format(group, path, state_type))
        logging.info('FSIM:DEL:GRO{}:PATH{}:PROF {}'.format(group, path, state_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_pathloss(self, group, path, pathloss):
        """
        Set the loss of the paths for the standard delay and fine delay 30 MHz / 50 MHz fading configurations.
        Parameters:
            Range: 0.0  to  50.0 dB
            Increment: 0.1 dB
            *RST:0 dB
            Default unit: dB

        example :
            FSIM:DEL:GRO:PATH2:LOSS 2 dB
        :return:
        """
        self.specan.write('FSIM:DEL:GRO{}:PATH{}:LOSS {}'.format(group, path, pathloss))
        logging.info('FSIM:DEL:GRO{}:PATH{}:LOSS {}'.format(group, path, pathloss))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_basicdelay(self, group, basicdelay):
        """
        Determine the group delay (basic delay) for the standard delay and fine delay 30 MHz / 50 MHz fading
        configurations. Within a group, all of the paths are jointly delayed by this value. The resulting delay of a
        path is obtained by adding the basic delay and the additional delay. The basic delay of group 1 and 5
        is always equal to 0.
        Parameters:
            Range: 0.0  to  5.24287e-3 s
            Increment: 10 ns
            *RST:0.0 ns
            Default unit: s
        example :
            FSIM:DEL:GRO2:BDEL 1E-3
        :return:
        """
        self.specan.write('FSIM:DEL:GRO{}:BDEL {}'.format(group, basicdelay))
        logging.info('FSIM:DEL:GRO{}:BDEL {}'.format(group, basicdelay))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_additdelay(self, group, path, additdelay):
        """
        Determine the path-specific delay (additional delay) of the selected path for the standard delay and fine
        delay 30 MHz / 50 MHz fading configurations.
        Parameters:
            Range: 0.0  to  40.9e-6 s
            Increment: Standard delay: 10 ns, fine delay 50 MHz: 10 ps, fine delay 30 MHz: 10 ps
            *RST:0
            Default unit: s
        example :
            FSIM:DEL:GRO:PATH2:ADEL 10E-6
        :return:
        """
        self.specan.write('FSIM:DEL:GRO{}:PATH{}:ADEL {}'.format(group, path, additdelay))
        logging.info('FSIM:DEL:GRO{}:PATH{}:ADEL {}'.format(group, path, additdelay))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_resuldelay(self, group, path, resuldelay):
        """
        Query the resulting delay of the paths for the standard delay and fine delay 30 MHz / 50 MHz fading configurations.
        not complte
        example :
            FSIM:DEL:GRO2:PATH2:RDEL 0.00021
        :return:
        """
        self.specan.write('FSIM:DEL:GRO{}:PATH{}:RDEL {}'.format(group, path, resuldelay))
        logging.info('FSIM:DEL:GRO{}:PATH{}:RDEL {}'.format(group, path, resuldelay))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_power(self, group, path, power):
        """
        Query the resulting delay of the paths for the standard delay and fine delay 30 MHz / 50 MHz fading configurations.
        need profile is RICE
            Range: -30.0  to  +30.0 dB
            Increment: 0.1 dB
            *RST:0 dB
            Default unit: dB
        example :
            FSIM:DEL:GRO:PATH2:PRAT -15
        :return:
        """
        self.specan.write('FSIM:DEL:GRO{}:PATH{}:PRAT {}'.format(group, path, power))
        logging.info('FSIM:DEL:GRO{}:PATH{}:PRAT {}'.format(group, path, power))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_constphase(self, group, path, constphase):
        """
        Determine the phase for constant phase and pure Doppler fading for the standard delay and fine delay
        30 MHz / 50 MHz fading configurations
        need profile is RICE
            Range: 0.0  to  359.9 deg
            Increment: 0.1 deg
            *RST:0 deg
            Default unit: deg
        example :
            FSIM:DEL:GRO2:PATH:CPH 5DEG
        :return:
        """
        self.specan.write('FSIM:DEL:GRO{}:PATH{}:CPH {}'.format(group, path, constphase))
        logging.info('FSIM:DEL:GRO{}:PATH{}:CPH {}'.format(group, path, constphase))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_speed(self, group, path, speed):
        """
        Set the speed v of the moving receiver for the standard delay and fine delay 30 MHz / 50 MHz fading configurations
            Range: 0.0  to  4796680.0 m/s
            Increment: 0.1 m/s
            *RST:0 m/s
            Default unit: m/s
        example :
            FSIM:DEL:GRO:PATH2:SPE 2
        :return:
        """
        self.specan.write('FSIM:DEL:GRO{}:PATH{}:SPE {}'.format(group, path, speed))
        logging.info('FSIM:DEL:GRO{}:PATH{}:SPE {}'.format(group, path, speed))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_freqratio(self, group, path, freq):
        """
        Set the ratio of the actual Doppler frequency to the set Doppler frequency for the standard delay and fine delay
        30 MHz / 50 MHz fading configurations for Rice and pure Doppler fading.
            Range: -1.0  to  +1.0
            Increment:0.05
            *RST:1
        example :
            FSIM:DEL:GRO:PATH2:FRAT -0.71
        :return:
        """
        self.specan.write('FSIM:DEL:GRO{}:PATH{}:FRAT {}'.format(group, path, freq))
        logging.info('FSIM:DEL:GRO{}:PATH{}:FRAT {}'.format(group, path, freq))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_doppler(self, group, path, doppler):
        """
        Set or query the Doppler frequency for the standard delay and fine delay 30 MHz / 50 MHz fading configurations.\
        not complte
            Range: 0.0  to  1600.0
            Default unit: Hz
        example :
            FSIM:DEL:GRO:PATH:FDOP 556
        :return:
        """
        self.specan.write('FSIM:DEL:GRO{}:PATH{}:FDOP {}'.format(group, path, doppler))
        logging.info('FSIM:DEL:GRO{}:PATH{}:FDOP {}'.format(group, path, doppler))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_correlation(self, group, path, correlation_type):
        """
        witch on correlation of the paths of the first fader to the corresponding paths of the second fader for the
        standard delay and fine delay 30 MHz / 50 MHz fading configurations.
            ON
            OFF
        example :
            FSIM:DEL:GRO2:PATH:CORR:STAT ON
        :return:
        """
        self.specan.write('FSIM:DEL:GRO{}:PATH{}:CORR:STAT {}'.format(group, path, correlation_type))
        logging.info('FSIM:DEL:GRO{}:PATH{}:CORR:STAT {}'.format(group, path, correlation_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_coefficient(self, group, path, coefficient):
        """
        Determine the magnitude of the complex correlation coefficient for the standard delay and fine delay
        30 MHz / 50 MHz fading configurations
            Range: 0.0  to  100.0%
            Increment: 5%
            *RST:100%
            Default unit: %
        example :
            FSIM:DEL:GRO2:PATH:CORR:COEF 95
        :return:
        """
        self.specan.write('FSIM:DEL:GRO{}:PATH{}:CORR:COEF {}'.format(group, path, coefficient))
        logging.info('FSIM:DEL:GRO{}:PATH{}:CORR:COEF {}'.format(group, path, coefficient))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_phase(self, group, path, phase):
        """
        Determine the phase of the complex correlation coefficient for the standard delay and fine delay 30 MHz / 50 MHz
        fading configurations.
            Range: 0.0  to  359.9 deg
            Increment: 0.1 deg
            *RST:0 deg
            Default unit: deg
        example :
            FSIM:DEL:GRO2:PATH:CORR:PHAS 5
        :return:
        """
        self.specan.write('FSIM:DEL:GRO{}:PATH{}:CORR:PHAS {}'.format(group, path, phase))
        logging.info('FSIM:DEL:GRO{}:PATH{}:CORR:PHAS {}'.format(group, path, phase))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_lognormal(self, group, path, state_type):
        """
        Switch lognormal fading on or off for the standard delay and fine delay 30 MHz / 50 MHz fading configurations.
            ON
            OFF
        example :
            FSIM:DEL:GRO:PATH2:LOGN:STAT ON
        :return:
        """
        self.specan.write('FSIM:DEL:GRO{}:PATH{}:LOGN:STAT {}'.format(group, path, state_type))
        logging.info('FSIM:DEL:GRO{}:PATH{}:LOGN:STAT {}'.format(group, path, state_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_localconstant(self, group, path, local_constant):
        """
        Switch lognormal fading on or off for the standard delay and fine delay 30 MHz / 50 MHz fading configurations.
        not complet
            Range: 0.0  to  200.0 m
            Increment: 0.1 m
            *RST:100 m
            Default unit: m
        example :
            FSIM:DEL:GRO:PATH2:LOGN:LCON 100
        :return:
        """
        self.specan.write('FSIM:DEL:GRO{}:PATH{}:LOGN:LCON {}'.format(group, path, local_constant))
        logging.info('FSIM:DEL:GRO{}:PATH{}:LOGN:LCON {}'.format(group, path, local_constant))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_profile_standard(self, group, path, standard):
        """
        Set the standard deviation for lognormal fading for the standard delay and fine delay 30 MHz / 50 MHz fading
            Range: 0.0  to  12.0 dB
            Increment: 1dB
            *RST:0 dB
            Default unit: dB
        example :
            FSIM:DEL:GRO:PATH2:LOGN:CSTD 2
        :return:
        """
        self.specan.write('FSIM:DEL:GRO{}:PATH{}:LOGN:CSTD {}'.format(group, path, standard))
        logging.info('FSIM:DEL:GRO{}:PATH{}:LOGN:CSTD {}'.format(group, path, standard))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_settings_speedunit(self, speed_unit):
        """
        Set the standard deviation for lognormal fading for the standard delay and fine delay 30 MHz / 50 MHz fading
            MPS
            KMH
            MPH
        example :
            FSIM:SPE:UNIT MPS
        :return:
        """
        self.specan.write('FSIM:SPE:UNIT {}'.format(speed_unit))
        logging.info('FSIM:SPE:UNIT {}'.format(speed_unit))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_settings_reference(self, reference_type):
        """
        Set the constant in the formula for the Doppler frequency calculation
        not complet
            SPEed
            FDOPpler
        example :
            FSIM:REF:SPE
        :return:
        """
        self.specan.write('FSIM:REF:{}'.format(reference_type))
        logging.info('FSIM:REF:{}'.format(reference_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_settings_common(self, doppler_type):
        """
        Set the constant in the formula for the Doppler frequency calculation
        not complet
            ON
            OFF
        example :
            FSIM:CSP ON
        :return:
        """
        self.specan.write('FSIM:CSP:{}'.format(doppler_type))
        logging.info('FSIM:CSP:{}'.format(doppler_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_settings_ignore(self, ignore_type):
        """
        Determines whether frequency changes < 5% are ignored. This enables faster frequency hopping.
            ON
            OFF
        example :
            FSIM:IGN:RFCH ON
        :return:
        """
        self.specan.write('FSIM:IGN:RFCH {}'.format(ignore_type))
        logging.info('FSIM:IGN:RFCH {}'.format(ignore_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_settings_signal(self, signal_type):
        """
        Determines whether frequency changes < 5% are ignored. This enables faster frequency hopping.
            BB
            RF
            SFU
            SFE
            SMU
        example :
            FSIM:SDES RF
        :return:
        """
        self.specan.write('FSIM:SDES {}'.format(signal_type))
        logging.info('FSIM:SDES {}'.format(signal_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_settings_insertionmode(self, mode_type):
        """
        Sets the insertion loss of the fading simulator.
            NORMal
            LACP
            USER
        example :
            FSIM:ILOS:MODE USER
        :return:
        """
        self.specan.write('FSIM:ILOS:MODE {}'.format(mode_type))
        logging.info('FSIM:ILOS:MODE {}'.format(mode_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_fading_settings_insertionloss(self, insertion_loss):
        """
        Sets the user-defined insertion loss of the fading simulator if USER is selected.
            Range: -3  to  +30.0 dB
            Increment: 0.1 dB
            *RST:0.0 dB
            Default unit: dB
        example :
            FSIM:ILOS 4 dB
        :return:
        """
        self.specan.write('FSIM:ILOS {}'.format(insertion_loss))
        logging.info('FSIM:ILOS {}'.format(insertion_loss))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_input_source_dvbc(self, source_type):
        """
        Selects the signal source for the DVB-C coder.
            EXTernal
            TSPLayer
            TESTsignal
        example :
            DVBC:SOUR TEST
        :return:
        """
        self.specan.write('DVBC:SOUR {}'.format(source_type))
        logging.info('DVBC:SOUR {}'.format(source_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_symbolrate_dvbc(self, symbol_rate):
        """
        Sets the symbol rate.
            Range: 100000  to  8000000 MS/s
            *RST:6.900000e6
            Default unit: S/s
        example :
            DVBC:SYMB 4.711e6
        :return:
        """
        self.specan.write('DVBC:SYMB {}'.format(symbol_rate))
        logging.info('DVBC:SYMB {}'.format(symbol_rate))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_constellation_dvbc(self, symbol_rate):
        """
        Selects the modulation (constellation) of the DVB-C signal.
            C16          16QAM
            C32          32QAM
            C64          64QAM
            C128        128QAM
            C256        256QAM
         Example:
            DVBC:CONS C64
        :return:
        """
        self.specan.write('DVBC:CONS {}'.format(symbol_rate))
        logging.info('DVBC:CONS {}'.format(symbol_rate))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_rolloff_dvbc(self, roll_type):
        """
        Selects the roll off.
            0.10
            0.13
            0.15
            0.18
            0.20
         Example:
            DVBC:ROLL 0.13
        :return:
        """
        self.specan.write('DVBC:ROLL {}'.format(roll_type))
        logging.info('DVBC:ROLL {}'.format(roll_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_special_special_dvbc(self, special_type):
        """
        Enables the special settings.
            ON
            OFF
         Example:
            DVBC:SETT ON
        :return:
        """
        self.specan.write('DVBC:SETT {}'.format(special_type))
        logging.info('DVBC:SETT {}'.format(special_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_testtspacket_dvbc(self, packet_type):
        """
        Selects the mode of the test TS packet.
            H184        Head / 184 payload
            S187        Sync / 187 payload
         Example:
            DVBC:TSP S187
        :return:
        """
        self.specan.write('DVBC:TSP {}'.format(packet_type))
        logging.info('DVBC:TSP {}'.format(packet_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_pidtestpacket_dvbc(self, packet_type):
        """
        Selects the PID test packet.
            NULL
            VARiable
         Example:
            DVBC:PIDT VAR
        :return:
        """
        self.specan.write('DVBC:PIDT {}'.format(packet_type))
        logging.info('DVBC:PIDT {}'.format(packet_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_payloadtest_dvbc(self, stuff_type):
        """
        Selects the payload in the TS packets of the DVB-C signal.
            PRBS
            H00     Hex 00
            HFF     Hex FF
         Example:
            DVBC:PAYL HFF
        :return:
        """
        self.specan.write('DVBC:PAYL {}'.format(stuff_type))
        logging.info('DVBC:PAYL {}'.format(stuff_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_prbs_dvbc(self, prbs_type):
        """
        Selects the mode of the PRBS.
            P23_1       2^23 - 1 (ITU-T O.151)
            P15_1       2^15 - 1 (ITU-T O.151)
         Example:
            DVBC:PRBS P15_1
        :return:
        """
        self.specan.write('DVBC:PRBS {}'.format(prbs_type))
        logging.info('DVBC:PRBS {}'.format(prbs_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_input_source_dvbt(self, source_type):
        """
        Selects the signal source for the DVB-T coder for high priority in hierarchic and nonhierarchical coding.
            EXTernal
            TSPLayer
            TESTsignal
        example :
            DVBT:SOUR TEST
        :return:
        """
        self.specan.write('DVBT:SOUR {}'.format(source_type))
        logging.info('DVBT:SOUR {}'.format(source_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_input_stuffing_dvbt(self, source_type):
        """
        Sets the stuffing for the high priority branch in hierarchic or nonhierarchical coding.
            OFF         Stuffing off.
            ON          Stuffing on.
            ONEXtclk    Stuffing with an external clock signal
        example :
            DVBT:STUF OFF
        :return:
        """
        self.specan.write('DVBT:STUF {}'.format(source_type))
        logging.info('DVBT:STUF {}'.format(source_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_channelbandwidth_dvbt(self, bandwidth_type):
        """
        Selects the channel bandwidth for the DVB-T signal.
            BW_8        8 MHz
            BW_7        7 MHz
            BW_6        6 MHz
            BW_5        5 MHz
        example :
            DVBT:CHAN BW_7
        :return:
        """
        self.specan.write('DVBT:CHAN {}'.format(bandwidth_type))
        logging.info('DVBT:CHAN {}'.format(bandwidth_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_fftmode_dvbt(self, mode_type):
        """
        Sets the FFT mode of the DVB-T signal.
            M2K     2K
            M4K     4K
            M8K     8K
        example :
            DVBT:FFT:MODE M2K
        :return:
        """
        self.specan.write('DVBT:FFT:MODE {}'.format(mode_type))
        logging.info('DVBT:FFT:MODE {}'.format(mode_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_guard_dvbt(self, guard_type):
        """
        Sets the guard interval of the useful OFDM symbol duration Tu.
            G1_4        1/4
            G1_8        1/8
            G1_16       1/16
            G1_32       1/32
        example :
            DVBT:GUAR:INT G1_4
        :return:
        """
        self.specan.write('DVBT:GUAR:INT {}'.format(guard_type))
        logging.info('DVBT:GUAR:INT {}'.format(guard_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_dvbhstate_dvbt(self, state_type):
        """
        Switches the DVB-H modulation on or off.
            ON
            OFF
        example :
            DVBT:DVHS ON
        :return:
        """
        self.specan.write('DVBT:DVHS {}'.format(state_type))
        logging.info('DVBT:DVHS {}'.format(state_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_hierarchy_dvbt(self, state_type):
        """
        Sets the hierarchy of the DVB-T signal.
            NONHier     none
            A1          α = 1
            A2          α = 2
            A4          α = 4
        example :
            DVBT:HIER A4
        :return:
        """
        self.specan.write('DVBT:HIER {}'.format(state_type))
        logging.info('DVBT:HIER {}'.format(state_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_constellation_dvbt(self, constellation_type):
        """
        Selects the modulation (constellation) of the DVB-T signal.
            T4      QPSK
            T16     16QAM
            T64     64QAM
        example :
            DVBT:CONS T64
        :return:
        """
        self.specan.write('DVBT:CONS {}'.format(constellation_type))
        logging.info('DVBT:CONS {}'.format(constellation_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_coderate_dvbt(self, code_rate):
        """
        Selects the code rate for high priority in hierarchic and nonhierarchical coding.
            R1_2        1/2
            R2_3        2/3
            R3_4        3/4
            R5_6        5/6
            R7_8        7/8
        example :
            DVBT:RATE R7_8
        :return:
        """
        self.specan.write('DVBT:RATE {}'.format(code_rate))
        logging.info('DVBT:RATE {}'.format(code_rate))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_special_special_dvbt(self, special_rate):
        """
        Enables the special settings.
            ON
            OFF
        example :
            DVBT:SETT ON
        :return:
        """
        self.specan.write('DVBT:SETT {}'.format(special_rate))
        logging.info('DVBT:SETT {}'.format(special_rate))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_testtspacket_dvbt(self, packet_type):
        """
        Selects the mode of the test TS packet.
            H184        Head / 184 payload
            S187        Sync / 187 payload
        example :
            DVBT:TSP S187
        :return:
        """
        self.specan.write('DVBT:TSP {}'.format(packet_type))
        logging.info('DVBT:TSP {}'.format(packet_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_pidtestpacket_dvbt(self, packet_type):
        """
        Selects the PID test packet.
            NULL
            VARiable
        example :
            DVBT:PIDT VAR
        :return:
        """
        self.specan.write('DVBT:PIDT {}'.format(packet_type))
        logging.info('DVBT:PIDT {}'.format(packet_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_payloadtest_dvbt(self, stuff_type):
        """
        Selects the payload in the TS packets of the DVB-T signal.
            PRBS
            H00     Hex 00
            HFF     Hex FF
        example :
            DVBT:PAYL HFF
        :return:
        """
        self.specan.write('DVBT:PAYL {}'.format(stuff_type))
        logging.info('DVBT:PAYL {}'.format(stuff_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_prbs_dvbt(self, prbs_type):
        """
        Selects the mode of the PRBS.
            P23_1       2^23 - 1 (ITU-T O.151)
            P15_1       2^15 - 1 (ITU-T O.151)
        example :
            DVBT:PRBS P15_1
        :return:
        """
        self.specan.write('DVBT:PRBS {}'.format(prbs_type))
        logging.info('DVBT:PRBS {}'.format(prbs_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_tpscall_dvbt(self, hex_num):
        """
        Sets the cell ID.
            Range:      #H0000  to  #HFFFF
            Increment:  1
            *RST:       #H0000
        example :
            DVBT:CELL:ID #H123A
        :return:
        """
        self.specan.write('DVBT:CELL:ID {}'.format(hex_num))
        logging.info('DVBT:CELL:ID {}'.format(hex_num))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_tpsreservedstate_dvbt(self, state_type):
        """
        Switches the TPS reserved state on or off.
            ON
            OFF
        example :
            DVBT:TPSR:STAT ON
        :return:
        """
        self.specan.write('DVBT:TPSR:STAT {}'.format(state_type))
        logging.info('DVBT:TPSR:STAT {}'.format(state_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_tpsreservedbits_dvbt(self, bits):
        """
        Sets the TPS reserved value.
            Range:      #H0  to  #HF
            *RST:       #H0
        example :
            DVBT:TPSR:VAL #H4
        :return:
        """
        self.specan.write('DVBT:TPSR:VAL {}'.format(bits))
        logging.info('DVBT:TPSR:VAL {}'.format(bits))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_timeslicing_dvbt(self, slicing_type):
        """
        Switches time slicing for the high priority branch on or off in hierarchic or nonhierarchical codin
            ON
            OFF
        example :
            DVBT:TIM OFF
        :return:
        """
        self.specan.write('DVBT:TIM {}'.format(slicing_type))
        logging.info('DVBT:TIM {}'.format(slicing_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_mpefec_dvbt(self, fec_type):
        """
        Switches MPE FEC for the high priority branch on or off in hierarchic or nonhierarchical coding.
            ON
            OFF
        example :
            DVBT:MPEF OFF
        :return:
        """
        self.specan.write('DVBT:MPEF {}'.format(fec_type))
        logging.info('DVBT:MPEF {}'.format(fec_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_input_t2miinterface_dvbt2(self, interface_type):
        """
        Activates or deactivates the T2 modulator interface.
            ON
            OFF
        example :
            T2DV:INP:T2MI:INT ON
        :return:
        """
        self.specan.write('T2DV:INP:T2MI:INT {}'.format(interface_type))
        logging.info('T2DV:INP:T2MI:INT {}'.format(interface_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_input_t2misource_dvbt2(self, source_type):
        """
        Sets the T2 modulator interface.
            INTernal
            EXTernal
        example :
            T2DV:INP:T2MI INT
        :return:
        """
        self.specan.write('T2DV:INP:T2MI {}'.format(source_type))
        logging.info('T2DV:INP:T2MI {}'.format(source_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_input_number_dvbt2(self, number):
        """
        Sets the PLP number (NPLP = 1: single PLP).
            INTernal
            EXTernal
        example :
            T2DV:INP:NPLP 1
        :return:
        """
        self.specan.write('T2DV:INP:NPLP {}'.format(number))
        logging.info('T2DV:INP:NPLP {}'.format(number))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_input_inputformat_dvbt2(self, format_type):
        """
        Sets the input format.
            GFPS
            GCS
            GSE
            TS
        example :
            T2DV:PLP1:INP:FORM TS
        :return:
        """
        self.specan.write('T2DV:PLP1:INP:FORM {}'.format(format_type))
        logging.info('T2DV:PLP1:INP:FORM {}'.format(format_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_input_source_dvbt2(self, source_type):
        """
        Sets the input source.
            EXTernal
            TSPLayer
            TESTsignal
        example :
            T2DV:PLP1:INP:SOUR TSPL
        :return:
        """
        self.specan.write('T2DV:PLP1:INP:SOUR {}'.format(source_type))
        logging.info('T2DV:PLP1:INP:SOUR {}'.format(source_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_input_stuffing_dvbt2(self, stuffing_type):
        """
        Sets the stuffing state.
            ON
            OFF
        example :
            T2DV:PLP1:INP:STUF OFF
        :return:
        """
        self.specan.write('T2DV:PLP1:INP:STUF {}'.format(stuffing_type))
        logging.info('T2DV:PLP1:INP:STUF {}'.format(stuffing_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_framing_channelbandwidth_dvbt2(self, bandwidth_type):
        """
        Sets the channel bandwidth.
            BW_10       10 MHz; short form is BW_1, used as return value.
            BW_8        8 MHz
            BW_7        7 MHz
            BW_6        6 MHz
            BW_5        5 MHz
            BW_2        1.7 MHz
        example :
            T2DV:CHAN BW_8
        :return:
        """
        self.specan.write('T2DV:CHAN {}'.format(bandwidth_type))
        logging.info('T2DV:CHAN {}'.format(bandwidth_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_framing_bandwidth_dvbt2(self, bandwidth):
        """
        Sets the bandwidth variation.

            Range:          -1000  to  +1000 ppm
            *RST:           0 ppm
            Default unit:   ppm
        example :
            T2DV:BAND:VAR 10
        :return:
        """
        self.specan.write('T2DV:BAND:VAR {}'.format(bandwidth))
        logging.info('T2DV:BAND:VAR {}'.format(bandwidth))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_framing_fftsize_dvbt2(self, fft_type):
        """
        Sets the FFT size.
            M1K
            M2K
            M4K
            M8K
            M16K
            M32K
            M8E
            M16E
            M32E
        example :
            T2DV:FFT:MODE M32E
        :return:
        """
        self.specan.write('T2DV:FFT:MODE {}'.format(fft_type))
        logging.info('T2DV:FFT:MODE {}'.format(fft_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_framing_guard_dvbt2(self, guard_type):
        """
        Sets the channel bandwidth.
            G1_4        1/4
            G1_8        1/8
            G1_16       1/16; short form is G1_1, used as return value.
            G1_32       1/32; short form is G1_3, used as return value.
            G1128       1/128; short form is G112, used as return value.
            G19128      19/128; short form is G191, used as return value.
            G19256      19/256; short form is G192, used as return value.
        example :
            T2DV:GUAR:INT G1128
        :return:
        """
        self.specan.write('T2DV:GUAR:INT {}'.format(guard_type))
        logging.info('T2DV:GUAR:INT {}'.format(guard_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_framing_pilot_dvbt2(self, piloy_type):
        """
        Sets the pilot pattern.
            PP1
            PP2
            PP3
            PP4
            PP5
            PP6
            PP7
            PP8
        example :
            T2DV:PIL PP7
        :return:
        """
        self.specan.write('T2DV:PIL {}'.format(piloy_type))
        logging.info('T2DV:PIL {}'.format(piloy_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_framing_nt2_dvbt2(self, n_t2):
        """
        Sets the number of T2 frames per super frame. For limitations see the DVB-T2 specifications.
        example :
            T2DV:NT2F 2
        :return:
        """
        self.specan.write('T2DV:NT2F {}'.format(n_t2))
        logging.info('T2DV:NT2F {}'.format(n_t2))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_framing_ldata_dvbt2(self, l_data):
        """
        Sets the data symbols per T2 frame (L_DATA).
        example :
            T2DV:LDAT 59
        :return:
        """
        self.specan.write('T2DV:LDAT {}'.format(l_data))
        logging.info('T2DV:LDAT {}'.format(l_data))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_framing_nsub_dvbt2(self, n_sub):
        """
        Sets the number of subslices per T2 frame (N_SUB).
        not complete
        example :
            T2DV:NSUB 1
        :return:
        """
        self.specan.write('T2DV:NSUB {}'.format(n_sub))
        logging.info('T2DV:NSUB {}'.format(n_sub))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_bicm_fecframe_dvbt2(self, frame_type):
        """
        Sets the FEC frame.
            NORMal
            SHORt
        example :
            T2DV:PLP1:FECF NORM
        :return:
        """
        self.specan.write('T2DV:PLP1:FECF {}'.format(frame_type))
        logging.info('T2DV:PLP1:FECF {}'.format(frame_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_bicm_coderate_dvbt2(self, code_rate):
        """
        Sets the code rate.
            R1_2        1/2
            R2_3        2/3
            R3_4        3/4
            R5_6        5/6
            R3_5        3/5
            R4_5        4/5
            R1_3        1/3
            R2_5        2/5
        example :
            T2DV:PLP1:RATE R3_5
        :return:
        """
        self.specan.write('T2DV:PLP1:RATE {}'.format(code_rate))
        logging.info('T2DV:PLP1:RATE {}'.format(code_rate))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_bicm_constellation_dvbt2(self, constellation_type):
        """
        Sets the constellation.
            T4          "QPSK"
            T16         "16QAM"
            T64         "64QAM"
            T256        "256QAM"
        example :
            T2DV:PLP1:CONS T256
        :return:
        """
        self.specan.write('T2DV:PLP1:CONS {}'.format(constellation_type))
        logging.info('T2DV:PLP1:CONS {}'.format(constellation_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_bicm_constelrotation_dvbt2(self, constellation_type):
        """
        Sets the constellation rotation state.
            ON
            OFF
        example :
            T2DV:PLP1:CROT ON
        :return:
        """
        self.specan.write('T2DV:PLP1:CROT {}'.format(constellation_type))
        logging.info('T2DV:PLP1:CROT {}'.format(constellation_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_bicm_timeinterl_type_dvbt2(self, timeintel):
        """
        Sets the time interleaver type.
            0
            1
        example :
            T2DV:PLP1:TIL:TYPE 0
        :return:
        """
        self.specan.write('T2DV:PLP1:TIL:TYPE {}'.format(timeintel))
        logging.info('T2DV:PLP1:TIL:TYPE {}'.format(timeintel))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_bicm_frameint_dvbt2(self, frameint):
        """
        Sets the time interleaver frame interval (I jump). For limitations see the DVB-T2 specifications.
            "1"
            "2" to "255"
        example :
            T2DV:PLP1:TIL:FINT 1
        :return:
        """
        self.specan.write('T2DV:PLP1:TIL:FINT {}'.format(frameint))
        logging.info('T2DV:PLP1:TIL:FINT {}'.format(frameint))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_bicm_timeinterllength_dvbt2(self, frameint):
        """
        Sets the time interleaver length. For limitations see the DVB-T2 specifications.
            "0" to "255"
            If "0" is set and if "TIME INTERL. TYPE" = "0" ("TIME INTERL. TYPE") , the time interleaving is disabled.
        example :
            T2DV:PLP1:TIL:LENG 3
        :return:
        """
        self.specan.write('T2DV:PLP1:TIL:LENG {}'.format(frameint))
        logging.info('T2DV:PLP1:TIL:LENG {}'.format(frameint))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_system_modulation_dvbt2(self, modulation_type):
        """
        Sets the L1 post constellation.
            T2
            T4
            T16
            T64
        example :
            T2DV:L:CONS T64
        :return:
        """
        self.specan.write('T2DV:L:CONS {}'.format(modulation_type))
        logging.info('T2DV:L:CONS {}'.format(modulation_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_system_papr_dvbt2(self, papr_type):
        """
        Sets the peak-to-average-power ratio (PAPR) state.
            OFF
            TR
        example :
            T2DV:PAPR OFF
        :return:
        """
        self.specan.write('T2DV:PAPR {}'.format(papr_type))
        logging.info('T2DV:PAPR {}'.format(papr_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_testtspacket_dvbt2(self, packet_type):
        """
        Sets the payload length of the test TS packet.
            H184        Head / 184 payload
            S187        Sync / 187 payload
        example :
            T2DV:TSP S187
        :return:
        """
        self.specan.write('T2DV:TSP {}'.format(packet_type))
        logging.info('T2DV:TSP {}'.format(packet_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_pidtest_dvbt2(self, packet_type):
        """
        Sets the PID of test TS packet.
            NULL
            VARiable
        example :
            T2DV:PIDT NULL
        :return:
        """
        self.specan.write('T2DV:PIDT {}'.format(packet_type))
        logging.info('T2DV:PIDT {}'.format(packet_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_payload_dvbt2(self, packet_type):
        """
        Sets the payload of the test TS packets.
            PRBS
            H00     Hex 00
            HFF     Hex FF
        example :
            T2DV:PAYL PRBS
        :return:
        """
        self.specan.write('T2DV:PAYL {}'.format(packet_type))
        logging.info('T2DV:PAYL {}'.format(packet_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_prbs_dvbt2(self, prbs_type):
        """
        Sets the PRBS of the test TS packet.
            P23_1       2^23 - 1 (ITU-T O.151)
            P15_1       2^15 - 1 (ITU-T O.151)
        example :
            T2DV:PRBS P15_1
        :return:
        """
        self.specan.write('T2DV:PRBS {}'.format(prbs_type))
        logging.info('T2DV:PRBS {}'.format(prbs_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_input_source_j83b(self, source_type):
        """
        Selects the signal source for the J.83B coder.
            EXTernal
            TSPLayer
            TESTsignal
        example :
            J83B:SOUR TEST
        :return:
        """
        self.specan.write('J83B:SOUR {}'.format(source_type))
        logging.info('J83B:SOUR {}'.format(source_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_symbolrate_j83b(self, symbol_rate):
        """
        Sets the symbol rate.
        Parameters:
        <num> (64QAM)
            Range:          4.55124  to  5.56264 MS/s
            *RST:           5.056941e6
            Default unit:   S/s
        <num> (256QAM)
            Range:          4.82448  to  5.89659 MS/s
            *RST:           5.056941e6
            Default unit:   S/s
        example :
            J83B:SYMB 5.5e6
        :return:
        """
        self.specan.write('J83B:SYMB {}'.format(symbol_rate))
        logging.info('J83B:SYMB {}'.format(symbol_rate))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_coding_interleavermode_j83b(self, mode_type):
        """
        Selects the interleaver mode.
            0
            1
            2
            3
            4
            5
            6
            7
            8
            9
            10
            12
            14
        example :
            J83B:INT:MODE 0
        :return:
        """
        self.specan.write('J83B:INT:MODE {}'.format(mode_type))
        logging.info('J83B:INT:MODE {}'.format(mode_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_special_special_j83b(self, settings_type):
        """
        Enables the special settings.
            ON
            OFF
        example :
            J83B:SETT ON
        :return:
        """
        self.specan.write('J83B:SETT {}'.format(settings_type))
        logging.info('J83B:SETT {}'.format(settings_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_special_checksumgen_j83b(self, checksumgen_type):
        """
        Switches the checksum generator on or off.
            ON
            OFF
        example :
            J83B:CHEC OFF
        :return:
        """
        self.specan.write('J83B:CHEC {}'.format(checksumgen_type))
        logging.info('J83B:CHEC {}'.format(checksumgen_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_special_readsolomon_j83b(self, read_type):
        """
        Switches the Reed Solomon coder on or off.
            ON
            OFF
        example :
            J83B:REED OFF
        :return:
        """
        self.specan.write('J83B:REED {}'.format(read_type))
        logging.info('J83B:REED {}'.format(read_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_special_interleaver_j83b(self, interleaver_type):
        """
        Switches the interleaver on or off.
        not complte
            ON
            OFF
        example :
            J83B:INT OFF
        :return:
        """
        self.specan.write('J83B:INT {}'.format(interleaver_type))
        logging.info('J83B:INT {}'.format(interleaver_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_special_randomizer_j83b(self, randomizer_type):
        """
        Switches the randomizer on or off.
            ON
            OFF
        example :
            J83B:RAND OFF
        :return:
        """
        self.specan.write('J83B:RAND {}'.format(randomizer_type))
        logging.info('J83B:RAND {}'.format(randomizer_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_testtspacket_j83b(self, packet_type):
        """
        Selects the mode of the test TS packet.
            H184        Head / 184 payload
            S187        Sync / 187 payload
        example :
            J83B:TSP S187
        :return:
        """
        self.specan.write('J83B:TSP {}'.format(packet_type))
        logging.info('J83B:TSP {}'.format(packet_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_pidtest_j83b(self, packet_type):
        """
        Selects the PID test packet.
            NULL
            VARiable
        example :
            J83B:PIDT VAR
        :return:
        """
        self.specan.write('J83B:PIDT {}'.format(packet_type))
        logging.info('J83B:PIDT {}'.format(packet_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_payloadtest_j83b(self, payload_type):
        """
        Selects the payload in the TS packets of the J.83B signal
            PRBS
            H00     Hex 00
            HFF     Hex FF
        example :
            J83B:PAYL HFF
        :return:
        """
        self.specan.write('J83B:PAYL {}'.format(payload_type))
        logging.info('J83B:PAYL {}'.format(payload_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
        del self.specan

    def set_digitaltv_settings_prbs_j83b(self, prbs_type):
        """
        Selects the mode of the PRBS.
            P23_1       2^23 - 1 (ITU-T O.151)
            P15_1       2^15 - 1 (ITU-T O.151)
        example :
            J83B:PRBS P15_1
        :return:
        """
        self.specan.write('J83B:PRBS {}'.format(prbs_type))
        logging.info('J83B:PRBS {}'.format(prbs_type))
        # time.sleep(1)
        self.specan.query('*OPC?')
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
        # self.specan.write('NOIS:AWGN OFF')
        # self.specan.ext_clear_status()
        # print self.specan.query('*IDN?')
        # self.specan.query('*OPC?')
        self.specan.write('FSIM:REF:SPE')
        # self.specan.write('111')

    def set_player_timing_openfile(self, file_path):
        """
        Select the file to be loaded into the TS player.
        example :
            TSG:CONF:PLAY "d:\tsgen\live\jump.trp"
        :return:
        """
        self.specan.write(r'TSG:CONF:PLAY "{}"'.format(file_path))
        logging.info(r'TSG:CONF:PLAY "{}"'.format(file_path))
        # time.sleep(3)
        self.specan.query('*OPC?')
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
        self.specan.query('*OPC?')
        # time.sleep(17)
        del self.specan


def __del__(self):
    del self.specan


def _test_code():
    # net = "192.168.1.47"
    sfu_ip = "192.168.1.50"
    # host = '127.0.0.1'
    # port = 8900
    specan = Ektsfu(sfu_ip)
    # specan.set_frequency_frequency_frequency("990 MHz")
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
    # specan.set_level_settings_unit("DBM")
    # specan.set_modulation_modulation_modulation("ON")
    # specan.set_modulation_modulation_source("DTV")
    # specan.set_modulation_modulation_standard_atv("LPR")
    # specan.set_modulation_modulation_standard_dvt("T2DVb")
    # specan.set_digitaltv_input_source_dvbs2("TSPL")
    specan.set_digitaltv_coding_symbolrate_dvbs2("31.711e6")
    # specan.set_digitaltv_coding_constellation_dvbs2("S4")
    # specan.set_digitaltv_coding_fecframe_dvbs2("NORM")
    # specan.set_digitaltv_coding_pilots_dvbs2("OFF")
    # specan.set_digitaltv_coding_rolloff_dvbs2("0.25")
    # specan.set_digitaltv_coding_coderate_dvbs2("R8_9")
    # specan.set_digitaltv_special_settings_dvbs2("ON")
    # specan.set_digitaltv_phasenoise_phasenoise_dvbs2("ON")
    # specan.set_digitaltv_phasenoise_shape_dvbs2("SHA3")
    # specan.set_digitaltv_phasenoise_magnitude_dvbs2("3")
    # specan.set_digitaltv_settings_tspacket_dvbs2("S187")
    # specan.set_digitaltv_settings_pidpacket_dvbs2("VAR")
    # specan.set_digitaltv_settings_pid_dvbs2("0001")
    # specan.set_digitaltv_settings_payloadtest_dvbs2("HFF")
    # specan.set_digitaltv_settings_prbs_dvbs2("P15_1")
    # specan.set_interferer_source("ATVPr")
    # specan.set_noise_noise_noise("OFF")
    # specan = Ektsfu(sfu_ip)
    # specan.set_noise_noise_awgn("OFF")
    # specan.set_noise_awgn_cn("45")
    # specan.set_noise_impulsive_ci("45")
    # specan.set_noise_impulsive_frameduration("0.1")
    # specan.set_noise_settings_bandwith("ON")
    # specan.set_noise_settings_receiver("7.5e6")
    # specan.set_fading_fading_state("ON")
    # specan.set_fading_profile_parameterset("TU12")
    # specan.set_fading_profile_configuration("D30Fine")
    # specan.set_fading_profile_state("1", "1", "ON")
    # specan.set_fading_profile_profile("1", "1", "SPATh")
    # specan.set_fading_profile_pathloss("3", "1", "16 dB")
    # specan.set_fading_profile_basicdelay("2", "486E-6")
    # specan.set_fading_profile_additdelay("2", "1", "486E-6")
    # specan.set_fading_profile_resuldelay("2", "2", "20E-6")
    # specan.set_fading_profile_power("2", "2", "-15")
    # specan.set_fading_profile_constphase("2", "2", "5DEG")
    # specan.set_fading_profile_speed("2", "2", "2")
    # specan.set_fading_profile_freqratio("2", "2", "-0.71")
    # specan.set_fading_profile_doppler("2", "2", "2")
    # specan.set_fading_profile_correlation("2", "2", "ON")
    # specan.set_fading_profile_coefficient("2", "2", "95")
    # specan.set_fading_profile_phase("2", "2", "5")
    # specan.set_fading_profile_lognormal("2", "2", "ON")
    # specan.set_fading_profile_localconstant("2", "2", "100")
    # specan.set_fading_profile_standard("2", "2", "2")
    # specan.set_fading_settings_reference("SPEed")
    # specan.set_fading_settings_common("ON")
    # specan.set_fading_settings_ignore("ON")
    # specan.set_fading_settings_signal("BB")
    # specan.set_fading_settings_insertionmode("USER")
    # specan.set_fading_settings_insertionloss("5 dB")
    # specan.set_coder_output_symbol_rate_dvbc("5.711e6")
    # specan.set_digitaltv_coding_symbolrate_dvbc("C256")
    # specan.set_digitaltv_coding_coderate_dvbt("R7_8")
    # specan.set_digitaltv_coding_constellation_dvbt("T16")
    # specan.set_digitaltv_coding_guard_dvbt("G1_32")
    # specan.set_digitaltv_coding_channelbandwidth_dvbt("BW_7")
    # specan.set_digitaltv_coding_fftmode_dvbt("M8K")
    # specan.set_digitaltv_coding_dvbhstate_dvbt("OFF")
    # specan.set_digitaltv_coding_hierarchy_dvbt("NONHier")
    # specan.set_digitaltv_framing_fftsize_dvbt2("M32K")
    # specan.set_digitaltv_framing_channelbandwidth_dvbt2("BW_7")
    # specan.set_digitaltv_framing_guard_dvbt2("G1128")
    # specan.set_digitaltv_bicm_coderate_dvbt2("R3_4")
    # specan.set_digitaltv_bicm_constellation_dvbt2("T64")
    # specan.set_digitaltv_bicm_constelrotation_dvbt2("ON")
    # specan.set_digitaltv_settings_pidtest_dvbt2("NULL")
    # specan.set_digitaltv_input_source_j83b("TSPLayer")
    # specan.set_digitaltv_coding_symbolrate_j83b("4.7e6")
    # specan.set_digitaltv_coding_interleavermode_j83b("1")
    # specan.set_digitaltv_special_special_j83b("OFF")
    # specan.set_digitaltv_special_checksumgen_j83b("ON")
    # specan.set_digitaltv_special_readsolomon_j83b("OFF")
    # specan.set_digitaltv_special_interleaver_j83b("OFF")
    # specan.set_digitaltv_special_randomizer_j83b("OFF")
    # specan.set_digitaltv_settings_testtspacket_j83b("H184")
    # specan.set_digitaltv_settings_pidtest_j83b("NULL")
    # specan.set_digitaltv_settings_payloadtest_j83b("H00")
    # specan.set_digitaltv_settings_prbs_j83b("P15_1")
    # specan.set_digitaltv_settings_testtspacket_dvbt2("H184")
    # specan.set_digitaltv_settings_payload_dvbt2("H00")
    # specan.set_digitaltv_settings_prbs_dvbt2("P23_1")
    # specan.set_digitaltv_bicm_fecframe_dvbt2("SHORt")
    # specan.set_digitaltv_bicm_timeinterl_type_dvbt2("0")
    # specan.set_digitaltv_bicm_frameint_dvbt2("1")
    # specan.set_digitaltv_bicm_timeinterllength_dvbt2("4")
    # specan.set_digitaltv_framing_bandwidth_dvbt2("4")
    # specan.set_digitaltv_framing_pilot_dvbt2("PP7")
    # specan.set_digitaltv_framing_nt2_dvbt2("30")
    # specan.set_digitaltv_framing_ldata_dvbt2("61")
    # specan.set_digitaltv_framing_nsub_dvbt2("2")
    # specan.set_digitaltv_input_t2miinterface_dvbt2("OFF")
    # specan.set_digitaltv_input_t2misource_dvbt2("EXTernal")
    # specan.set_digitaltv_input_number_dvbt2("2")
    # specan.set_digitaltv_input_inputformat_dvbt2("GSE")
    # specan.set_digitaltv_input_source_dvbt2("TSPLayer")
    # specan.set_digitaltv_input_stuffing_dvbt2("OFF")
    # specan.set_digitaltv_input_source_dvbt("TSPLayer")
    # specan.set_digitaltv_input_stuffing_dvbt("ON")
    # specan.set_digitaltv_special_special_dvbt("OFF")
    # specan.set_digitaltv_settings_testtspacket_dvbt("S187")
    # specan.set_digitaltv_settings_pidtestpacket_dvbt("VARiable")
    # specan.set_digitaltv_settings_payloadtest_dvbt("H00")
    # specan.set_digitaltv_settings_prbs_dvbt("P15_1")
    # specan.set_digitaltv_settings_tpscall_dvbt("#H123A")
    # specan.set_digitaltv_settings_tpsreservedstate_dvbt("OFF")
    # specan.set_digitaltv_settings_tpsreservedbits_dvbt("#H7")
    # specan.set_digitaltv_settings_timeslicing_dvbt("OFF")
    # specan.set_digitaltv_settings_mpefec_dvbt("OFF")
    # specan.set_digitaltv_input_source_dvbc("TSPLayer")
    # specan.set_digitaltv_coding_rolloff_dvbc("0.18")
    # specan.set_digitaltv_special_special_dvbc("OFF")
    # specan.set_digitaltv_settings_testtspacket_dvbc("H184")
    # specan.set_digitaltv_settings_pidtestpacket_dvbc("VARiable")
    # specan.set_digitaltv_settings_payloadtest_dvbc("PRBS")
    # specan.set_digitaltv_settings_prbs_dvbc("P15_1")
    # specan.set_noise_noise_awgn("ON")
    # specan.set_noise_noise_impulsive("ON")
    # specan.set_frequency_settings_channlfrequency("5", "400 MHz")
    # specan.set_modulation_modulation_standard("J83B")
    # specan.set_modulation_modulation_spectrum("NORMal")
    # specan.set_modulation_settings_level("DBM3")
    # specan.set_modulation_settings_factor("20")
    # specan.set_modulation_settings_filtering("ON")
    # specan.set_modulation_settings_mode("WBEC")
    # specan.set_modulation_settings_output("AFC")
    # specan.set_noise_noise_phase("OFF")
    # specan.preset_instrument()
    # specan.set_impairments_modulator("ON")
    # specan.set_impairments_modulator_quadrature("-5")
    # specan.set_impairments_modulator_amplitude("3")
    # specan.set_impairments_baseband("OFF")
    # specan.set_impairments_baseband_quadrature("-5")
    # specan.set_impairments_baseband_amplitude("4")
    # specan.set_impairments_optimize("OFF")
    # specan.set_level_level_offset(str(4.6))
    # specan.set_player_timing_openfile(r"E:\333\DIVER.GTS")
    # specan.set_digitaltv_system_modulation_dvbt2("T64")
    # specan.set_digitaltv_system_papr_dvbt2("TR")
    # specan.set_interferer_source("ATVPr")
    # specan.set_interferer_addition("BEFN")
    # specan.set_interferer_reference("ATT")
    # specan.set_interferer_attenuation("5")
    # specan.set_interferer_level("-10")
    # specan.set_interferer_frequency_offset("-1")
    # specan.set_interferer_singal_frequency_offs99et("-1")
    # specan.set_fading_profile_pathloss("3", "1", "{} dB".format(str("16")))
    # specan.set_digitaltv_coding_channelbandwidth_dvbt("BW_{}".format(str("8")))
    # specan.set_fading_profile_pathloss("3", "1", "16 dB")
    # specan.set_fading_settings_speedunit("KMH")

    specan.set_cmd()

    # sfu_ip = "192.168.1.50"

    # specan = Ektsfu(sfu_ip)
    # specan.set_level_level_offset(str(4.6))
    # specan = Ektsfu(sfu_ip)
    # specan.set_level_level_level("dBm", "-30")


if __name__ == '__main__':
    _test_code()
    # pass

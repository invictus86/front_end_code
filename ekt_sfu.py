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
        time.sleep(0.1)

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
        logging.info('FREQ:CW {}'.format(frequency))
        time.sleep(0.1)

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
        time.sleep(0.1)

    def set_frequency_frequency_channel(self, channel):
        """
         Setting the channel.  Channels can be selected in the range of  1 ... 100
         example : FREQ:CHAN 5
        :return:
        """
        self.specan.write('FREQ:CHAN {}'.format(channel))
        logging.info('FREQ:CHAN {}'.format(channel))
        time.sleep(0.1)

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
        logging.info('SWE:STARt {}'.format(frequency))
        time.sleep(0.1)

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
        logging.info('SWE:STOP {}'.format(frequency))
        time.sleep(0.1)

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
        logging.info('SWE:CENT {}'.format(frequency))
        time.sleep(0.1)

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
        logging.info('SWE:SPAN {}'.format(frequency))
        time.sleep(0.1)

    def set_frequency_sweep_spacing(self, span_type):
        """
        Sets the type of progressive step size during the sweep.
        LINear     LOGarithmic
         example : SWE:SPAC LIN
        :return:
        """
        self.specan.write('SWE:SPAC {}'.format(span_type))
        logging.info('SWE:SPAC {}'.format(span_type))
        time.sleep(0.1)

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
        logging.info('SWE:STEP {}'.format(step_frequency))
        time.sleep(0.1)

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
        logging.info('SWE:DWEL {}'.format(dewll_time))
        time.sleep(0.1)

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
        logging.info('SWE:MODE AUTO'.format(mode_type))
        time.sleep(0.1)
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
        time.sleep(0.1)

    def set_frequency_sweep_reset(self):
        """
        Resets an active frequency sweep to the start frequency
         example : :SWE:RES
        :return:
        """
        self.specan.write(':SWE:RES')
        logging.info(':SWE:RES')
        time.sleep(0.1)


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
        time.sleep(0.1)
        self.specan.write('POW {}'.format(level_num))
        time.sleep(0.1)
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
        time.sleep(0.1)

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
        time.sleep(0.1)

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
        time.sleep(0.1)

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
        time.sleep(0.1)

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
        time.sleep(0.1)

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
        time.sleep(0.1)

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
        time.sleep(0.1)

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
        time.sleep(0.1)

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
        time.sleep(0.1)

    def set_modulation_modulation_standard_dvt(self, standard_type):
        """
        Sets the analog transmission standard or queries its setting
        The multi ATV predefined option
            Available DTV standards
            DTV standard  Required option  For details see
            DVB-T/H         R&S SFU-K1          "DVB-T/H"
            DVB-C           R&S SFU-K2          "DVB-C"
            DVB-S           R&S SFU-K3          "DVB-S"
            8VSB            R&S SFU-K4          "8VSB"
            J.83/B          R&S SFU-K5          "J.83/B"
            ISDB-T          R&S SFU-K6          "ISDB-T"
            DMB-T           R&S SFU-K7          "DMB-T"
            DVB-S2          R&S SFU-K8          "DVB-S2"
            DIRECTV         R&S SFU-K9          "DIRECTV"
            MEDIAFLO        R&S SFU-K10          "MediaFLO"
            T-DMB/DAB       R&S SFU-K11          "T-DMB/DAB"
            DTMB            R&S SFU-K12          "DTMB"
            CMMB            R&S SFU-K15          "CMMB"
            DVB-T2          R&S SFU-K16          "DVB-T2"
            DVB-C2          R&S SFU-K17          "DVB-C2"
            ATSC-M/H        R&S SFU-K18          "ATSC-M/H"
        example :
            DM:TRAN DIR
        :return:
        """
        self.specan.write('DM:TRAN {}'.format(standard_type))
        logging.info('DM:TRAN {}'.format(standard_type))
        time.sleep(0.1)

    def set_digitaltv_input_source(self, source_type):
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
        time.sleep(0.1)

    def set_digitaltv_coding_symbolrate(self, symbol_rate):
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
        time.sleep(0.1)

    def set_digitaltv_coding_constellation(self, constellation_type):
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
        time.sleep(0.1)

    def set_digitaltv_coding_fecframe(self, fecframe_type):
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
        time.sleep(0.1)

    def set_digitaltv_coding_pilots(self, fecframe_type):
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
        time.sleep(0.1)

    def set_digitaltv_coding_rolloff(self, rolloff_num):
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
        time.sleep(0.1)

    def set_digitaltv_coding_coderate(self, code_rate):
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
        time.sleep(0.1)

    def set_digitaltv_special_settings(self, setting_type):
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
        time.sleep(0.1)

    def set_digitaltv_phasenoise_phasenoise(self, phasenoise_type):
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
        time.sleep(0.1)

    def set_digitaltv_phasenoise_shape(self, shape_type):
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
        time.sleep(0.1)

    def set_digitaltv_phasenoise_magnitude(self, magnitude):
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
        time.sleep(0.1)

    def set_digitaltv_settings_tspacket(self, tspacket_type):
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
        time.sleep(0.1)

    def set_digitaltv_settings_pidpacket(self, pidpacket_type):
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
        time.sleep(0.1)

    def set_digitaltv_settings_pid(self, pid):
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
        time.sleep(0.1)

    def set_digitaltv_settings_payloadtest(self, payloadtest_type):
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
        time.sleep(0.1)

    def set_digitaltv_settings_prbs(self, prbs_type):
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
        time.sleep(0.1)

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
        time.sleep(0.1)


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
        time.sleep(0.1)

    def set_noise_noise_awgn(self, awgn_type):
        """
        Switches the Gaussian noise generator on or off.
        Only effective if "ADD" or "ONLY"

        not complete
            ON
            OFF
        example :
            NOIS:AWG ON
        :return:
        """
        self.specan.write('NOIS:AWG {}'.format(awgn_type))
        logging.info('NOIS:AWG {}'.format(awgn_type))
        time.sleep(0.1)

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
        time.sleep(0.1)

    def set_noise_awgn_ebno(self, ebno):
        """
        This function queries the noise Eb/N0 ratio
        example :
            NOISe:EN?
        :return:
        """
        self.specan.write('NOIS:EN {}'.format(ebno))
        logging.info('NOIS:EN {}'.format(ebno))
        time.sleep(0.1)










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
        self.specan.write('NOIS:AWG ON')


    def set_player_timing_openfile(self, file_path):
        """
        Select the file to be loaded into the TS player.
        example :
            TSG:CONF:PLAY "d:\tsgen\live\jump.trp"
        :return:
        """
        self.specan.write(r'TSG:CONF:PLAY "{}"'.format(file_path))
        logging.info(r'TSG:CONF:PLAY "{}"'.format(file_path))
        time.sleep(0.1)


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
    # specan.set_modulation_modulation_standard_dvt("DVB-T2")
    # specan.set_digitaltv_input_source("TSPL")
    # specan.set_digitaltv_coding_symbolrate("31.711e6")
    # specan.set_digitaltv_coding_constellation("S4")
    # specan.set_digitaltv_coding_fecframe("NORM")
    # specan.set_digitaltv_coding_rolloff("0.25")
    # specan.set_digitaltv_coding_coderate("R8_9")
    # specan.set_digitaltv_special_settings("ON")
    # specan.set_digitaltv_phasenoise_phasenoise("ON")
    # specan.set_digitaltv_phasenoise_shape("SHA3")
    # specan.set_digitaltv_phasenoise_magnitude("3")
    # specan.set_digitaltv_settings_packet("S187")
    # specan.set_digitaltv_settings_pidpacket("VAR")
    # specan.set_digitaltv_settings_pid("0001")
    # specan.set_digitaltv_settings_payloadtest("HFF")
    # specan.set_digitaltv_settings_prbs("P15_1")
    # specan.set_interferer_source("OFF")
    # specan.set_noise_noise_noise("OFF")
    # specan.set_noise_noise_awgn("ON")
    specan.set_noise_awgn_cn("45")
    # specan.set_cmd()


if __name__ == '__main__':
    # _test_code()
    pass
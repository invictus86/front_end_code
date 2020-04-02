import visa
import pyvisa
import time
# import VISAresourceExtentions


# -----------------------------------------------------------
# Initialization
# -----------------------------------------------------------
rm = pyvisa.ResourceManager()
specan = rm.open_resource('TCPIP::192.168.1.47::INSTR')

# try block to catch any InstrumentErrorException()

# specan.write_termination = '\n'
# specan.ext_clear_status()  # Clear instrument io buffers and status
# print specan.query('*IDN?')  # Query the Identification string
# specan.write('*RST;*CLS')  # Reset the instrument, clear the Error queue
# specan.write('INIT:CONT OFF')  # Switch OFF the continuous sweep
# specan.write('SYST:DISP:UPD ON')  # Display update ON - switch OFF after debugging
# specan.ext_error_checking()  # Error Checking after Initialization block
#
# # -----------------------------------------------------------
# # Basic Settings:
# # -----------------------------------------------------------
# specan.write('DISP:WIND:TRAC:Y:RLEV 10.0')  # Setting the Reference Level
# specan.write('FREQ:CENT 3.0 GHz')  # Setting the center frequency
# specan.write('FREQ:SPAN 200 MHz')  # Setting the span
specan.write('FREQ:CHAN:TABL:FREQ 5, 400 MHz')  # Setting the span
specan.write('FREQ:CHAN:TABL:FREQ 1, 400 MHz')  # Setting the span
# time.sleep(1)
# specan.write('FREQ:CHAN 5')  # Setting the span
# specan.write('BAND 100 kHz')  # Setting the RBW
# specan.write('BAND:VID 300kHz')  # Setting the VBW
# specan.write('SWE:POIN 10001')  # Setting the sweep points
# # -----------------------------------------------------------
# # SyncPoint 'SettingsApplied' - all the settings were applied
# # -----------------------------------------------------------
# specan.timeout = 2000  # Acquisition timeout in milliseconds - set it higher than the sweep time
# specan.write('INIT')  # Start the sweep
# # -----------------------------------------------------------
# specan.query('*OPC?')  # Using *OPC? query waits until the instrument finished the Acquisition
# specan.ext_error_checking()  # Error Checking
# # -----------------------------------------------------------
# # SyncPoint 'AcquisitionFinished' - the results are ready
# # -----------------------------------------------------------
# # Fetching the trace in ASCII format
# # -----------------------------------------------------------
# print('Fetching trace in ASCII format... ')
# traceASC = specan.query_ascii_values('FORM ASC;:TRAC? TRACE1')
# print 'ASCII data points read: {}'.format(len(traceASC))
# specan.ext_error_checking()  # Error Checking after the data transfer
# # -----------------------------------------------------------
# # Fetching the trace in Binary format
# # Transfer of traces in binary format is faster.
# # The traceBIN data and traceASC data are however the same.
# # -----------------------------------------------------------
# print('Fetching trace in binary format... ')
# traceBIN = specan.query_binary_values('FORM REAL;:TRAC? TRACE1')
# print 'Binary data points read: {}'.format(len(traceBIN))
# specan.ext_error_checking()  # Error Checking after the data transfer
# # -----------------------------------------------------------
# # Setting the marker to max and querying the X and Y
# # -----------------------------------------------------------
# specan.write('CALC1:MARK1:MAX')  # Set the marker to the maximum point of the entire trace
# specan.query('*OPC?')  # Using *OPC? query waits until the marker is set
# markerX = float(specan.query('CALC1:MARK1:X?'))
# markerY = float(specan.query('CALC1:MARK1:Y?'))
# print('Marker Frequency %0.1f Hz, Level %0.2f dBm\n' % (markerX, markerY))
# specan.ext_error_checking()  # Error Checking after the markers reading
# # -----------------------------------------------------------
# # Making an instrument screenshot and transferring the file to the PC
# # -----------------------------------------------------------
# print('Taking instrument screenshot and saving it to the PC... ')
# specan.write('HCOP:DEV:LANG PNG')
# specan.write('MMEM:NAME \'c:\\temp\\Dev_Screenshot.png\'')
# specan.write('HCOP:IMM')  # Make the screenshot now
# specan.query('*OPC?')  # Wait for the screenshot to be saved
# specan.ext_error_checking()  # Error Checking after the screenshot creation
# specan.ext_query_bin_data_to_file('MMEM:DATA? \'c:\\temp\\Dev_Screenshot.png\'', r'c:\Temp\PC_Screenshot.png')
# print('saved to PC c:\\Temp\\PC_Screenshot.png\n')
# specan.ext_error_checking()  # Error Checking after the screenshot save
# specan.ext_copy_pc_file_to_instrument(r'c:\Temp\PC_Screenshot.png', r'c:\temp\Dev_ScreenshotCopy.png')
# specan.ext_error_checking()  # Error Checking after the transfer



# stb_tester config
BANCH_ID = "ba709db"
STB_TESTER_URL = "http://192.168.1.154"
STB_TESTER_IP = "192.168.1.154"

# front_end server config
FRONT_END_SERVER_IP = "192.168.1.24"
FRONT_END_SERVER_PORT = 9999

# DVBS lock function config
DVB_S_LOCK_FUNCTION = ["tests/front_end_test/testcases.py::test_continuous_button_dsn5414a"]
DVB_S_CATEGORY = "auto_front_end_test"
DVB_S_REMOTE = "DSD4614iALM"

# DVBS2 lock function config
DVB_S2_LOCK_FUNCTION = ["tests/front_end_test/testcases.py::test_continuous_button_dsn5414a"]
DVB_S2_CATEGORY = "auto_front_end_test"
DVB_S2_REMOTE = "DSD4614iALM"

# DVBT lock function config
DVB_T_LOCK_FUNCTION = ["tests/front_end_test/testcases.py::test_continuous_button_dtn7414g"]
DVB_T_CATEGORY = "auto_front_end_test"
DVB_T_REMOTE = "DSD4614iALM"

# DVBT2 lock function config
DVB_T2_LOCK_FUNCTION = ["tests/front_end_test/testcases.py::test_continuous_button_dtn7414g"]
DVB_T2_CATEGORY = "auto_front_end_test"
DVB_T2_REMOTE = "DSD4614iALM"

# DVBC lock function config
DVB_C_LOCK_FUNCTION = ["tests/front_end_test/testcases.py::test_continuous_button_dcn7514i"]
DVB_C_CATEGORY = "auto_front_end_test"
DVB_C_REMOTE = "dcn7514i"

# DVBJ83 lock function config
DVB_J83_LOCK_FUNCTION = ["tests/front_end_test/testcases.py::test_continuous_button_dcn7514i"]
DVB_J83_CATEGORY = "auto_front_end_test"
DVB_J83_REMOTE = "dcn7514i"

# DVBT set serrch
DVB_T_SET_SEARCH_FUNCTION = ["tests/front_end_test/testcases.py::test_continuous_button_dtn7414g_set_search"]
DVB_T_SET_SEARCH_CATEGORY = "auto_front_end_test"
DVB_T_SET_SEARCH_REMOTE = "DSD4614iALM"

# DVBT set frequency bandwidth
DVB_T_SET_FREQUENCY_BANDWIDTH_FUNCTION = ["tests/front_end_test/testcases.py::test_continuous_button_dtn7414g_set_frequency_bandwidth"]
DVB_T_SET_FREQUENCY_BANDWIDTH_CATEGORY = "auto_front_end_test"
DVB_T_SET_FREQUENCY_BANDWIDTH_REMOTE = "DSD4614iALM"

# DVBT OCR fuunction
DVB_T_OCR_FUNCTION = ["tests/front_end_test/testcases.py::test_ocr_strength_quality_dtn7414g"]
DVB_T_OCR_CATEGORY = "auto_front_end_test"
DVB_T_OCR_REMOTE = "DSD4614iALM"

# DVBT2 set serrch
DVB_T2_SET_SEARCH_FUNCTION = ["tests/front_end_test/testcases.py::test_continuous_button_dtn7414g_set_search"]
DVB_T2_SET_SEARCH_CATEGORY = "auto_front_end_test"
DVB_T2_SET_SEARCH_REMOTE = "DSD4614iALM"

# DVBT2 set frequency bandwidth
DVB_T2_SET_FREQUENCY_BANDWIDTH_FUNCTION = ["tests/front_end_test/testcases.py::test_continuous_button_dtn7414g_set_frequency_bandwidth"]
DVB_T2_SET_FREQUENCY_BANDWIDTH_CATEGORY = "auto_front_end_test"
DVB_T2_SET_FREQUENCY_BANDWIDTH_REMOTE = "DSD4614iALM"

# DVBT2 OCR fuunction
DVB_T2_OCR_FUNCTION = ["tests/front_end_test/testcases.py::test_ocr_strength_quality_dtn7414g"]
DVB_T2_OCR_CATEGORY = "auto_front_end_test"
DVB_T2_OCR_REMOTE = "DSD4614iALM"

CAPTURE_NUM = 10
# ERR_MOSIC_NUM = 6
ERR_MOSIC_NUM = 8

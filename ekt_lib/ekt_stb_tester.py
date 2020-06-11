#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import ekt_cfg
import time
import os
import logging

current_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename='{}/ekt_log/ekt_stb_tester.log'.format(current_path),
                    filemode='a',  ##模式,有w和a,w就是写模式,每次都会重新写日志,覆盖之前的日志
                    # a是追加模式,默认如果不写的话,就是追加模式
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )

def stb_tester_execute_testcase(ip, banch_id, test_cases, category, remote):
    """
    detect motion or lock frequency using stb_tester
    :param ip:stb_tester_ip
    :param banch_id:test case banck id
    :param test_cases:test case item
    :param category:job category
    :param remote:RCU
    :return:
    """
    while True:
        try:
            res_status = requests.post(
                '{}/api/v1/run_tests'.format(ip),
                data=json.dumps({
                    "test_pack_revision": banch_id,
                    "test_cases": test_cases,
                    "category": category,
                    "remote_control": remote
                }))
            break
        except:
            time.sleep(60)
            print("stb_tester post Request error")
            logging.info("stb_tester post Request error")

    result = res_status.json()  # dict
    job_url = result.get("job_url")
    print (result)

    while True:
        while True:
            try:
                res = requests.get(job_url).json()
                break
            except:
                time.sleep(60)
                print("stb_tester get Request error")
                logging.info("stb_tester get Request error")

        # print res
        time.sleep(0.5)
        if res['status'] == "exited":
            fail_result = res.get("result_counts").get("fail")
            pass_result = res.get("result_counts").get("pass")
            if fail_result == 1 and pass_result == 0:
                return False
            elif fail_result == 0 and pass_result == 1:
                return True


if __name__ == '__main__':
    res = stb_tester_execute_testcase(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                   ["tests/front_end_test/testcases.py::test_recored"],
                                   "auto_front_end_test", "DSD4614iALM")
    print (res)

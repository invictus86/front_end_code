#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import time
import cv2
import numpy
import ekt_cfg


def stb_tester_detect_motion(ip, banch_id, test_cases, category, remote):
    """
    detect motion using stb_tester
    :param ip:stb_tester_ip
    :param banch_id:test case banck id
    :param test_cases:test case item
    :param category:job category
    :param remote:RCU
    :return:
    """
    res_status = requests.post(
        '{}/api/v1/run_tests'.format(ip),
        data=json.dumps({
            "test_pack_revision": banch_id,
            "test_cases": test_cases,
            "category": category,
            "remote_control": remote
        }))

    result = res_status.json()  # dict
    job_url = result.get("job_url")
    print result

    while True:
        res = requests.get(job_url).json()
        # print res
        # time.sleep(1)
        if res['status'] == "exited":
            fail_result = res.get("result_counts").get("fail")
            pass_result = res.get("result_counts").get("pass")
            if fail_result == 1 and pass_result == 0:
                return False
            elif fail_result == 0 and pass_result == 1:
                return True


if __name__ == '__main__':
    res = stb_tester_detect_motion(ekt_cfg.STB_TESTER_URL, ekt_cfg.BANCH_ID,
                                   ["tests/front_end_test/testcases.py::test_recored"],
                                   "auto_front_end_test", "DSD4614iALM")
    print res

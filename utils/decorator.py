# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/10/26 15:45
# @Author : masai
# @Email : sai.ma@spacexwalk.com
# @File : retry_decorator.py
# @Software: PyCharm
import time
import sys
import traceback


def retry_decorator(func):
    def inner(*args, **kwargs):
        counter = 0
        while True:
            counter += 1
            if counter > 3:
                print('Failed 3 times. Abort action.')
                break
            try:
                result = func(*args, **kwargs)
                return result
            except:
                ex_type, ex_value, ex_traceback = sys.exc_info()
                print(traceback.format_exc())
            time.sleep(2)
        return ex_value
    return inner
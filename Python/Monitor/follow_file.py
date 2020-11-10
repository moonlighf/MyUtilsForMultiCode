# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name         :  follow_file
# Description  :  实现如何实时监控一个文件，类似与linux中的tail -f功能
# Author       :  skymoon9406@gmail.com
# Date         :  2020/8/19
# -------------------------------------------------------------------------------
# --------------------------------设置工作路径------------------------------------#
import time
import sys
import os
CURRENT_PATH = os.path.split(os.path.realpath(__file__))[0]
PARENT_PATH = os.path.dirname(CURRENT_PATH)
sys.path.append(CURRENT_PATH)
sys.path.append(PARENT_PATH)
# --------------------------------导入模块和包------------------------------------#


def follow(the_file):
    """
    generator function that yields new lines in a file
    """
    # seek the end of the file
    the_file.seek(0, os.SEEK_END)
    # start infinite loop
    while True:
        # read last line of file
        line = the_file.readline()
        # sleep if file hasn't been updated
        if not line:
            time.sleep(0.02)
            continue
        yield line


if __name__ == '__main__':
    with open("/home/skymoon/monitor/123.log", "r") as log_file:
        log_lines = follow(log_file)
        # iterate over the generator
        for _line in log_lines:
            print(_line)

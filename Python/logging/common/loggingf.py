# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name         :  better_logging
# Description  :  读取配置文件生成日志相关配置
# Author       :  skymoon9406@gmail.com
# Date         :  2020/6/23
# -------------------------------------------------------------------------------
# --------------------------------设置工作路径------------------------------------#
import sys
import os
abspath = os.path.split(os.path.realpath(__file__))[0]
father_path = os.path.dirname(abspath)
sys.path.append(abspath)
sys.path.append(father_path)
# --------------------------------导入模块和包------------------------------------#
import json
import logging


def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


@singleton
class Logger:
    def __init__(self, logger_module, log_conf_path, log_file=None, log_error_file=None):
        self.logger = logging.getLogger(logger_module)
        with open(log_conf_path, "r") as config:
            logging_config = json.load(config)
            logging_config["handlers"]["info_file_handler"]["filename"] = log_file
            logging_config["handlers"]["error_file_handler"]["filename"] = log_error_file
            logging.config.dictConfig(logging_config)

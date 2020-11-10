# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name         :  GetLogging
# Description  :  日志封装类
# Author       :  skymoon9406@gmail.com
# Date         :  2020/7/2
# -------------------------------------------------------------------------------
# --------------------------------设置工作路径------------------------------------#
import sys
import os
abspath = os.path.split(os.path.realpath(__file__))[0]
father_path = os.path.dirname(abspath)
sys.path.append(abspath)
sys.path.append(father_path)
# --------------------------------导入模块和包------------------------------------#
import functools
from loguru import logger


class GetLogging:
    """
    日志配置
    """
    def __init__(self, error_log_file_path, info_log_file_path):
        # 错误日志
        logger.add(
            error_log_file_path,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {file}:{name}:{function}:{line} | {message}",
            filter=lambda x: True if x["level"].name == "ERROR" else False,
            rotation="00:00", retention="7 days", level='ERROR', encoding='utf-8', enqueue=True
        )
        # INFO日志
        logger.add(
            # os.path.join(father_path, "logs/{time:YYYY-MM-DD}.log"),
            info_log_file_path,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <5} | {file}:{name}:{function}:{line} | {message}",
            filter=lambda x: True if x["level"].name == "INFO" else False,
            rotation="00:00", retention="7 days", level='INFO', encoding='utf-8', enqueue=True
        )
        self.logger = logger

    def get(self):
        return self.logger

    @staticmethod
    def logger_wraps(*, entry=True, exit=True, level="INFO"):

        def wrapper(func):
            name = func.__name__

            @functools.wraps(func)
            def wrapped(*args, **kwargs):
                logger_ = logger.opt(depth=1)
                if entry:
                    logger_.log(level, "Entering '{}' (args={}, kwargs={})", name, args, kwargs)
                result = func(*args, **kwargs)
                if exit:
                    logger_.log(level, "Exiting '{}' (result={})", name, result)
                return result

            return wrapped

        return wrapper


if __name__ == '__main__':
    _client = GetLogging("./logs/a.log", "./b.log")
    lg = _client.get()
    # 普通日志输出
    lg.info("niasjidaj{}-----{}", "爱仕达", "asdazzzz")
    # 错误ERROR的输出
    try:
        a = 3
        b = 0
        c = a/b
    except:
        lg.exception("ca")
        print(412)
    # 作为魔法函数跟踪进入函数的参数和输出的值
    @_client.logger_wraps(level="INFO")
    def foo(a, b, c):
        lg.info("Inside the function")
        return a * b * c


    def bar():
        foo(2, 4, c=8)

    bar()

# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name         :  MonitorFile
# Description  :  利用watchdog模块实现的文件监控，并且输出最后一行
# Author       :  skymoon9406@gmail.com
# Date         :  2020/10/10
# -------------------------------------------------------------------------------
# --------------------------------设置工作路径------------------------------------#
import os
import time

from loguru import logger
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


class MonitorHandler(PatternMatchingEventHandler):
    def __init__(self, _watch_patterns, _ignore_patterns, _ignore_directories, _case_sensitive,
                 _filename):
        super(MonitorHandler, self).__init__()
        self._patterns = _watch_patterns
        self._ignore_patterns = _ignore_patterns
        self._ignore_directories = _ignore_directories
        self._case_sensitive = _case_sensitive
        # 如果针对指定文件进行监控并且输出修改内容需要指定
        self._filename = _filename

    @staticmethod
    def get_file_last_line(input_file):
        file_size = os.path.getsize(input_file)
        block_size = 1024
        with open(input_file, 'r') as f:
            last_line = ""
            if file_size > block_size:
                max_seek_point = (file_size // block_size)
                f.seek((max_seek_point - 1) * block_size)
            elif file_size:
                f.seek(0, 0)
            lines = f.readlines()
            if lines:
                lineno = 1
                while last_line == "":
                    last_line = lines[-lineno].strip()
                    lineno += 1
            return last_line

    def on_created(self, event):
        logger.info("{}被创建", event.src_path)

    def on_deleted(self, event):
        logger.info("{}被删除", event.src_path)

    def on_modified(self, event):
        realpath = os.path.realpath(event.src_path)
        (_, filename) = os.path.split(realpath)
        # extend_type = os.path.splitext(realpath)[1]
        if filename == self._filename:
            logger.info("{}被修改", event.src_path)
            logger.info(self.get_file_last_line(realpath))

    def on_moved(self, event):
        logger.info("{}被移动到{}", event.src_path, event.dest_path)


class ScanFileOrFolder:
    def __init__(self, watch_patterns, ignore_patterns, ignore_directories,
                 case_sensitive, watch_path, go_recursively, file_name):
        """
        :param watch_patterns:      监控文件的模式，输入为列表形式     ["*.py", "*.txt", "*.log"]
        :param ignore_patterns:     忽略的文件模式，输入为列表形式     [] / ["*.tmp"]
        :param ignore_directories:  是否忽略文件夹变化               True/False
        :param case_sensitive:      是否对大小写敏感                 True/False
        :param watch_path:          监控文件夹目录
        :param go_recursively:      是否监控子文件夹                 True/False
        :param file_name:           是否监控指定文件，如果是则直接指定文件名，否则赋值为空字符串
        """
        self.my_observer = Observer()
        self.my_observer.schedule(
            MonitorHandler(watch_patterns, ignore_patterns, ignore_directories, case_sensitive,
                           file_name), watch_path, recursive=go_recursively)

    def stop(self):
        # 关闭监控
        self.my_observer.stop()
        self.my_observer.join()

    def start(self):
        self.my_observer.start()


if __name__ == '__main__':
    _watch_patterns = ["*.py", "*.txt", "*.log"]   # 监控文件的模式
    _ignore_patterns = ["*.tmp"]  # 设置忽略的文件模式
    _ignore_directories = True  # 是否忽略文件夹变化
    _case_sensitive = True  # 是否对大小写敏感
    _watch_path = "/home/skymoon/NewWork/01.TmNewProject/test/未命名文件夹"  # 监控目录
    _go_recursively = True  # 是否监控子文件夹
    _file_name = "abc.log"
    _client = ScanFileOrFolder(_watch_patterns,
                               _ignore_patterns,
                               _ignore_directories,
                               _case_sensitive,
                               _watch_path,
                               _go_recursively,
                               _file_name)
    _client.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        _client.stop()

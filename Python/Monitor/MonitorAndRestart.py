# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name         :  MonitorAndRestart
# Description  :  监控是否日志文件仍在写入，如果没有写入则重启天猫实时抓取流程
# Author       :  skymoon9406@gmail.com
# Date         :  2020/10/10
# -------------------------------------------------------------------------------
# --------------------------------设置工作路径------------------------------------#
import sys
import os

CURRENT_PATH = os.path.split(os.path.realpath(__file__))[0]
PARENT_PATH = os.path.dirname(CURRENT_PATH)
sys.path.append(CURRENT_PATH)
sys.path.append(PARENT_PATH)
# --------------------------------导入模块和包------------------------------------#
import time
from loguru import logger


class MonitorAndRestart:
    def __init__(self, file_path, restart_py_path, monitor_process_word, log_file_path):
        # 初始化要监控的文件
        self.log_file_handle = self.init_follow_file(file_path)

        # 设置初始的时间
        self.cur_time = time.time()

        # 需要重启的脚本路径和检测进程使用的关键词
        self.restart_py_path = restart_py_path
        self.monitor_process_word = monitor_process_word

        # 重启脚本的日志路径
        self.log_file_path = log_file_path

    @staticmethod
    def init_follow_file(file_path):
        if os.path.exists(file_path) is False:
            with open(file_path, "w") as _:
                pass
        log_file_handle = open(file_path, "r")
        return log_file_handle

    def restart_process(self):
        restart_code = "nohup /home/work/anaconda3/envs/pyf/bin/python {} >{} 2>&1 &".format(
            self.restart_py_path, self.log_file_path)
        os.popen(restart_code)
        logger.info("success restart {}", str(restart_code))

    def kill_process(self):
        lines = os.popen("ps -ef|grep {}".format(self.monitor_process_word))
        for line in lines:
            # 跳过本身的查找进程
            if line.find('grep {}'.format(self.monitor_process_word)) != -1:
                continue
            # 找到进程号
            params = line.split()
            pid = params[1]
            # 获取该进程的描述
            proc = ''.join(params[7:])
            # 杀死该进程
            out = os.system('kill ' + pid)
            if out == 0:
                logger.info("success! kill {} -- {}", str(pid), str(proc))
            else:
                logger.info("failed! kill {} -- {}", str(pid), str(proc))

    def follow(self, the_file):
        the_file.seek(0, os.SEEK_END)
        while True:
            delta = time.time() - self.cur_time
            # 如果时间大于10分钟，则退出程序
            if delta > 5 * 60:
                # 关闭文件句柄
                self.log_file_handle.close()
                # 杀死待重启的进程
                self.kill_process()
                # 重新启动脚本
                self.restart_process()
                # 退出程序
                sys.exit(0)
            line = the_file.readline()
            if not line:
                time.sleep(0.02)
                continue
            yield line

    def start(self):
        log_lines = self.follow(self.log_file_handle)
        for line in log_lines:
            logger.info(line)
            # 更新此时的时间
            self.cur_time = time.time()


if __name__ == '__main__':
    _monitor_log_file = ""
    _restart_py_path = ""
    _monitor_process_word = ""
    _log_file_path = ""
    MonitorAndRestart(
        file_path=_monitor_log_file,
        restart_py_path=_restart_py_path,
        monitor_process_word=_monitor_process_word,
        log_file_path=_log_file_path
    ).start()

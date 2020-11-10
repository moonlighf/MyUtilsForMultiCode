# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name         :  SSHConnection
# Description  :  封装后的远程和本地文件互相操作
# Author       :  skymoon9406@gmail.com
# Date         :  2020/10/22
# -------------------------------------------------------------------------------
# --------------------------------设置工作路径------------------------------------#
import paramiko
import sys
import os

CURRENT_PATH = os.path.split(os.path.realpath(__file__))[0]
PARENT_PATH = os.path.dirname(CURRENT_PATH)
sys.path.append(CURRENT_PATH)
sys.path.append(PARENT_PATH)
# --------------------------------导入模块和包------------------------------------#


# noinspection PyTypeChecker
class SSHConnection:
    # 初始化连接创建Transport通道
    def __init__(self, host='xxx.xxx.xxx.xxx', port=22, user='xxx', pwd='xxxxx'):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.__transport = paramiko.Transport((self.host, self.port))
        self.__transport.connect(username=self.user, password=self.pwd)
        self.sftp = paramiko.SFTPClient.from_transport(self.__transport)

    # 关闭通道
    def close(self):
        self.sftp.close()
        self.__transport.close()

    # 上传文件到远程主机
    def upload(self, local_path, remote_path):
        self.sftp.put(local_path, remote_path)

    # 从远程主机下载文件到本地
    def download(self, local_path, remote_path):
        self.sftp.get(remote_path, local_path)

    # 在远程主机上创建目录
    def mkdir(self, target_path):
        self.sftp.mkdir(target_path)

    # 删除远程主机上的目录
    def rmdir(self, target_path):
        self.sftp.rmdir(target_path)

    # 查看目录下文件以及子目录（如果需要更加细粒度的文件信息建议使用listdir_attr）
    def listdir(self, target_path):
        return self.sftp.listdir(target_path)

    # 删除文件
    def remove(self, target_path):
        self.sftp.remove(target_path)

    # 查看目录下文件以及子目录的详细信息（包含内容和参考os.stat返回一个FSTPAttributes对象，对象的具体属性请用__dict__查看）
    def list_dir_attr(self, target_path):
        try:
            dir_list = self.sftp.listdir_attr(target_path)
        except BaseException as e:
            print(e)
            sys.exit(-1)
        return dir_list

    # 获取文件详情
    def stat(self, remote_path):
        return self.sftp.stat(remote_path)

    # 判断远程文件是否存在，如果不存在则创建
    def judge_and_mkdir(self, remote_path):
        try:
            self.stat(remote_path)
            print("dir path exist")
        except IOError:
            self.mkdir(remote_path)

    # SSHClient输入命令远程操作主机
    def cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh._transport = self.__transport
        stdin, stdout, stderr = ssh.exec_command(command)
        result = stdout.read()
        print(result)
        return result


if __name__ == '__main__':
    host_ip = ''  # 远程服务器IP
    host_port =   # 远程服务器端口
    host_username = ''  # 远程服务器用户名
    host_password = ''  # 远程服务器密码
    _ssh = SSHConnection(host=host_ip, user=host_username, pwd=host_password)
    # 判断远程文件夹是否存在
    try:
        a = _ssh.stat(
            "/home/skymoon/NewWork/06.ProductDefinition/eagle_tags_analyse/results")
        print("exist")
    except IOError:
        print("not exist")

    # # 遍历本地文件
    # source_path = '/home/work/fuzheng/22.commentAndEagleModel/eagle_tags_analyse/results/'
    # t_path = '/home/skymoon/NewWork/06.ProductDefinition/eagle_tags_analyse/results/'
    # source_files = os.listdir(source_path)
    # for file in source_files:
    #     # 判断后缀是否是 指定后缀
    #     if ".xlsx" in file:
    #         local_file = source_path + file
    #         remote_file = t_path + file
    #         # 本地文件推送到远程
    #         _ssh.upload(local_file, remote_file)

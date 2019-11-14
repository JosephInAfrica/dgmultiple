#!encoding=utf8

"for dataCenter initialization problems."
from codes.status_light import purify_light
import os
from setting import setting
from loggers import rlog, elog
import json


def recover_host(dataCenter):

    # 尝试recover:如果没有文件，就建一个新文件。
    if not os.path.exists(setting.backup_host):
        with open(setting.backup_host, 'w') as file:
            file.write("")
        rlog("没有找到远程平台备份")
        return

    with open(setting.backup_host, 'r') as file:
        try:
            file = file.read()
            print("file read===>", file)
            dataCenter.host = json.loads(file)
            print("成功载入上位机缓存")
            print(dataCenter.host)
        except Exception as e:
            print("没有载入上位机缓存==>")
            print(e)


def recover_light(dataCenter):
    # 尝试recover:如果没有文件，就建一个新文件。
    if not os.path.exists(setting.backup_light):
        with open(setting.backup_light, 'w') as file:
            file.write("")
        rlog("没有找到远程平台备份")
        return

    with open(setting.backup_light, 'r') as file:
        try:
            dataCenter.vanila_light = purify_light(json.loads(file.read()))
            print("成功载入灯光缓存")
            print(dataCenter.vanila_light)
        except Exception as e:
            print("没有载入灯光缓存==>")
            print(e)


def recover_blink(dataCenter):
    # 尝试recover:如果没有文件，就建一个新文件。
    if not os.path.exists(setting.backup_blink):
        with open(setting.backup_blink, 'w') as file:
            file.write("")
        rlog("没有找到闪灯频率的备份")
        return

    with open(setting.backup_blink, 'r') as file:
        try:
            self.blink_freq = json.loads(file.read())
            print("成功载入闪灯频率")
            print(self.blink_freq)
        except Exception as e:
            print("没有载入闪灯频率==>")
            elog(e)

#!encoding=utf8
# 这个模块用来handle网络设置。 解析设置文件，输出设置文件，应用设置。
from tornado import template
import re
import os
from setting import setting,get_network_config,conf,save_conf
from loggers import elog, elogger,rlog

network_temp = template.Template('''
# !/bin/sh -e
ifconfig eth1 {{address}}
ifconfig eht1 netmask {{netmask}} 
route add default gw {{gateway}}
dns = 'nameserver {{dns}}'
sed - i '2c '"$dns"'' /etc/resolv.conf
ntpdate cn.ntp.org.cn
cp /usr/share/zoneinfo/Asia/Hong_Kong/etc/localtime
''')


def set_network_config(kwargs):
    '''接收一个dict, 如{'netmask': '255.255.255.0', 'gateway': '192.168.0.1', 'address': '192.168.0.199'}。将其写入 / etc / network / interfaces'''
    old_config = get_network_config()
    try:
        old_ip, old_netmask, old_gateway, old_dns = old_config
    except Exception as e:
        old_ip, old_netmask, old_gateway, old_dns = "", "", "", ""
        rlog("failed to get old data")

    address = kwargs.get('address')
    netmask = kwargs.get('netmask')
    gateway = kwargs.get('gateway')
    dns = kwargs.get('dns')

    if not (is_valid(netmask) and is_valid(gateway) and is_valid(address) and is_valid(dns)):
        elog("invalid config")
        # 检测三个数据都不为空。

    to_write = network_temp.generate(**kwargs)

    with open(setting.ip_config, 'w') as file:
        file.write(to_write)
    os.system("sync")



def set_hardware_config(dic):
    for key,value in dic.items():
        conf.set("hardware",key,value)
    save_conf()
    os.system("sync")

def get_hardware_config():
    return dict(conf.items("hardware"))


def is_valid(address):
    "check is ip mask gate is valid 4 "
    print("data under check==>", address)
    try:
        digits = address.split(".")
        if len(digits) != 4:
            return 0
        for digit in digits:
            if not (int(digit) >= 0 and int(digit) <= 255):
                return 0

    except Exception as e:
        rlog(e)
        return 0
    return 1

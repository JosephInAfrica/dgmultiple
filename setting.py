#!encoding=utf8
import os
import logging
import logging.handlers
from os.path import abspath, dirname, join
import re
import json
from ConfigParser import ConfigParser

color16 = {0: "00", 1: "00", 2: "06", 3: "01",4:"02",5:"0D",6:"08",7:"09",8:"04",9:"03",10:"05",11:"07",12:"0B",13:"0A",14:"0C",15:"0E"}

color4={0: "06", 1: "01", 2: "0D", 3: "08"}
basedir = abspath("/home/root/")
ip_config = join(basedir, "ip.sh")
user_config=join(basedir,"default.conf")


def get_user_config():
    with open(user_config,'r') as file:
        d=json.loads(file.read())
    return d
    # d=json.loads(user_conf)

def get_network_config():
    "从系统中读取到配置文件"
    def parse(file):
        import re
        ip_ = re.compile("\d+\.\d+\.\d+\.\d+")
        with open(file, 'r') as file:
            lines = file.readlines()

        ips = [re.findall(ip_, line) for line in lines]
        ips = [ip[0] for ip in ips if ip]
        ip, netmask, gateway, dns = ips

        return dict(address=ip, netmask=netmask, gateway=gateway, dns=dns)
    print("get_network_config is called!!!!\n\n")
    return parse(ip_config)

class BaseConfig:
    network=get_network_config()

    backup_light = join(basedir, "backup_light.json")
    backup_status = join(basedir, "backup_status.json")
    backup_blink = join(basedir, "backup_blinkfreq.json")
    backup_lightcodes = join(basedir, "backup_lightcodes.json")
    backup_host = join(basedir, "backup_host.json")
    logsdir = join(basedir, "logs")
    # 有几节模块。设置多于实际节数也能用。但效率稍有影响。因为会尝试读不存在设备的地址.
    # 腾讯要求只允许4种状态码。超出报相应错。状态码限定数量。
    # 是否全部上线才下发灯效。推荐是。
    regular_log = join(logsdir, "regular.log")
    error_log = join(logsdir, "error.log")
###

    ip_config=ip_config


# 调试
     # for_tencnet值0,1分别代表模块和标签的id按腾讯的要求加工/采用原始数据。
    for_tencent=0
    upload = 1
    heart_beat = 1
    light_range = range(16)
    color_map=color16

    allow_temp_failure = 0
    allow_enquiry_fail=2

    url_status = "/status"
    url_heartbeat = "/heartbeat"
    url_temp="/temp"
    request_timeout=5
    all_loaded_required = True
###
# 自检参照 按实际情况配置 应该可以导入文件 web api
    module_amount = 1
    u_count=52
    temp_amount=3
    heartbeat_interval = 20
    write_bunch=10
    write_delay=0
    # write_interval=0.6
    # 写灯光命令时，每写write_bunch个，就读一次stroke。避免长时间阻塞。

class TencentConfig(BaseConfig):
    for_tencent=1
    upload = 0
    heart_beat = 0
    module_amount = 4
    color_map=color4
    light_range = range(4)
    all_loaded_required = True


class Test72(BaseConfig):
    module_amount = 1
    u_count=52
    temp_amount=3

    # 每个模块温湿度模块个数

class Test77(BaseConfig):
    module_amount = 1
    u_count=52
    temp_amount=3
    all_loaded_required = False

class Test71(BaseConfig):
    module_amount = 4
    u_count=52
    temp_amount=3
    color_map=color4
    light_range = range(4)
    # 每个模块温湿度模块个数

class setting(Test71):
    pass


tornado_setting = dict(
    template_path=os.path.join(os.path.dirname(__file__), "http_server", "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "http_server", "static"),
    cookie_secret="ahardtoguessstring",
    static_url_prefix="/static/",
    login_url="/login",
)

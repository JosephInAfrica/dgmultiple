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

color={16:color16,4:color4}

conf=ConfigParser()
conf.read(user_config)

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

class setting:
    network=get_network_config()
    backup_light = join(basedir, "backup_light.json")
    backup_status = join(basedir, "backup_status.json")
    backup_blink = join(basedir, "backup_blinkfreq.json")
    backup_lightcodes = join(basedir, "backup_lightcodes.json")
    backup_host = join(basedir, "backup_host.json")
    logsdir = join(basedir, "logs")
    regular_log = join(logsdir, "regular.log")
    error_log = join(logsdir, "error.log")
    code_log = join(logsdir, "code.log")
    ip_config=ip_config
    # for_tencnet值0,1分别代表模块和标签的id按腾讯的要求加工/采用原始数据。
    for_tencent=0
    upload = 1
    heart_beat = 1
    light_range = range(16)

    allow_temp_failure = 0
    allow_enquiry_fail=2

    url_status = "/status"
    url_heartbeat = "/heartbeat"
    url_temp="/temp"
    all_loaded_required = True
    write_bunch=10
    write_delay=0

# 自检参照 按实际情况配置 应该可以导入文件 web api
    color_map=color.get(int(conf.get("mechanics","lightcolor")))
    light_range=range(int(conf.get("mechanics","lightcolor")))
    module_amount = int(conf.get("hardware","module_amount")) or 1
    u_count=int(conf.get("hardware","u_count")) or 52
    temp_amount=int(conf.get("hardware","temp_amount")) or 3
    heartbeat_interval = int(conf.get("mechanics","heartbeat_interval")) or 20
    request_timeout=int(conf.get("mechanics","request_timeout")) or 5
    all_loaded_required=int(conf.get("mechanics","all_loaded_required")) or 1
    
tornado_setting = dict(
    template_path=os.path.join(os.path.dirname(__file__), "http_server", "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "http_server", "static"),
    cookie_secret="ahardtoguessstring",
    static_url_prefix="/static/",
    login_url="/login",
)

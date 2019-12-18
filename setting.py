#!encoding=utf8
import os
import logging
import logging.handlers
from os.path import abspath, dirname, join
import re
import json
from ConfigParser import ConfigParser
import re
color16 = {0: "00", 1: "00", 2: "06", 3: "01",4:"02",5:"0D",6:"08",7:"09",8:"04",9:"03",10:"05",11:"07",12:"0B",13:"0A",14:"0C",15:"0E"}

color4={0: "06", 1: "01", 2: "0D", 3: "08"}
basedir = abspath("/home/root/")
ip_config = join(basedir, "ip.sh")
user_config=join(basedir,"default.conf")

color={16:color16,4:color4}

conf=ConfigParser()
conf.read(user_config)

def save_conf():
    with open(user_config,"wb") as file:
        conf.write(file)


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


def get_mac(dir):
    if not os.path.isdir(dir):
        os.system("ifconfig eth1 > /tmp/mac.txt")

    
    with open(dir,"r") as file:
        para=file.read()
    # except IOError:

        
    e=re.compile(r"HWaddr\s+([0-9a-f:]+)")
    c=re.findall(e,para)[0]
    c=c.replace(":","")
    return c.decode("hex")


class Setting(object):
    backup_light = join(basedir, "backup_light.json")
    backup_blink = join(basedir, "backup_blinkfreq.json")
    backup_lightcodes = join(basedir, "backup_lightcodes.json")
    backup_host = join(basedir, "backup_host.json")
    logsdir = join(basedir, "logs")
    mac_dir="/tmp/mac.txt"
    regular_log = join(logsdir, "regular.log")
    error_log = join(logsdir, "error.log")
    code_log = join(logsdir, "code.log")
    parse_log = join(logsdir, "parse.log")
    ip_config=ip_config

    # for_tencnet值0,1分别代表模块和标签的id按腾讯的要求加工/采用原始数据。
    for_tencent=1
    upload = 0
    allow_temp_failure =5
    allow_enquiry_fail=3
    allow_write_enquiry_fail=3

    write_bunch=10
    write_delay=0

# 自检参照 按实际情况配置 应该可以导入文件 web api
    color_map=color.get(int(conf.get("mechanics","lightcolor")))
    light_range=range(int(conf.get("mechanics","lightcolor")))


    def set(self,column,key,value):
        conf.set(column,key,value)

    @property
    def url_status(self):
        return conf.get("upstream","status")


    @property
    def url_heartbeat(self):
        return conf.get("upstream","heartbeat")
        
    @property
    def get(module,key):
        return conf.get(module,key)

    @property
    def url_temp(self):
        return conf.get("upstream","temp")

    @property
    def self_ip(self):
        return conf.get("network","address")

    @property
    def self_netmask(self):
        return conf.get("network","netmask")

    @property
    def self_gateway(self):
        return conf.get("network","gateway")

    @property
    def self_dns(self):
        return conf.get("network","dns")

    @property
    def network(self):
        return dict(address=self.self_ip,netmask=self.self_netmask,gateway=self.self_gateway,dns=self.self_dns)

    @property
    def blink_freq(self):
        return conf.get("mechanics","blink_freq")

    @property
    def upstream_host(self):
        return conf.get("upstream","host")

    @property
    def module_amount(self):
        return int(conf.get("hardware","module_amount"))

    @property
    def u_count(self):
        return int(conf.get("hardware","u_count"))

    @property
    def temp_amount(self):
        return int(conf.get("hardware","temp_amount"))

    @property
    def heartbeat_interval(self):
        return int(conf.get("mechanics","heartbeat_interval"))

    @property
    def request_timeout(self):
        return int(conf.get("mechanics","request_timeout"))

    @property
    def all_loaded_required(self):
        return int(conf.get("mechanics","all_loaded_required"))

   
tornado_setting = dict(
    template_path=os.path.join(os.path.dirname(__file__), "http_server", "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "http_server", "static"),
    cookie_secret="ahardtoguessstring",
    static_url_prefix="/static/",
    login_url="/login",
)


setting=Setting()

print("heartbeat interval,",setting.heartbeat_interval)
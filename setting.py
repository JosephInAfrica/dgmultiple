#!encoding=utf8
import os
import logging
import logging.handlers
from os.path import abspath, dirname, join
import re

color16 = {0: "00", 1: "00", 2: "06", 3: "01",4:"02",5:"0D",6:"08",7:"09",8:"04",9:"03",10:"05",11:"07",12:"0B",13:"0A",14:"0C",15:"0E"}

color4={0: "06", 1: "01", 2: "0D", 3: "08"}
basedir = abspath("/home/root/")
ip_config = join(basedir, "ip.sh")
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

    # for_tencnet值0,1分别代表模块和标签的id按腾讯的要求加工/采用原始数据。
    network=get_network_config()
    for_tencent=0
    # 是否上传数据到数据平台。
    upload = 1
    # 是否上传心跳。
    ip_config=ip_config
    heart_beat = 1
    # 有几节模块。设置多于实际节数也能用。但效率稍有影响。因为会尝试读不存在设备的地址.
    module_amount = 1
    # 腾讯要求只允许4种状态码。超出报相应错。状态码限定数量。
    light_range = range(16)
    # 是否全部上线才下发灯效。推荐是。
    all_loaded_required = True
    color_map=color16
    # 全部掉线后是否延时加载。
    lazy_recover=True
    # 全部掉线后，delay多少秒重读数据。
    resume_delay=24
    # 心跳间隔。
    heartbeat_interval = 20
    basedir = abspath("/home/root/")
    logsdir = join(basedir, "logs")
    # ip_config = join(basedir, "ip.sh")
    backup_light = join(basedir, "backup_light.json")
    backup_status = join(basedir, "backup_status.json")
    backup_blink = join(basedir, "backup_blinkfreq.json")
    backup_lightcodes = join(basedir, "backup_lightcodes.json")
    backup_host = join(basedir, "backup_host.json")
    # 允许温湿度读取失败多少次.
    allow_temp_failure = 20

    # 是否心跳。
    # 与数据平台对接：数据平台接收update和heartbeat相应uri.
    url_status = "/status"
    url_heartbeat = "/heartbeat"
    url_temp="/temp"
    regular_log = join(logsdir, "regular.log")
    uvariation_log = join(logsdir, "uvariation.log")
    error_log = join(logsdir, "error.log")
    temp_amount=6
    temp_hum_nos = [(10, 11, 12), (13, 14, 15)]
    interval = 0.6
    write_interval=1.2
    write_repeat=2
    # 写灯光命令时，每写write_bunch个，就读一次stroke。避免长时间阻塞。
    write_bunch=10
    # 写命令
    startup_delay=6
    # 当所有模块都掉线时，多长时间以后重新检测。
    # 上传超时时间
    request_timeout=3

    # 每个模块温湿度模块个数

class RegularConfig(BaseConfig):
    for_tencent=0
    upload = 1
    heart_beat = 1
    module_amount = 1
    light_range = range(16)
    color_map=color16
    all_loaded_required = True
    lazy_recover=True


class TencentConfig(BaseConfig):
    for_tencent=0
    upload = 1
    heart_beat = 1
    module_amount = 4
    color_map=color4
    light_range = range(4)
    all_loaded_required = True
    lazy_recover=True


class TestConfig(BaseConfig):
    for_tencent=0
    upload = 1
    heart_beat = 1
    module_amount = 1
    color_map=color16
    light_range = range(16)
    all_loaded_required = False
    lazy_recover=False
    temp_amount=1
    # 每个模块温湿度模块个数

class setting(TestConfig):
    pass


tornado_setting = dict(
    template_path=os.path.join(os.path.dirname(__file__), "http_server", "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "http_server", "static"),
    cookie_secret="ahardtoguessstring",
    static_url_prefix="/static/",
    login_url="/login",
)

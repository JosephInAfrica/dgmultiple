#!encoding=utf8
# 与qt 和 云端的数据交换接口。 转换数据。
#!encoding=utf8
from setting import setting
import os
import json
import urllib2
from setting import setting
from loggers import elogger, rlogger, rlog, elog
from tornado.gen import coroutine
import os
from codes.status_light import status_light, treat_post,from_light_to_codes, from_light_to_executables
from codes.blink_freq import parse as parse_blink
from codes.temp_hum import temp_hum
from startup import recover_host, recover_light, recover_blink
from configInterface import get_network_config


class DataCenter(dict):
    #  这是为了单例模式。
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataCenter, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    _instance = None
    vanila_status = {}
    vanila_light = {}
    blink_freq = {}
    temp = {}
    temp_failure_count = {}
    codes_for_recovery = []
    registered_modules = set()
    host = ""
    # host is ip for remote data cloud.
    last_enquiry = {}
    network = {}

    def __init__(self):
        print("尝试初始化数据中心")
        recover_light(self)
        recover_host(self)
        recover_blink(self)
        self.network = get_network_config()
        print("network", self.network)

    def parse_blink_freq(self, data):
        print("trying to parse data", data)
        return parse_blink(self.vanila_status, data)

    @property
    def online_light(self):
        light = {}
        for key in self.vanila_light.keys():
            if key in self.vanila_status.keys():
                light[key] = self.vanila_light[key]
        return light


    @property
    def light_codes(self):
        return from_light_to_codes(self.vanila_light)

    @property
    def to_upload(self):
        return {self.network.get("address"): {"status":self.vanila_status, "light": self.vanila_light}}

    @property
    def commands(self):
        "这是用来恢复灯光的。不在线的就不管了。"
        return from_light_to_executables(self.online_light, self.vanila_status)



    @property
    def all_loaded(self):
        if len(self.vanila_status)==0:
            return False
        for content in self.vanila_status.values():
            if not content.get("u_count") >= 42:
                return False
        return True

    def parse_blink(self):
        pass

    @property
    def temp_hum(self):
        return temp_hum(self.vanila_status)

    @property
    def online_modules(self):
        return self.vanila_status.keys()

    @property
    def partly_online(self):
        return len(self.online_address)<setting.module_amount and len(self.online_address)>0

    @property
    def online_address(self):
        return [item.get("address") for item in self.vanila_status.values()]

    def save(self):
        self.save_light()
        self.save_blink()

    def save_host(self):
        with open(setting.backup_host, "w") as file:
            # set is not serializable. It need to be converted to list.
            print("hosts to save in file===>")
            print(json.dumps(self.host))
            file.write(json.dumps(self.host))
            try:
                os.system("sync")
                print("hosts to notify saved==>", self.host)
            except:
                pass

    def save_blink(self):
        with open(setting.backup_blink, "w") as file:
            file.write(json.dumps(self.blink_freq))
            try:
                os.system("sync")
                print("saved==>", self.blink_freq)
            except:
                pass

    def save_light(self):
        with open(setting.backup_light, 'w') as file:
            file.write(json.dumps(self.vanila_light))
            try:
                os.system("sync")
                print("saved==>", self.vanila_light)
            except:
                pass

    @property
    def json_tencent_status(self):
        # 把现有数据转化成api的样子。
        models = self.vanila_status
        light = self.vanila_light
        registered_modules = self.registered_modules
        return status_light(models, light, registered_modules)

    def parse_setting(self, dic):
        "将腾讯的设置json解析为两层dict."
        result = treat_post(dic, self.vanila_light, self.vanila_status, light_range=setting.light_range)
        # print("vanila_light:", self.vanila_light)
        return result


dataCenter = DataCenter()

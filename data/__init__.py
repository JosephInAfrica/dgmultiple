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
from .output import new_status as _new_status,new_temp as _new_temp,new_light as _new_light

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
    vanila_temp={}
    blink_freq = {}
    temp = {}
    temp_failure_count = {}
    codes_for_recovery = []
    # 目前设定为map,key是module_id,value是u_amount
    registered_modules = {}
    host = ""
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


    # @property
    # def new_online_light(self):
    #     light={}
    #     for key in self.new_vanila_light.keys():

    def reonline_light_commands(self,reon_modules):
        "这是用来恢复灯光的。不在线的就不管了。"
        light={}
        for key in self.vanila_light.keys():
            if key not in reon_modules:
                continue
            if key in self.vanila_status.keys():
                light[key] = self.vanila_light[key]

        return from_light_to_executables(light, self.vanila_status)

    @property
    def light_codes(self):
        return from_light_to_codes(self.vanila_light)

    @property
    def new_status(self):
        return _new_status(self.vanila_status)


    @property
    def new_temp(self):
        return _new_temp(self.vanila_temp)

    @property
    def new_light(self):
        return _new_light(self.vanila_light)


    @property
    def status(self):
        
        return {self.network.get("address"): {"status":self.vanila_status, "light": self.vanila_light}}

    # @property
    # def to_upload(self):
    #     return {self.network.get("address"): {"status":self.vanila_status, "light": self.vanila_light}}

    @property
    def status_to_upload(self):
        return {self.network.get("address"): self.vanila_status}

    @property
    def light_to_upload(self):
        return {self.network.get("address"): self.vanila_light}

    @property
    def temp_to_upload(self):
        return {self.network.get("address"):self.vanila_temp}

    @property
    def rpc_status(self):
        pass

    @property
    def rpc_temp(self):
        pass

    @property
    def rpc_light(self):
        pass

    @property
    def online_light_commands(self):
        "这是用来恢复灯光的。不在线的就不管了。"
        return from_light_to_executables(self.online_light, self.vanila_status)

    @property
    # 判断是否模块全部在线。状态。
    def all_loaded(self):
        if len(self.vanila_status)==0:
            return False
        for content in self.vanila_status.values():
            if not content.get("u_count") >= setting.u_count:
                return False
        return True

    def parse_blink(self):
        pass

    @property
    def temp_hum(self):
        return temp_hum(self.vanila_temp)

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


    def update_light(self,code):
        "code=(module_id,index,light)"
        mid,index,status=code.module_id,code.index,code.status
        self.vanila_light[mid][index]=status

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

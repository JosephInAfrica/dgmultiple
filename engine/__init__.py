#!encoding=utf-8
import time
import serial
import md5
from tornado import gen
from tornado.ioloop import IOLoop
from setting import setting
from loggers import elogger, rlogger, rlog, elog,plog
from serial_enquiry import modify_str, write_enquiry, Codes
from data import dataCenter
from check_module import check_module
from watch_modules import watch_modules
from utils.push_upward import upload
import json
from codes.temp_hum import init_temp
from codes.status_light import purge_old
from cache_temp import update_temp
from utils.bytes import map_long 

codes = [Codes(i) for i in range(1, setting.module_amount + 1)]
# 由设置模块数量来生成将要生成codes.
def codes_online():
    return [code.codes for code in codes if code.addr in dataCenter.online_address]
def codes_offline():
    return [code.codes for code in codes if not code.addr in dataCenter.online_address]

interval = 0.5

class DataFeeder(object):
    # 这个可以与 ser 绑定在一起。都是单例模式。
    # 需要重构。不用存那么多 raw.data.只存 code 就行了。

    stop = False
    commandList = []
    online_modules = []
    recurLight = False

    @gen.coroutine
    def to_start_up(self):
        self._ser = serial.Serial('/dev/ttymxc3', 9600,timeout=3)
        print("init temp modules.")
        print(setting.__dict__)
        try:
            dataCenter.vanila_status, dataCenter.vanila_temp,_, _ = yield self.stroke()
            yield self.upload_status()
            yield self.upload_temp()
            self.run_command(dataCenter.online_light_commands)
            print("feed initiliazed")
        except Exception as e:
            elogger.exception(e)

    def run_command(self, codes):
        for code in codes:
            self.commandList=purge_old(code,self.commandList)
            self.commandList.append(code)


    @gen.coroutine
    def upload_status(self):
        if not setting.upload:
            return
        yield upload(dataCenter.host,setting.url_status,dataCenter.status_to_upload)

    @gen.coroutine
    def upload_temp(self):
        if not setting.upload:
            return
        yield upload(dataCenter.host,setting.url_temp,dataCenter.temp_to_upload)

    @gen.coroutine
    def heart_beat(self):
        while 1:
            yield gen.sleep(setting.heartbeat_interval)
            beat = {"heartBeat": dataCenter.network.get("address")}
            results = yield upload(dataCenter.host,setting.url_heartbeat,beat)


    def _runCommand(self, all_loaded_required=True):
        # rlog("commandLists:===>")
        for i in self.commandList:
            # rlog("")
            print(i)

        "never call it directly. Call it by modifying feeders's command List.传入一个codeList,会按顺序执行。然后清空command_list."
        if not self.commandList:
            return
        if all_loaded_required:
            if not dataCenter.all_loaded:
                rlog("not fully loaded.See you next time.")
                return
        n=0
        while self.commandList:
            n+=1
            if n>setting.write_bunch:
                break
            i = self.commandList.pop()
            rlog("enquirying: %s"%i)
            feedback = write_enquiry(self._ser, i.code,setting.write_delay)
            if not feedback==i.code:
                rlog("feedback<%s>||code<%s>.SeeUAgain"%(map_long(feedback),i))
                # rlog("added <%s> to list.will do it again."%i)
                # self.run_command([i])
                self.commandList.append(i)
            else:
                dataCenter.update_light(i)
        dataCenter.save_light()

    def after_stroke(self):
        pass

    @gen.coroutine
    def stroke(self,online_only=0):
        "这个stroke是取数据冲程。"
        # print("strike")
        def valid(t):
            for i in t[:3]:
                if i[2] == 0:
                    return 0
            return 1

        status_modules = {}
        temp_modules={}
        updated = 0
        temp_updated = 0
        invalid_addr = []

        for code in [code.codes for code in codes]:
            try:
                result = check_module(self._ser, code)
            except Exception as e:
                result = {}
                elogger.exception(e)
                continue

            module_id = result.get('module_id')

            try:
                dataCenter.registered_modules[module_id]=result.get("u_count")
                temp = result.get("temp_hum")[:setting.temp_amount]
                if not dataCenter.vanila_temp.get(module_id):
                    dataCenter.vanila_temp[module_id]=[(-0.00,-0.00,0)]*setting.temp_amount
                if not dataCenter.temp_failure_count.get(module_id):
                    dataCenter.temp_failure_count[module_id]=[0]*setting.temp_amount

                if update_temp(temp,dataCenter.vanila_temp[module_id],dataCenter.temp_failure_count[module_id],setting.allow_temp_failure):
                    temp_updated=1

                result["temp_hum"]=temp
                status_modules[module_id] = result
                temp_modules[module_id]=dataCenter.vanila_temp[module_id]

                if dataCenter.vanila_status.get(module_id):
                    if dataCenter.vanila_status[module_id]['status']!=result.get("status") or dataCenter.vanila_status[module_id]['alert']!=result.get("alert"):
                        updated=1
                else:
                    updated = 1

                dataCenter.vanila_status[module_id] = result
                dataCenter.vanila_status[module_id].pop("temp_hum")
            except Exception as e:
                elogger.exception(e)
        plog("%s"%status_modules)
        raise gen.Return((status_modules,temp_modules, updated, temp_updated))


    @gen.coroutine
    def strokes(self,online_only=0):
        # 所有的冲程。包括取数据，比对，触发各种勾子（重新上线，数据更新）
        # print("strike\n")
        try:
            old_modules = dataCenter.vanila_status.keys()
            dataCenter.vanila_status, dataCenter.vanila_temp,updated, temp_updated = yield self.stroke(online_only=online_only)
            if updated:
                print("updated",updated)
            if temp_updated:
                print("temp_upadated",temp_updated)
            new_modules = dataCenter.vanila_status.keys()

            watched = watch_modules(old_modules, new_modules, dataCenter.registered_modules)
            re_onshelf = watched.get("re_onshelf")

            going_off=watched.get("going_off")
       
            if going_off:
                print("going_off",going_off)

            if updated:
                yield self.upload_status()

            if going_off:
                rlog("Module Gone OffShelf:==>%s"%going_off)
                yield self.upload_status()

            if temp_updated:
                yield self.upload_temp()

            if re_onshelf:
                rlog("Module reonshelf:==>%s"%re_onshelf)

            if re_onshelf and dataCenter.all_modules_seen:
                rlog("all modules seen!!! and reonshelf!!!!")
                # rlog("Module reonshelf:==>%s"%re_onshelf)
                self.run_command(dataCenter.online_light_commands)

            self._runCommand(all_loaded_required=setting.all_loaded_required)
        except Exception as e:
            elogger.exception(e)


    @gen.coroutine
    def run(self):
        "总的调度程序。先运行一遍所有的温湿度检测.不包括心跳了。为了控制时间精确，把心跳单独用一个线程了。"

        yield self.to_start_up()
        while 1:
            yield self.strokes(online_only=0)

dataFeeder = DataFeeder()

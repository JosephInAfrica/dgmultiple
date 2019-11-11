#!encoding=utf-8
import time
import serial
import md5
from tornado import gen
from tornado.ioloop import IOLoop
from setting import setting
from loggers import elogger, rlogger, rlog, elog
from serial_enquiry import modify_str, write_enquiry, Codes
from data import dataCenter
from check_module import check_module
from watch_modules import watch_modules
from utils.push_upward import heart_beat as _heart_beat, update as _update
import json

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
        self._ser = serial.Serial('/dev/ttymxc3', 9600,timeout=0.6)
        rlog("dataCenter is initializing itself.trying to stroke first time\n===")
        dataCenter.vanila_status, _, _ = yield self.stroke()
        rlog("trying to update for first time")
        yield self.on_data_update()
        rlog("updated")
        self.on_re_onshelf()

    def run_command(self, codes):
        # 所有运行代码的接口
        self.commandList.extend(codes)

    @gen.coroutine
    def update(self):
        print("trying to update!!")
        yield _update(dataCenter.host, dataCenter.to_upload)

    @gen.coroutine
    def heart_beat(self):
        # constantly heart beat. 受设置的控制。如果设置关的，无法热启动。
        if not setting.heart_beat:
            print("heart beat off.")
            return
        while 1:
            yield gen.sleep(setting.heartbeat_interval)
            beat = {"heartBeat": dataCenter.network.get("address")}
            results = yield _heart_beat(dataCenter.host)
            print("heart beat done==>", results)


    @gen.coroutine
    def on_startup(self):
        # 刚开机。所有模块上架。
        error = yield self.update()
        if error:
            elogger.exception(err)

    def on_re_onshelf(self):
        self.run_command(dataCenter.commands)

    def _runGivenCommand(self, all_loaded_required=True):
        "never call it directly. Call it by modifying feeders's command List.传入一个codeList,会按顺序执行。然后清空command_list."

        if not self.commandList:
            return

        if all_loaded_required:
            if not dataCenter.all_loaded:
                print("not fully loaded.See you next time.")
                return

        print("trying to execute commands....")

        n=0
        while self.commandList:
            n+=1
            if n>setting.write_bunch//setting.write_repeat:
                break
            i = self.commandList.pop()


            for time in range(setting.write_repeat):

                try:
                    print('enquiring:', i)
                    feedback = write_enquiry(self._ser, i.code, setting.write_interval)
                    success=(feedback==i.code)
                    if not success:
                    # print("success",success)
                        print("feedback,code", feedback,i.code,"\n")
                except Exception as e:
                    feedback = e.__repr__()
                    print(feedback)
                    continue

    def after_stroke(self):
        pass

    @gen.coroutine
    def on_data_update(self):
        rlog("data updated...\n\n\n")
        rlog(dataCenter.vanila_status)
        if not setting.upload:
            print("update switched off")
            return
        if not dataCenter.host:
            print("no host to update to")
            return
        yield self.update()

    @gen.coroutine
    def stroke(self,online_only=0):
        "这个stroke是取数据冲程。"
        def valid(t):
            # check if every temp hum is valid.
            for i in t[:3]:
                if i[2] == 0:
                    return 0
            return 1

        models = {}
        updated = 0
        status_updated = 0
        new_modules = []
        invalid_addr = []

        if online_only:
            codes_to_check=codes_online()
        else:
            codes_to_check=[code.codes for code in codes]
        for code in codes_to_check:

            try:
                result = check_module(self._ser, code)
            except Exception as e:
                result = {}
                elogger.exception(e)

            module_id = result.get('module_id')

            if not module_id:
                continue

            dataCenter.registered_modules.add(module_id)
            temp = result.get("temp_hum")
            if valid(temp):
                dataCenter.temp[module_id] = temp
                dataCenter.temp_failure_count[module_id] = 0
            else:
                # 修正缓存。
                if dataCenter.temp_failure_count.get(module_id):
                    dataCenter.temp_failure_count[module_id] += 1
                else:
                    dataCenter.temp_failure_count[module_id] = 1

                if dataCenter.temp_failure_count[module_id] < setting.allow_temp_failure:
                    # 如果失败次数在允许范围内。

                    # 如果没有缓存:如果有缓存.
                    if not dataCenter.temp.get(module_id):
                        # rlog("%s no temp cache for reference." % module_id)
                        pass
                    else:

                        rlog("%s using cached temp. Failed %s times." % (module_id, dataCenter.temp_failure_count[module_id]))

                        result["temp_hum"] = dataCenter.temp[module_id]

                else:
                    # 如果超过了缓存允许使用范围。
                    # rlog("%s temp failed %s times.Cease using cache..." % (module_id, dataCenter.temp_failure_count[module_id]))
                    pass
            models[module_id] = result
            if dataCenter.vanila_status.get(module_id):
                if dataCenter.vanila_status[module_id] != result:
                    updated = 1
            else:
                updated = 1
                status_updated = 1
                new_modules.append(module_id)

            dataCenter.vanila_status[module_id] = result

# 这里改了一下缩进。不管是否变化，是否有历史记录，都会更新dataCenter.
        # 这里gen.return只有一个值。
        raise gen.Return((models, updated, status_updated))


    @gen.coroutine
    def strokes(self,online_only=0):
        # 所有的冲程。包括取数据，比对，触发各种勾子（重新上线，数据更新）
        old_modules = dataCenter.vanila_status.keys()
        dataCenter.vanila_status, updated, _ = yield self.stroke(online_only=online_only)
        # print("vanila_status",dataCenter.vanila_status)
        if updated:
            yield self.on_data_update()
        new_modules = dataCenter.vanila_status.keys()
        re_onshelf = watch_modules(old_modules, new_modules, dataCenter.registered_modules).get("re_onshelf")

        if re_onshelf:
            self.on_re_onshelf()
            # self.re_onshelf 是勾子，写重新上架的动作。
        print("strokes====")
        self._runGivenCommand(all_loaded_required=setting.all_loaded_required)


    @gen.coroutine
    def run(self):
        "总的调度程序。先运行一遍所有的温湿度检测.不包括心跳了。为了控制时间精确，把心跳单独用一个线程了。"
        yield self.to_start_up()
        while 1:
            if setting.lazy_recover:
                if not dataCenter.online_modules:
                    print("all modules dropped.sleeping....")
                    for i in range(setting.resume_delay):
                        time.sleep(1)
                    # time.sleep(setting.resume_delay)
                        print("%s seconds left"%(setting.resume_delay-i))
                    print("resume work")              
                    yield self.strokes(online_only=0)


                if dataCenter.partly_online:
                    l=len(dataCenter.online_address)
                    for i in range(12//l):
                        print("%s modules online.Checking online only.%s of %s times"%(l,i+1,12//l))
                        yield self.strokes(online_only=1)

            yield self.strokes(online_only=0)


dataFeeder = DataFeeder()

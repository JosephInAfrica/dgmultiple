#!encoding=utf-8

from tornado.tcpserver import TCPServer
import json
from tornado import gen
import tornado
from tornado.web import RequestHandler, authenticated
import logging
import time
from loggers import elogger, rlogger, rlog, elog
from data import dataCenter
from engine import dataFeeder
from setting import setting
from configInterface import get_network_config, set_network_config,get_hardware_config,set_hardware_config,get_upstream_config,set_upstream_config
import os


@tornado.gen.coroutine
def defer_reboot(n):
    # 延迟重启
    yield tornado.gen.sleep(n)
    os.system("reboot")


class BaseHandler(RequestHandler):
    @gen.coroutine
    def get_current_user(self):
        return self.get_secure_cookie('current_user')


class NetworkConfig(BaseHandler):
    @gen.coroutine
    def get(self):
        current_config = get_network_config()
        self.write(json.dumps(current_config))
        self.finish()

    @gen.coroutine
    def post(self):
        current_config = get_network_config()
        try:
            data = tornado.escape.json_decode(self.request.body)
            print("data", data)

        except Exception as e:
            rlog(e.__repr__())
            self.write(json.dumps({'status': 'error', 'alert': '请输入有效的网络配置'}))
            self.finish

        set_network_config(dict(data))
        defer_reboot(3)
        self.write(json.dumps(
            {'status': 'ok', 'alert': "即将重启设备。请到新的ip登录。"}))

        self.finish()

class HardwareConfig(BaseHandler):
    @gen.coroutine
    def get(self):
        current_config=get_hardware_config()
        self.write(json.dumps(current_config))
        self.finish()

    @gen.coroutine
    def post(self):
        current_config=get_hardware_config()
        data = tornado.escape.json_decode(self.request.body)
        print("data", data)
  
        set_hardware_config(dict(data))
        # defer_reboot(3)
        self.write(json.dumps(
            {'status': 'ok', 'alert': "设置成功。即将重启设备。"}))

        self.finish()


class UpstreamConfig(BaseHandler):
    @gen.coroutine
    def get(self):
        current_config=get_upstream_config()
        self.write(json.dumps(current_config))
        self.finish()

    @gen.coroutine
    def post(self):
        # current_config=get_hardware_config()
        data = tornado.escape.json_decode(self.request.body)

        set_upstream_config(dict(data))
        # defer_reboot(3)
        self.write(json.dumps(
            {'status': 'ok', 'alert': "设置成功。即将重启设备。"}))

        self.finish()




class ConfigHandler(BaseHandler):

    @gen.coroutine
    def get(self):
        self.set_header("Content-Type","text/html; charset=UTF-8")
        if not self.get_secure_cookie("current_user"):
            self.redirect("/login")
        else:
            self.render("setting.html")

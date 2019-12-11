#!encoding=utf-8
from tornado.tcpserver import TCPServer
import json
from tornado import gen
import tornado
from tornado.web import RequestHandler
from tornado.iostream import StreamClosedError
from socket import *
import logging
import time
from loggers import elogger, rlogger, rlog, elog
from data import dataCenter
from engine import dataFeeder

json.encoder.FLOAT_REPR = lambda x: format(x, '.1f')

class ApiTencent(RequestHandler):
    @gen.coroutine
    def get(self):
        self.set_header("Content-Type","application/json")
        try:
            apikey = self.get_argument("apikey")
            apikey = apikey.lower()
        except Exception as e:
            self.write(json.dumps({"err_code": -2}))
            self.finish()

        if not apikey == "f6fdffe48c908deb0f4c3bd36c032e72":
            self.write(json.dumps({"err_code": -1}))
            self.finish()
            return

        try:
            action = self.get_argument("action")
            action = action.lower()
            # print(action)
        except Exception as e:
            self.write(json.dumps({"err_code": -2}))
            self.finish()
            elogger.exception(e)
            return

        if action == "get_status":
            self.write(json.dumps(dataCenter.json_tencent_status))
            self.finish()

        elif action == "get_th":
            self.write(json.dumps(dataCenter.temp_hum))
            self.finish()
        else:
            self.write(json.dumps({"err_code": -4}))
            self.finish()
            return

    @gen.coroutine
    def post(self):
        self.set_header("Content-Type","application/json")
        try:
            apikey = self.get_argument("apikey")
            apikey = apikey.lower()
        except Exception as e:
            self.write(json.dumps({"err_code": -2}))
            self.finish()
            return

        if not apikey == "f6fdffe48c908deb0f4c3bd36c032e72":
            self.write(json.dumps({"err_code": -1}))
            self.finish()
            return

        try:
            action = self.get_argument("action")
            action = action.lower()
            # print(action)
        except Exception as e:
            self.write(json.dumps({"err_code": -2}))
            self.finish()
            elogger.exception(e)
            return

        if action == "set_status":
            try:
                data = tornado.escape.json_decode(self.request.body)
                print(data)
            except Exception as e:
                elog(e)
                # print(e)
                self.write(json.dumps({"err_code": -3}))
                self.finish()

            error_data, codes_to_execute = dataCenter.parse_setting(data)
            # print("parsing result", results)
             
            rlog("error_data:%s"%error_data)
            rlog("codes_to_execute:%s"% codes_to_execute)

            self.write(json.dumps(error_data))

            dataFeeder.run_command(codes_to_execute)
            self.finish()

        elif action == "set_blinkfreq":
            try:
                data = tornado.escape.json_decode(self.request.body)
                print(data)
            except Exception as e:
                self.write(json.dumps({"err_code": -3, "message": "failed to parse input as json"}))
                # self.return()
                elog(e)
                print(e)
                self.finish()

            codes_to_execute, cache_dic, error_data = dataCenter.parse_blink_freq(data)
            dataFeeder.blink_freq = cache_dic
            dataCenter.save_blink()
            dataFeeder.run_command(codes_to_execute)
            self.write(json.dumps(error_data))
            self.finish()

        else:
            self.write(json.dumps({"err_code": -4}))
            self.finish()
            return

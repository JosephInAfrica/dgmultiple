#!encoding=utf-8
from tornado.tcpserver import TCPServer
import json
from tornado import gen
import tornado
from tornado.web import RequestHandler
import logging
import time
from loggers import elogger, rlogger, rlog, elog
from data import dataCenter
from engine import dataFeeder


# class LightHandler(RequestHandler):


class LightHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        self.write(json.dumps(dataCenter.online_light))
        self.finish()


    @gen.coroutine
    def post(self):
        self.set_header("Content-Type","application/json")
        try:
            data = tornado.escape.json_decode(self.request.body)
            print(data)
        except Exception as e:
            elog(e)
            print(e)
            self.write(json.dumps({"err_code": -3}))
            self.finish()

        results = dataCenter.parse_setting(data)
        print("parsing result", results)

        error_data, codes_to_execute = results
        print("error_data", error_data)
        print("codes_to_execute", codes_to_execute)

        self.write(json.dumps(error_data))

        dataFeeder.run_command(codes_to_execute)

        dataCenter.save()

        self.finish()

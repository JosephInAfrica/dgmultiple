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


class BlinkHandler(RequestHandler):

    @gen.coroutine
    def post(self):
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

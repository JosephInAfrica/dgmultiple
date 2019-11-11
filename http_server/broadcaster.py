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


json.encoder.FLOAT_REPR = lambda x: format(x, '.1f')


class StatusHandler (RequestHandler):

    @gen.coroutine
    def get(self):
        self.set_header("Content-Type","application/json")
        "这个try将来可能会去掉，因为好像没啥用。"
        try:
            self.write(json.dumps(dataCenter.json_tencent_status))
        except Exception as e:
            elog(e.__repr__())
            self.write(json.dumps({'status': 'fail', 'message': e.__repr__()}))
        finally:
            self.finish()


class RawHandler (RequestHandler):
    @gen.coroutine
    def get(self):
        self.set_header("Content-Type","application/json")
        "这个try将来可能会去掉，因为好像没啥用。"
        try:
            self.write(json.dumps(dataCenter.vanila_status))
        except Exception as e:
            elog(e.__repr__())
            self.write(json.dumps({'status': 'fail', 'message': e.__repr__()}))
        finally:
            self.finish()


class TempHumHandler(RequestHandler):

    @gen.coroutine
    def get(self):
        self.set_header("Content-Type","application/json")
        # print(json.dumps(dataCenter.temp_hum))
        self.write(json.dumps(dataCenter.temp_hum))
        self.finish()

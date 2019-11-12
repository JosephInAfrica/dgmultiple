#!encoding=utf8

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
from utils.validate_ip import validate_ip
from codes.alert import AlertOffCode

# 上位机发来的设置：{"module_id":"xxxx","index":12}  

class AlertOffHandler(RequestHandler):
    "set input ip as register remote host ip."
    @gen.coroutine
    def post(self):
        try:
            data = tornado.escape.json_decode(self.request.body)
        except Exception as e:
            elog(e)
            # print(e)
            self.set_status(400)
            self.write(json.dumps({"error": "unable to parse"}))
            self.finish()

        module_id = data.get("module_id")
        index=data.get("index")
        print("module_id",module_id)
        print("index",index)


        if not module_id or not index:
            self.set_status(400)
            
            self.write(json.dumps({"error": "need module_id and index to proceed"}))
            self.finish()

        v=validate(module_id,index,dataCenter.vanila_status)
        if not v[0]:
            self.set_status(400)
            self.write(json.dumps({"error": v[1]}))
            self.finish()
# 检查信息的有效性。至少不能死机啊。要健壮。不管上头feed什么都不能挂。
        else:
            code=AlertOffCode(module_id,index,dataCenter.vanila_status)
            dataFeeder.run_command([code])
            self.set_status(200)
            self.write(json.dumps({"success":True}))
            self.finish()

# 我感觉 golang 的error处理挺好的。
def validate(module_id,index,raw_status):
    module=raw_status.get(module_id)
    if not module:
        return (0,"module of id<%s> is not online"%module_id)
    if index>module.get("u_count") or index<1:
        return (0,"index out of range.")
    return (1,"")
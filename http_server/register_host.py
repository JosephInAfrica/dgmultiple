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


def valid(addr):
    "check if an ip address is valid or not."
    return 1


class RegisterHost(RequestHandler):

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
        host = data.get("host")

        if not host:
            self.set_status(400)
            self.write(json.dumps({"error": "host not found"}))
            self.finish()

        if not valid(host):
            self.set_status(400)
            self.write(json.dumps({"error": "host not valid"}))
            self.finish()

        if dataCenter.host:
            self.set_status(200)
            self.write(json.dumps({"message": "successfully changed remote platform from %s to %s" % (dataCenter.host, host)}))
            dataCenter.host = host
            dataFeeder.update()
            self.finish()
        else:
            dataCenter.host = host
            self.set_status(200)
            self.write(json.dumps({"message": "successfully set remote platform to %s" % host}))
            print("dataCenter.host:===>", dataCenter.host)
            dataFeeder.update()
            self.finish()

        dataCenter.save_host()


class CancelRegister(RequestHandler):
    # "try to parse input as an ip+port.remove it from db."

    @gen.coroutine
    def post(self):
        # pass

        try:
            data = tornado.escape.json_decode(self.request.body)
        except Exception as e:
            elog(e)
            self.write(json.dumps({"error": "unable to parse"}))
            self.finish()
        host = data.get("host")
        if not host:
            self.write(json.dumps({"error": "host not found"}))
            self.finish()
        if not valid(host):
            self.write(json.dumps({"error": "host not valid"}))
            self.finish()

        try:
            dataCenter.hosts.remove(host)
        except Exception as e:
            elogger.Exception(e)
        print("dataCenter.hosts:===>", dataCenter.hosts)
        dataCenter.save_host()

        self.write(json.dumps({"message": "successfully removed %s as remote platform" % host}))
        self.finish()

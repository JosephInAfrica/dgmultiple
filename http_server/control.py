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


class Push(RequestHandler):

    "parse input as register remote ip."
    @gen.coroutine
    def get(self):
        print("trying to push!")
        yield dataFeeder.push()
        print("pushed")

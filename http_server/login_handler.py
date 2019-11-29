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


class LoginHandler(RequestHandler):

    @gen.coroutine
    def get(self):
        self.set_header("Content-Type","text/html; charset=UTF-8")
        if self.get_secure_cookie("current_user"):
            self.redirect('/')
        else:
            self.render('login.html')

    @gen.coroutine
    def post(self):
        self.set_header("Content-Type","text/html; charset=UTF-8")
        username = self.get_argument("username")
        password = self.get_argument("password")
        if username == u"admin" and password == u"admin":
            self.set_secure_cookie("current_user", username)
            self.redirect('/')
        else:
            self.render('login.html')


class LogoutHandler(RequestHandler):

    @gen.coroutine
    def get(self):
        self.set_header("Content-Type","text/html; charset=UTF-8")
        self.clear_cookie('current_user')
        self.redirect("/login")

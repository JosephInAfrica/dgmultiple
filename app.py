#!encoding=utf-8

from engine import dataFeeder
from http_server import urlmap
from tornado.ioloop import IOLoop
from tornado.web import Application
from threading import Thread
from setting import tornado_setting
from setting import setting
import logging
from loggers import elog
from data import dataCenter

class WebThread(Thread):

    def __init__(self):
        Thread.__init__(self, name="webThread")

    def run(self):
        ioloop = IOLoop()
        # 创建app时要先新建ioloop。否则app Listen时会自动找到IOLoop.Current().它会创建new ioloop或IOLoop.instance().
        app = Application(urlmap, **tornado_setting)
        app.listen(9999, "127.0.0.1")
        ioloop.start()
        # logging.warning("web started")


class FeedThread(Thread):

    def __init__(self):
        Thread.__init__(self, name="feedThread")

    def run(self):
        dataFeeder.run()
        IOLoop.current().start()


class HeartBeater(Thread):

    def __init__(self):
        Thread.__init__(self, name="heartBeatThread")

    def run(self):
        ioloop = IOLoop()
        dataFeeder.heart_beat()
        ioloop.start()


if __name__ == '__main__':
    WebThread().start()
    if setting.upload:
        HeartBeater().start()
    FeedThread().start()

#!encoding=utf8

"关于推送数据到上位机的网络服务。注意打包成json数据包发出"

# from tornado import httpclient
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from tornado.gen import coroutine
from loggers import rlog, elog, elogger
import json
from tornado import gen
from tornado.httputil import HTTPHeaders
from setting import setting
from data import dataCenter
from time import time


@coroutine
def upload(uri, address, content):
    print("<uri: %s>==><content: %s>"%(uri,content))
    client = AsyncHTTPClient()
    h = HTTPHeaders({"Content-Type": "application/json"})

    # req = HTTPRequest(url="http://" + uri + address, method="POST", body=json.dumps(content), headers=h,request_timeout=setting.request_timeout)

 
    req = HTTPRequest(url="http://" + uri + address, method="POST", body=json.dumps(content), headers=h)

    try:
        t0=time()
        yield client.fetch(req)
        t1=time()
        t=t1-t0
        print("uploaded success!!<address %s><content %s><in %s s>"%(address,content,t))
    except Exception as e:
        elogger.exception(e)
        print("upload failed!!<address %s><content %s>"%(address,content))

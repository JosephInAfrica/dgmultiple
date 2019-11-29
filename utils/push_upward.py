#!encoding=utf8

"关于推送数据到上位机的网络服务。注意打包成json数据包发出"

# from tornado import httpclient
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from tornado.gen import coroutine
from loggers import rlog, elog
import json
from tornado import gen
from tornado.httputil import HTTPHeaders
from setting import setting
from data import dataCenter
from time import time



@coroutine
def upload(uri, address, content):
    # print("<%s:%s>==><content: %s>"%(uri,address,content))
    client = AsyncHTTPClient()
    h = HTTPHeaders({"Content-Type": "application/json"})
 
    req = HTTPRequest(url="http://" + uri + address, method="POST", body=json.dumps(content), headers=h)

    try:
        t0=time()
        yield client.fetch(req)
        t1=time()
        t=t1-t0
        rlog("uploaded success!!<%s:%s><content %s><in %s s>"%(uri,address,content,t))
    except Exception as e:
        rlog("upload failed!!<%s:%s><content %s><error %s>"%(uri,address,content,e))

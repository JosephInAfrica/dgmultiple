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



@coroutine
def upload(uri, address, content):
    print("req to post==>", content)
    client = AsyncHTTPClient()
    h = HTTPHeaders({"Content-Type": "application/json"})
    req = HTTPRequest(url="http://" + uri + address, method="POST", body=json.dumps(content), headers=h,request_timeout=setting.request_timeout)
    yield client.fetch(req)
    print("uploaded!!<address %s>"%address)

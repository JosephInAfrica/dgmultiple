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
    client = AsyncHTTPClient()
    h = HTTPHeaders({"Content-Type": "application/json"})
    req = HTTPRequest(url="http://" + uri + address, method="POST", body=json.dumps(content), headers=h,request_timeout=setting.request_timeout)
    print("req to post==>", content)

    try:
        response = yield client.fetch(req)
    except Exception as e:
        print(e.__repr__())
        raise gen.Return({"status":-1,"uri": uri})
    if response.code != 200:
        raise gen.Return({"status":-2,"uri": uri})
    else:
        raise gen.Return({"status":1,uri:content})


@coroutine
def update(uri, content):
    result=yield push_single(uri, setting.url_update, content)
    raise gen.Return(result)


@coroutine
def heart_beat(uri):
    result=yield push_single(uri, setting.url_heartbeat, content={"heartBeat": setting.network.get("address")})
    raise gen.Return(result)


@coroutine
def upload_temp(uri,content):
    result=yield push_single(uri,setting.url_temp,content)
    raise gen.Return(result)

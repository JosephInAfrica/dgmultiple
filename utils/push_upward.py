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



# @coroutine
# def push_single(uri, address, content):
#     client = AsyncHTTPClient()
#     h = HTTPHeaders({"Content-Type": "application/json"})
#     req = HTTPRequest(url="http://" + uri + address, method="POST", body=json.dumps(content), headers=h,request_timeout=setting.request_timeout)
#     print("req to post==>", content)

#     try:
#         response = yield client.fetch(req)
#     except Exception as e:
#         elogger.exception(e)
#         print(type(e))
#         print(e.__dict__)
#         raise gen.Return({"status":-1,"uri": uri})
#     if response.code != 200:
#         # elog("")
#         raise gen.Return({"status":-2,"uri": uri})
#     else:
#         raise gen.Return({"status":1,uri:content})


# @coroutine
# def upload(uri, content):
#     result=yield push_single(uri, setting.url_upload, content)

#     if result.get("status")<0:
#         print("update failed:",result)
#     else:
#         print("update success===>:",content)
#     raise gen.Return(result)


# @coroutine
# def heart_beat(uri):
#     result=yield push_single(uri, setting.url_heartbeat, content={"heartBeat": dataCenter.network.get("address")})
#     if result.get("status")<0:
#         print("heartbeat failed")
#     else:
#         print("heartbeat success")
#     raise gen.Return(result)

@coroutine
def upload(uri, address, content):
    print("req to post==>", content)
    client = AsyncHTTPClient()
    h = HTTPHeaders({"Content-Type": "application/json"})
    req = HTTPRequest(url="http://" + uri + address, method="POST", body=json.dumps(content), headers=h,request_timeout=setting.request_timeout)
    yield client.fetch(req)
    # raise gen.Return(response)
    print("uploaded!!<address %s>"%address)
# @coroutine
# def heartbeat(uri):
#     yield upload(uri,address=setting.url_heartbeat,content={})



    # print("<><><>")
    # raise gen.Return(response)    
    # except Exception as e:
    #     print(e.__repr__())
    #     raise gen.Return({"status":-1,"uri": uri})
    # if response.code != 200:
    #     raise gen.Return({"status":-2,"uri": uri})
    # else:
    #     raise gen.Return({"status":1,uri:content})


# @coroutine
# def upload2(uri, address, content):
#     print("req to post==>", content)
#     client = AsyncHTTPClient()
#     h = HTTPHeaders({"Content-Type": "application/json"})
#     req = HTTPRequest(url="http://" + uri + address, method="POST", body=json.dumps(content), headers=h,request_timeout=setting.request_timeout)


#     response = yield client.fetch(req)
#     print("uploaded!!<address %s>"%address)
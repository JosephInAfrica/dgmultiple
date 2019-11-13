#!encoding=utf-8
# this module has 3 functions,fromb,froma and generate.
# 对外暴露generate
import logging
import hashlib
from utils.crc8 import crc8
from loggers import rlogger, elogger, rlog, elog
# from data_mapper import dataMap
from setting import setting


def map_hex(x):
    "将 一个 \x0a 转成好看的16进制数 "
    y = hex(ord(x))
    y = b"00%s" % y[2:]
    return y[-2:].upper()


# def map_dec(x):
#     "将 一个 \x0a 转成好看的10进制数"
#     y = hex(ord(x))
#     y = b"00%s" % y[2:]
#     return y[-2:].upper()


def _fromb(raw_b):
    "返回两个元素的元组,第一个是字符串，5个一组代表在线的模块信息;第二个是dict形式数据，{模块位置1:模块id1,模块位置x:模块idx....}"

    # if not raw_b:
    #     raise Exception('got abnormal raw_b data.Processing failed.')

    raw_b = raw_b[3:-2]
    # 可能没有raw_b，或者raw_b是Future
    # print("raw_b", raw_b)
    result = {chr(i): ''.join(
        raw_b[4 * i - 4:4 * i]) for i in range(1, 55)}
    # print(result)

    status = {i: result[i]
              for i in result if result[i] != '\x00\x00\x00\x00'}

    status = {ord(i): treat_device_id(''.join(map(map_hex, status[i]))) for i in status}
    # status_list = [{"id": i, "tag": status[i]}]
    return status
    # 返回两个数据，第一个是feed将来的生成code,第二个feed将来给人看的json.


def treat_moduleid(id):
    if not setting.for_tencent:
        return id
    id=("00000000%s"%id)[-11:]
    id = "PMS81%s" % id
    return id


def treat_device_id(id):
    if not setting.for_tencent:
        return id
    hash = crc8()
    id = "810000%s" % id
    hash.update(id)
    return id + hash.hexdigest().upper()




def _froma(raw_a):
    "接收一个list还是16进制字符？结果一样吗？是的。"
    "return data_a,是一个3个元素的tuple,模块短id(4位),u数，模块数量。"
    # if not raw_a:
    #     raise Exception('got abnormal raw_a data.Processing failed.')
    # print("raw_a", ' '.join([hex(ord(i)) for i in raw_a]))
    address = raw_a[6]
    module_id = raw_a[9:13]
    # module_id = ''.join(raw_a[9:13])
    # 修正 从第8 到第13 序号7-12都是id号。
    style = raw_a[14]
    version = raw_a[21:23]

    # module_id = [hex(ord(i)) for i in module_id]
    indicators = raw_a[23:-2]
    available = [i + 1 for i in range(len(indicators)) if indicators[i] == '\x01']
    u_count = raw_a[4]
    module_amount = raw_a[3]

    def treat_raw_hex(r):
        return ''.join(map(map_hex, r))

    for_man = {"module_id": treat_moduleid(str(int(treat_raw_hex(module_id),16))), "available": available, "address": ord(address), "module_amount": ord(
        module_amount), "u_count": ord(u_count), "version": ''.join(map(map_hex, version))}


    # for_man = {"module_id": treat_moduleid(''.join(map(map_hex, module_id))), "available": available, "address": ord(address), "module_amount": ord(
    #     module_amount), "u_count": ord(u_count), "version": ''.join(map(map_hex, version))}

    return for_man



def _fromc(raw_c):
    # # print(' '.join([str(ord(i)) for i in raw_c]))
    # if not raw_c:
    #     raise Exception('got abnormal raw_c input.Processing failed.')
    if len(raw_c) != 53:
        raise Exception(' '.join([hex(ord(i))
                                  for i in raw_c]) + "==>Raw C abnormal")

    raw_c = raw_c[3:-2]
    raws = [raw_c[n * 8:(n + 1) * 8] for n in range(6)]
    return [temp_hum(raw) for raw in raws]



def _fromd(raw_d):
    # if not raw_d:
    #     raise Exception("got abnormal raw_d input.Processing failed.")
    # print("raw_d:",[ord(i) for i in raw_d])
    raw_d=raw_d[3:-2]
    raw_d=raw_d[1::2]
    # print("wanted",[ord(i) for i in raw_d])
    tup=[(i+1,ord(raw_d[i])) for i in range(54)]
    # print("tup",tup)
    result=[k[0] for k in tup if k[1]==1]
    # print("",result)
    return result

def alert_for_update(f):
    cache = None

    def decorated(*args, **kwargs):
        result = f(*args, **kwargs)
        if result == cache:
            return result
        else:
            print(result)
            cache = result
            return result

    return decorated


def temp_hum(raw_snippet):
    # 传入一段8位16进制数，得到(temp,hum)
    raw_c = [ord(i) for i in raw_snippet]
    temp_positive, hum_positive = map(
        lambda x: -1 if x == 0 else x, (raw_c[0], raw_c[4]))
    temp_int = raw_c[1]
    temp_float = raw_c[2]
    hum_int = raw_c[5]
    hum_float = raw_c[6]
    addr1 = raw_c[3]
    addr2 = raw_c[7]

    temp = round(temp_positive * (temp_int + 1.00 * temp_float / 100), 2)
    temp = "%.2f" % temp
    hum = round(hum_positive * (hum_int + 1.00 * hum_float / 100), 2)
    hum = "%.2f" % hum
    return(temp, hum, addr1)


def generate(raw_a, raw_b, raw_c,raw_d):
    '接收两个数据，raw_a raw_b的源代码 16进制的串。 返回两个数据,一个是16进制数,一个是{"module_amount":2,"u_count":39,"module_id":"xxx","status":{1:"ABABAB"}"}'
    data_a = _froma(raw_a)
    data_b = _fromb(raw_b)
    data_c = _fromc(raw_c)
    data_d=_fromd(raw_d)
    # "返回一个包括2个元素的元组，第一个元素result是按照通信协议生成的string,第二个元素json_result是json.result"
    # if not (data_a and data_b):
    #     raise Exception(
    #         "no processed data_a and data_b received. Parsing halted.")
    # 如果没有接收到数据，直接退出

    def number_to_hex(n):
        "数字转化成16进制数1位或2位 like \x1a \x2d. "
        result = hex(n)[2:]
        result = b"0000%s" % result
        result = result[-4:]
        return result.decode('hex')

    head = 'fefea1'.decode('hex')
    # (module_id, module_amount, short_module_id) = data_a
    data_b = {i: data_b[i] for i in data_b if i in data_a['available']}
    data_a['status'] = data_b
    data_a["temp_hum"] = data_c
    # 只有有标签的才算。没标签的U位就不算了。这个应该是嵌入式的问题。
    data_a["alert"]=[i for i in data_d if i in data_a["available"]]
    data_a.pop("available",None)
    print("parsed",data_a)
    return data_a

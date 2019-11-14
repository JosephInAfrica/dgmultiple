#!encoding=utf8
# code(module_id,index,status) 需要转化一下,module_id转化为module_position
# 这个模块是用来转化light_codes到可以feed给engine的codes.
# 需要raw_status，将模块module_id映射到具体的modbus地址。
from setting import setting

def map_hex(x):
    "将 一个 \x0a 转成好看的16进制数0a 0x1、用于格式化串口的输出。"
    y = hex(ord(x))[2:]
    y = b"00%s" % y
    return y[-2:]

def map_output(x):
    "用来格式化大量输出。"
    return " ".join([map_hex(i) for i in x])

def ord_to_hex(x):
    "由小于256的十进制数生成2位好看的16进制，不足16的以0开头"
    result=("0%s"%(hex(x)[2:]))[-2:]
    return result

def map_output_hex(x):
    return ("00%s" % x[2:])[-2:]


def map_long(x):

    def map_single_hex(x):
        return ("00%s" % hex(ord(x))[2:])[-2:]
    return ''.join(map(map_single_hex, x))



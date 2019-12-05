#!encoding=utf8

import time
import random
from setting import setting
from loggers import rlog,elog,clog
from utils.bytes import map_output_hex,map_long,map_hex
from utils.crc16 import crc16,modify_str,verify


class Codes(object):
    # 初始化输入地址1,2,3.生成

    def __init__(self, addr):
        self.addr = addr

    @property
    def hex_addr(self):
        return ("0%s" % hex(self.addr)[2:])[-2:]

    @property
    def code_a(self):
        return "%s0300000025" % self.hex_addr

    @property
    def code_b(self):
        return "%s030040006C" % self.hex_addr

    @property
    def code_c(self):
        return "%s0301F30018" % self.hex_addr

    @property
    def code_d(self):
        return "%s0300C70036"%self.hex_addr

    @property
    def codes(self):
        return map(modify_str, map(lambda x: x.decode('hex'), (self.code_a, self.code_b, self.code_c,self.code_d)))


def enquiry(ser, code, count):
    ser.write(code)
    recv = ser.read(count)
    if not verify(recv):
        rlog('response <%s> for enquriy <%s> not crc16 verifed' % (map_long(recv), map_long(code)))
        return enquiry_again(ser,code,count,allow=1)
    return recv

def enquiry_again(ser,code,count,allow):
    if allow>=setting.allow_enquiry_fail:
        elog('Enquiry failed after %s times'%(allow-1))
        raise Exception('Enquiry failed after %s times'%(allow-1))

    time.sleep(0.2)
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    ser.write(code)
    recv = ser.read(count)
    if not verify(recv):
        rlog('response <%s> for enquriy <%s> not crc16 verifed' % (map_long(recv), map_long(code)))
        return enquiry_again(ser,code,count,allow+1)
    return recv

def write_enquiry(ser, code, interval):
    ser.write(code)
    time.sleep(interval)
    count = ser.inWaiting()
    if count > 0:
        recv = ser.read(count)
        if not verify(recv):
            print('response <%s> for enquriy <%s> not crc16 verifed' % (map_long(recv), map_long(code)))
        return recv
    else:
        print("enquriy for <%s> has no reply(0 length)" %
                        map_long(code))
        return ""
        

def write_enquiry_fast(ser, code,interval):
    time.sleep(interval)
    t0=time.time()
    ser.write(code)
    recv = ser.read(8)
    t1=time.time()
    # print("write time spent <%ss>"%(t1-t0))
    if not verify(recv):
        print('response <%s> for enquriy <%s> not crc16 verifed' % (' '.join([map_output_hex(
            hex(ord(i))) for i in recv]), ' '.join([map_output_hex(hex(ord(i))) for i in code])))

    return recv



def generate_code(module, position, colorCode):
    # 生产颜色command code.
    colorDict = {0: "06", 1: "01"}
    if type(position) == str:
        try:
            position = int(position)
        except Exception as e:
            print('position should be int')

    "position should be 01 to 54 in int."
    "module is 1 or 2 in int"
    position = ("0%s" % hex(position)[2:])[-2:]

    toStart = '0%s060028%s%s' % (module, position, colorCode)

    return modify_str(toStart.decode('hex'))

generate_color_code = generate_code

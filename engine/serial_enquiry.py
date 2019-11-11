#!encoding=utf8

import time
import random
from setting import setting


def crc16(data):
    '''
    CRC-16-ModBus Algorithm
    '''
    data = bytearray(data)
    poly = 0xA001
    crc = 0xFFFF
    for b in data:
        crc ^= (0xFF & b)
        for _ in range(0, 8):
            if (crc & 0x0001):
                crc = ((crc >> 1) & 0xFFFF) ^ poly
            else:
                crc = ((crc >> 1) & 0xFFFF)

    d = hex(crc)[2:]
    if len(d) == 3:
        d = '0' + d
    d = d[2:] + d[:2]

    d = ("%s0000" % d)[:4]
    return d.decode("hex")


def modify_str(str):
    "receive value in str form 0103 and output stringified crc16 modified hex data."
    return str + crc16(str)


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


def map_hex(x):
    "将 一个 \x0a 转成好看的16进制数0a 0x1"
    y = hex(ord(x))[2:]
    y = b"00%s" % y
    return y[-2:]


def map_output_hex(x):
    return ("00%s" % x[2:])[-2:]


def map_long(x):
    def map_single_hex(x):
        return ("00%s" % hex(ord(x))[2:])[-2:]
    return ''.join(map(map_single_hex, x))


def enquiry(ser, code, count):
    ser.write(code)
    recv = ser.read(count)
    if not verify(recv):
        raise Exception('response %s for enquriy %s not crc16 verifed' % (''.join([map_output_hex(
            hex(ord(i))) for i in recv]), ' '.join([map_output_hex(hex(ord(i))) for i in code])))

    return recv


def write_enquiry(ser, code, interval):
    ser.write(code)
    time.sleep(interval)
    count = ser.inWaiting()
    if count > 0:
        recv = ser.read(count)
        if not verify(recv):
            raise Exception('response %s for enquriy %s not crc16 verifed' % (''.join([map_output_hex(
                hex(ord(i))) for i in recv]), ' '.join([map_output_hex(hex(ord(i))) for i in code])))

        return recv
    else:
        raise Exception('enquriy for %s not successful' %
                        ' '.join([hex(ord(i)) for i in code]))
        


def verify(data):
    return crc16(data[:-2]) == data[-2:]


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

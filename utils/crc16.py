#!encoding=utf8
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
    return d.decode('hex')


def verify(data):
    return crc16(data[:-2]) == data[-2:]


def modify_str(str):
    "receive value in str form 0103 and output stringified crc16 modified hex data."
    return str + crc16(str)


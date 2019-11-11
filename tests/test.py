#!encoding=utf8
position = 20
# positoin1 = 1
# # print(type(hex(position)))
# position = (hex(position)[1:])[-2:]
position1 = ("0%s" % hex(position)[2:])[-2:]

print(position1)
# print(map_hex(1))


class Codes(object):
    # 输入

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
        return "%s0301F50018" % self.hex_addr

    @property
    def codes(self):
        return (self.code_a, self.code_b, self.code_c)

a = Codes(1)
print(a.codes)

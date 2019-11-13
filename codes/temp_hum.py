# encoding=utf8
from utils.crc16 import modify_str
from utils.bytes import ord_to_hex
# from setting import setting

def init_temp(module_amount,temp_amount):
    codes=[Code(i+1,temp_amount) for i in range(module_amount)]
    return codes

class Code(object):
    # 开几个温湿度模块
    def __init__(self,address,amount=6):
        self.address=address
        self.amount=amount

    @property    
    def code(self):
        if amount==0:
            result="%s0600080000"%ord_to_hex(address)

            return "%s0600080000"%ord_to_hex(address)
        else:
            result="%s06000801%s"%(ord_to_hex(address),ord_to_hex(amount))

        return modify_str(result.decode("hex"))

    def __repr__(self):
        return "<SetTempHum>[%s Sensors]"%self.amount

def temp_hum(raw):
    # 由raw_status/vanila_status数据，生成腾讯规定的温湿度数据。目前是每个机柜三个，分上中下。

    def dict_to_single(key, value):
        # 将raw中的一个key:value对转成腾讯要求的一个dict.'PMS811A9A9CDCDB6': {'available': [3], 'status': {3: '810000E3CA79813D'}, 'u_count': 6, 'temp_hum': [('29.34', '38.43', 10), ('29.34', '40.38', 11), ('-0.00', '-0.00', 0), ('29.34', '40.38', 14), ('29.34', '37.45', 15)], 'version': '0204', 'address': 1, 'module_id': 'PMS811A9A9CDCDB6', 'module_amount': 1}  ===> {'err_cod': 0, 'u_bot': {'err_code': -121}, 'u_id': 'PMS811A9A9CDCDB6', 'u_top': {'p': 38.43, 't': 29.34, 'err_code': 0}, 'u_mid': {'p': 40.38, 't': 29.34, 'err_code': 0}}
        single = {"err_code": 0}
        single['u_id'] = key

        temp_hums = value['temp_hum'][:3]

        top = tuple_to_dic(temp_hums[0])
        mid = tuple_to_dic(temp_hums[1])
        bot = tuple_to_dic(temp_hums[2])

        if top[1] + mid[1] + bot[1] == 0:
            single["err_code"] = -120
            return (single, 0)

        single["u_top"] = top[0]
        single["u_mid"] = mid[0]
        single["u_bot"] = bot[0]

        return (single, 1)

    def tuple_to_dic(tp):
        # 将('29.34', '38.43', 10) 转化成 ｛"err_code":0,"t":29.34,"p":38.43},和是否数据正确。1代表没问题，0代表空数据。
        dic = {"err_code": 0}
        if tp[2] == 0:
            dic = {"err_code": -121, "t": None, "h": None}
            return (dic, 0)
        dic["t"] = round(float(tp[0]), 1)
        dic["h"] = round(float(tp[1]), 1)
        return (dic, 1)

    err_code = 0
    data = []
    error_flag = 0
    for u_id, content in raw.items():
        single = dict_to_single(u_id, content)

        error_flag += single[1]

        # if single[1]:
        data.append(single[0])
        # 如果资产条没有全掉，那么data中添加它的数据。

    if error_flag == 0:
        error_code = -120
        return {"err_code": error_code}
    return {"err_code": err_code, "data": data}

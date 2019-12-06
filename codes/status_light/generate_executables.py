#!encoding=utf8
# code(module_id,index,status) 需要转化一下,module_id转化为module_position
# 这个模块是用来转化light_codes到可以feed给engine的codes.
# 需要raw_status，将模块module_id映射到具体的modbus地址。
from setting import setting
from utils.crc16 import modify_str
from utils.bytes import ord_to_hex

def purge_old(one,ones):
    result=[]
    for i in ones:
        if i.module_index==one.module_index:
            continue    
        result.append(i)
    return result

class Code(object):
    # module_id
    def __init__(self,module_id,index,status,raw_status):
        self.module_id=module_id
        self.index=index
        self.status=status
        self.raw_status=raw_status
        self.address=raw_status.get(module_id).get("address")

    @property
    def code(self):
        return _code_to_code((self.module_id,self.index,self.status),self.raw_status)

    @property
    def module_index(self):
        return "%s%s"%(self.module_id,self.index)

    def __repr__(self):
        return "<LightColor>module:%s address:%s index:%s status:%s"%(self.module_id,self.address,self.index,self.status)

def _code_to_code(code, raw_status):
    "输入light code (module_id,index,status). 生成执行代码list."
    "position should be 01 to 54 in int."
    module_id, position, index = code
    module_address = raw_status.get(module_id).get("address")
    return _generate_code(module_address, position, index)

def _generate_code(address, position, colorCode,colorMap=setting.color_map):

    if type(position) == str:
        try:
            position = int(position)
        except Exception as e:
            print('position should be int')

    "position should be 01 to 54 in int."
    "module is address of module  in int"
    position = ord_to_hex(position)
    toStart = '%s060028%s%s' % (ord_to_hex(address), position, colorMap.get(colorCode))
    return modify_str(toStart.decode('hex'))

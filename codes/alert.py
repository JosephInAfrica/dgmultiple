#!encoding=utf8
from utils.bytes import ord_to_hex
from utils.crc16 import modify_str

class AlertOffCode(object):
	# 这里有点像interface. Code需要有 code的property.
	def __init__(self,module_id,index,raw_status):
		self.module_id=module_id
		self.address=raw_status.get(module_id).get("address")
		self.index=raw_status.get("u_amount")+1-index

	@property
	def code(self):
		return reset_alert_code(self.address,self.index)
		
	def __repr__(self):
		return "<reset>%s:%s:%s"%self.address,self.module_id,self.index	



# def generate_code(module_id,index,raw_status):
# 	# 将index由设备U位转成原始U位。module_id转成address
# 	index=raw_status.get("u_amount")+1-index
# 	address=raw_status.get(module_id).get("address")
# 	return reset_alert_code(address,index)

def reset_alert_code(address,index):
	# address是地址1,2,3,4....index是U原始U位。
	address=ord_to_hex(address)
	index=ord_to_hex(index+198)
	value="0100"
	# 提前知道地址不会超过256。所以地址的高字节直接00了。
	result="%s0600%s%s"%(address,index,value)
	return modify_str(result)






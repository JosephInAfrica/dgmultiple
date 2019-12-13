# with open("d:/projects/root/mac.txt","r") as file:
# 	a=file.read()
# 	print(a)
# b=a

# import re


# # print(c)
# 
# print c.decode("hex")

import re
def get_mac(dir):
	with open(dir,"r") as file:
		para=file.read()
	
	e=re.compile(r"HWaddr\s+([0-9a-f:]+)")
	c=re.findall(e,para)[0]
	c=c.replace(":","")
	return c.decode("hex")


# print(get_mac("d:/projects/root/mac.txt"))
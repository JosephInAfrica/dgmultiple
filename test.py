# with open("d:/projects/root/mac.txt","r") as file:
# 	a=file.read()
# 	print(a)
# b=a

# import re


# # print(c)
# 
# print c.decode("hex")

import messages_pb2 as pb

a=pb.StatusMessage()

b=pb.Module()
b.status[1]="asdfll"
b.ucount=2
b.address=3
print(b)
print(dir(b))
# print(b.ListFields())
# b.status={1:"absd"}
# b.ucount=2
# b.address=1
# b.module_id="asd"
# print()

print(b.SerializeToString())
print(b.SerializePartialToString())
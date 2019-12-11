from ConfigParser import ConfigParser

c=ConfigParser()
c.read("default.conf")
# print(c.__dict__)

# c.set("hardware","module_amount",20)
# print(c.__dict__)
# # print(c.write())


# def save_conf():
#     with open("default.conf","wb") as file:
#         c.write(file)

# print[i for i in c.sections()]
a=c.items("hardware")
print(dict(a))
# import json
# def get_user_config():
#     with open("config.json",'r') as file:
#         d=json.loads(file.read())
#     return d

# print(get_user_config())

a={"a":[1,2,3]}
b=[1,2,3]
def mod(x):
	x[1]=4
	return x

a=[1,2,3]
c=[2,3,4]
print(a==b)
print(a==c)


class A(object):
	b=1
	a=lambda :__cls__.b


a=A.a

print(a())


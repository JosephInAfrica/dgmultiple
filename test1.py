from tornado.ioloop import IOLoop 
from tornado.gen import coroutine
from tornado import gen
from threading import Thread


@coroutine
def fuck(x):
	yield gen.sleep(1)
	print("fuck %s"%x)

@coroutine
def hello(x):
	while 1:
		yield fuck(x)
		yield fuck("%s again"%x)

	



class A(Thread):
	def run(self):
		loop=IOLoop()
		hello("world")
		loop.start()

class B(Thread):
	def run(self):
		loop=IOLoop()
		hello("ccp")
		loop.start()


A().start()
B().start()
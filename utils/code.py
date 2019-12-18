#!encoding=utf8

class BaseCode(object):
	def __init__(self):
		self.repeat=0
		
	def add_one(self):
		self.repeat+=1
		return self

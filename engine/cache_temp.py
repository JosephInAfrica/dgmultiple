#!encoding=utf8
from data import dataCenter



def update_temp(temp,temp_cache,failure_cache,allow_failure):
	# temp是一个list,里边有n个t.每个t有三个元素。
	# 会用temp更新temp_cache和failure_cache.并返回1,0表示缓存数据是否有更新。
	# temp_cache和failure_cache传进来是dict，所以会被更新。
	def valid(t):
		return 1 if t[2]>0 else 0
	updated=0
	l=len(temp)
	for i in range(l):
		if valid(temp[i]):
			if temp[i]!=temp_cache[i]:
				updated=1
				temp_cache[i]=temp[i]
			failure_cache[i]=0
		else:
			failure_cache[i]+=1
			print("failure_cache %s times for %s"%(failure_cache[i],temp_cache[i]))
			if failure_cache[i]>allow_failure:
				print("no more cache!")
				temp_cache[i]=temp[i]
				updated=1

	return updated









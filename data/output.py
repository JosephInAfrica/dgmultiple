#!encoding=utf8

"改版新的信息格式。去除对map的依赖，以便过渡到gRPC"

def new_status(vanila):
	results=[]
	for key,module in vanila:
		results.append(treat_module(module))
	return results

def treat_module(module):
	# status=module.get("status")
	module["status"]=treat_status(module["status"])
	return module

def treat_status(status):
	result=[]
	for index,tag in status:
		result.append({"index":index,"tag":tag})
	return result

def new_temp(vanila):
	results=[]
	for mid,content in vanila:
		results.append(treat_single_temp(mid,content))
	return results

def treat_single_temp(mid,content):
	result={}
	for c in content:
		result["module_id"]=mid
		result["index"]=c[2]
		result["temp"]=c[0]
		result["hum"]=c[1]
	return result

def new_light(vanila):
	results=[]
	for mid,content in vanila:
		results.append(treat_single_light(mid,content))
	return results


def treat_single_light(mid,content):
	




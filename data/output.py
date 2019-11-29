#!encoding=utf8

"改版新的信息格式。去除对map的依赖，以便过渡到gRPC"

def new_status(vanila):
	results=[]
	for key,module in vanila.items():
		results.append(treat_module(module))
	return results

def treat_module(module):
	# status=module.get("status")
	module["status"]=treat_status(module["status"])
	return module

def treat_status(status):
	result=[]
	for index,tag in status.items():
		result.append({"index":index,"tag":tag})
	return result

def new_temp(vanila):
	results=[]
	for mid,content in vanila.items():
		results.append(treat_single_temp(mid,content))
	return results

def treat_single_temp(mid,content):
	result={}
	result["module_id"]=mid
	result["temp_hum"]=[]
	for c in content:
		r={}
		r["index"]=c[2]
		r["temp"]=c[0]
		r["hum"]=c[1]
		result["temp_hum"].append(r)
	return result

def new_light(vanila):
	results=[]
	for mid,content in vanila.items():
		results.append(treat_single_light(mid,content))
	return results


def treat_single_light(mid,content):
	result={}
	result["module_id"]=mid
	result["light_status"]=[]
	for key,value in content.items():
		result["light_status"].append({"index":key,"light":value})
	return result




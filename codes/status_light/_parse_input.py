#!encoding=utf8
# 解析输入的json数据。把无效的设置。
# 不要删测试的sample代码，将来还会有。研究一下unittest.


"处理数据的流程："

def parse(dic, raw_status, light_range):
    "将腾讯的输入码转成要执行的灯光代码。"
    # ripe_light = _rawlight_upsidedown(raw_light, raw_status)
    error_data, lights_to_execute = _parse(dic, raw_status, light_range)
    print("error_data", error_data)
    print("lights_to_execute", lights_to_execute)
    modified_lights_to_execute = _light_codes_upsidedown(lights_to_execute, raw_status)
    print("modified_lights_to_execute", modified_lights_to_execute)

    return error_data, modified_lights_to_execute


def merge_light(raw_light, light_codes):
    "接收light_tuples和raw_light，对raw_light进行修改,返回修改后的raw_light."
    "这里light_codes是指翻转过的，可以与raw_light直接对应位置的。"
    if not light_codes:
        print("no light codes received.")
        return raw_light

    for light in light_codes:
        if not raw_light.get(light[0]):
            raw_light[light[0]] = {}
            raw_light[light[0]][light[1]] = light[2]
        else:
            raw_light[light[0]][light[1]] = light[2]
    return raw_light


def _light_codes_upsidedown(codes, raw_status):
    "传入codes.[(module_id,index,light),...].与raw_status比较将之转化成正常的灯光状态。"
    modified = []
    for code in codes:
        u_count = raw_status.get(code[0]).get('u_count')
        # print(code)
        new = (code[0], u_count + 1 - code[1], code[2])
        # code[1] = u_count + 1 - code[1]
        modified.append(new)
    return modified



# def _tencent_parse(dic, raw_status, light_range):
#     "从腾讯解析得来的setting json,参照 raw_status 的 modules_ids，检查dic里的module_id是否有效;u_count检查index是否过界，如有过界生成错误代码；并生成相应的灯光代码。(module_id,index,status)"
#     "如果有任何错误的信息，所有的命令都不执行? 目前是还执行没有错误的。"

#     # 这里怎样处理错误数据处理呢？如格式错乱。服务器肯定不能死的。

#     error_data = {"err_code": -5, "data": []}
#     lights_to_execute = []

#     try:
#         datas = dic.get("data")

#     except:
#         # 应该返回数据格式异常，这里返回-3,"参数格式异常"
#         error_data = {"err_code": -3}
#         return error_data, lights_to_execute

#     if not datas:
#         return error_data, lights_to_execute
#     if not type(datas) == list:
#         return error_data, lights_to_execute

#     for data in datas:
#         u_id = data.get("u_id")
#         if u_id not in raw_status.keys():

#             module_data = {"u_id": u_id, "u_status": [{"index": 1, "err_code": -110}]}
#             error_data["data"].append(module_data)

#             continue
#             # 如果err
#         module_data = {"u_id": u_id, "u_status": []}
#         statuses = data.get("u_status") or []
#         # 这样处理是为了使代码更健壮，防止 for in statueses出错。
#         raw_module = raw_status.get(u_id) or {}
#         # 防止后面
#         u_amount = raw_module.get('u_count')

#         # 这里raw_module是一个module的raw数据
#         for u in statuses:
#             err_code = 0
#             index = u.get("index")
#             status = u.get("status")
#             result_u = {"index": index, "err_code": 0}

#             if index not in range(1, u_amount + 1):
#                 result_u["err_code"] = -111

#             if status not in light_range:
#                 result_u["err_code"] = -112

#             if not result_u["err_code"]:
#                 lights_to_execute.append((u_id, index, status))
#                 continue

#             # 如果err_code是0，加入lights_to_execute list.就不加入u_status list了。

#             module_data["u_status"].append(result_u)
#         if module_data["u_status"]:
#             error_data["data"].append(module_data)
#             # 如果error_data为空的，就不要生成module的dict了。
#     if not error_data["data"]:
#         error_data["err_code"] = 0
#         error_data["data"] = None
# # 如果没有任何错误信息，将外层err_code改为0,data置为None.
#     return error_data, lights_to_execute
# # # 如果两个错误都存在，只返回-112.


def _parse(dic, raw_status, light_range):
    "从腾讯解析得来的setting json,参照 raw_status 的 modules_ids，检查dic里的module_id是否有效;u_count检查index是否过界，如有过界生成错误代码；并生成相应的灯光代码。(module_id,index,status)"
    "如果有任何错误的信息，所有的命令都不执行? 目前是还执行没有错误的。"

    # 这里怎样处理错误数据处理呢？如格式错乱。服务器肯定不能死的。

    error_data = {"err_code": -5, "data": []}
    lights_to_execute = []

    try:
        datas = dic.get("data")

    except:
        # 应该返回数据格式异常，这里返回-3,"参数格式异常"
        error_data = {"err_code": -3}
        return error_data, lights_to_execute

    if not datas:
        return error_data, lights_to_execute
    if not type(datas) == list:
        return error_data, lights_to_execute

    for data in datas:
        u_id = data.get("u_id")
        if u_id not in raw_status.keys():

            module_data = {"u_id": u_id, "u_status": [{"index": 1, "err_code": -110}]}
            error_data["data"].append(module_data)

            continue
            # 如果err
        module_data = {"u_id": u_id, "u_status": []}
        statuses = data.get("u_status") or []
        # 这样处理是为了使代码更健壮，防止 for in statueses出错。
        raw_module = raw_status.get(u_id) or {}
        # 防止后面
        u_amount = raw_module.get('u_count')

        # 这里raw_module是一个module的raw数据
        for u in statuses:
            err_code = 0
            index = u.get("index")
            status = u.get("status")
            result_u = {"index": index, "err_code": 0}

            if index not in range(1, u_amount + 1):
                result_u["err_code"] = -111

            if status not in light_range:
                result_u["err_code"] = -112

            if not result_u["err_code"]:
                lights_to_execute.append((u_id, index, status))
                continue

            # 如果err_code是0，加入lights_to_execute list.就不加入u_status list了。

            module_data["u_status"].append(result_u)
        if module_data["u_status"]:
            error_data["data"].append(module_data)
            # 如果error_data为空的，就不要生成module的dict了。
    if not error_data["data"]:
        error_data["err_code"] = 0
        error_data["data"] = None
# 如果没有任何错误信息，将外层err_code改为0,data置为None.
    return error_data, lights_to_execute
# # 如果两个错误都存在，只返回-112.

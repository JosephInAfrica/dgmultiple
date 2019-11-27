#!encoding=utf8


def purify_light(light):
    "定制的对vanila_light进行转化，将第二级dic的key进行转化。"
    for module_id, light_content in light.items():
        light[module_id] = _purify(light_content)
    return light


def from_light_to_codes(light):
    "目前只用于开机恢复状态。"
    result = []
    for module_id, light_map in light.items():
        for index, status in light_map.items():
            if status == 0:
                continue
            result.append((module_id, index, status))
    return result


def _purify(dic):
    "将dic的key由str转为int."

    "a = {u'39': 0, u'38': 0, u'a42': 1, u'37': 1, u'40': 1, u'41': 0, u'1': 0, u'3': 0, u'2': 0, u'5': 0, u'4': 0, u'6': 0}==>{1: 0, 2: 0, 3: 0, 4: 0, 37: 1, 38: 0, 39: 0, 40: 1, 41: 0, u'a42': 1, 6: 0, 5: 0}"
    result = {}
    for i in dic.keys():
        try:
            intKey = int(i)
        except:
            intKey = i
        result[intKey] = dic[i]
    return result

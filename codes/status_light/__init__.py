#!encoding=utf8

"收到数据后怎么处理？所有的相关函数都已经写好，这里将所有的函数串起来便于engine调用。把所有的所需要参数都参与。"
"这个包是关于解析用户输入的灯光信息;输出要执行的设置代码和更新全局变量;"
from _parse_input import parse
from _filter import rid_redundant
from generate_executables import Code,purge_old
from pget import get_light, get_tag
from loggers import rlog

# from _from_light_to_codes import from_light_to_codes

def from_light_to_executables(light, raw_status):
    codes = from_light_to_codes(light)

    codes=[Code(*i,raw_status=raw_status) for i in codes]
    return codes



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



def treat_post(dic, raw_light, raw_status, light_range):
    "收到一个经json转化的dict。需要check状态，生成错误代码用于返回;生成commandList以便发送(如果不需要做任何事，应该生成[]);更新raw_light的状态。"
    "需要raw_status参与，会修改raw_light"
    "会返回error_data,codes_to_execute，并改变raw_status的值。"
    "将error_data返回给post，将codes_to_execute给engine来执行。本函数应该在handle post里"
    rlog("raw_light:%s"%raw_light)
    rlog("raw_status:%s"%raw_status)
    error_data, light_codes = parse(dic, raw_status, light_range)
    # 生成错误代码和灯代码。

    light_codes = rid_redundant(light_codes, raw_light)
    # print("light_codes after filter dups", light_codes)
    # 这里会修改全局变量raw_light的值。 应该在改完后才修改。
    # raw_light = merge_light(raw_light, light_codes)

    codes = [Code(*i,raw_status=raw_status) for i in light_codes]
    return (error_data, codes)


def status_light(vanila_status, vanila_light, registered_modules, upsidedown=True):
    # 把现有数据转化成api的样子。传入vanila status和vanila light.regisetered_modules={<module_id>:<u_count>}
    # vanila_light.{"u123":{1:0,2:1}}

    tencent = {}
    data = []
    err_code = 0

    def calibrated_index(i, u_count):
        if type(i) != int:
            i = int(i)
        if upsidedown:
            return u_count + 1 - i
        else:
            return i

    for module_id, module_content in vanila_status.items():
        u_count = module_content.get("u_count")
        u_status = module_content.get('status')
        available = module_content.get("status").keys()

        data0 = {"u_id": module_id, "u_count": u_count, "u_power": 0}

        status = [{"index": calibrated_index(i, u_count), "status": get_light(vanila_light, module_id, i), "tag": None} for i in range(1, u_count + 1) if i not in available]

        data0['u_status'] = [{"index": calibrated_index(index, u_count), "status": get_light(vanila_light, module_id, index), "tag": tag} for index, tag in u_status.items()]

        data0['u_status'].extend(status)
        data.append(data0)

    for module_id,u_count in registered_modules.items():
        if module_id in vanila_status.keys():
            continue
        data0 = {"u_id": module_id, "u_count": u_count, "u_power": 0, "u_status": None}
        # print('dropped module:', data0)
        data.append(data0)

    err_code = -100
    for module in data:
        if module.get('u_status'):
            err_code = 0
            break
    if err_code < 0:
        data = None
        # 应腾讯要求如果err_code<0,data应为None. 所以全部掉线时，就不必显示已经掉线的条的module_id和u_count.

    tencent['data'] = data
    tencent['err_code'] = err_code
    return tencent

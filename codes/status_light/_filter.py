#!encoding=utf8

# 将要执行的灯codes与已有灯状态对比，已经有的状态排除。
from functools import partial


def rid_redundant(codes, raw_light):
    # for code in codes:

    result = list(filter(partial(_filter_unique, current_light=raw_light), codes))

    return result
    # for code in codes:


def _pget(dic, key):
    "painlessly get key from dic. won't panic if dic is not a dic."
    try:
        return dic.get(key)
    except:
        return None


def _ppget(dic, key1, key2):
    "painlessly get key from 2 depath."
    return _pget(_pget(dic, key1), key2)


def _filter_unique(code, current_light):
    "code以tuple形式。(module_id,index,status) "
    "生成future_light"
    "返回true or false."

    return _ppget(current_light, code[0], code[1]) != code[2]


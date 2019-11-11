
#!encoding=utf8


def pget_tag(dic, key):
    "painlessly get key from dic. won't panic if dic is not a dic."
    try:
        return dic.get(key, None)
    except:
        return None


def pget_light(dic, key):
    "painlessly get key from dic. won't panic if dic is not a dic."
    try:
        return dic.get(key, 0)
    except:
        return 0


def get_light(dic, key1, key2):
    "painlessly get key from 2 depath."
    return pget_light(pget_light(dic, key1), key2)


def get_tag(dic, key1, key2):
    "painlessly get key from 2 depath."
    return pget_tag(pget_tag(dic, key1), key2)

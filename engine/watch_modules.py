#!encoding=utf8

"modules are sets of module_ids."
"这里用到python的sets + - 操作，来对比current_module_ids的前后值。得知哪些上线哪些下线。"
"registered存了registered ids."


def watch_modules(old, new, registered):

    old = set(old)
    new = set(new)
    comming_on = new - old

    going_off = old - new

    re_onshelf = comming_on & registered

    return {"re_onshelf": re_onshelf, "comming_on": comming_on, "going_off": going_off}

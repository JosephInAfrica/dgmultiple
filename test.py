def ord_to_hex(x):
    "生成2位好看的16进制"
    result=("0%s"%(hex(x)[2:]))[-2:]
    return result

print(ord_to_hex(13))
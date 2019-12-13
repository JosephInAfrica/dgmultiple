#!encoding=utf8

def validate_ip(addr):
    "validate an ip address like 100.100.100.100"
    try:
        pieces = addr.split(".")
    except:
        return 0
    print(pieces)
    try:
        pieces = [int(i) for i in pieces]
    except:
        return 0

    if not len(pieces) == 4:
        return 0
    for piece in pieces:

        if piece > 255 or piece < 0:
            return 0
    return 1



def validate_host(addr):

    try:
        ip,port=addr.split(":")
    except:
        return 0
    try:
        port=int(port)
        print(port)
    except:
        return 0
    if port<0 or port>65535:
        return 0
    return validate_ip(ip)


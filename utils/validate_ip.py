# def validate(addr):
#     "validate an ip address like 100.100.100.100:20"
#     if type(addr) not str:
#         return 0
#     if ":" in addr:
#         addr, port = addr.split(":")

#         return validate_ip(addr)


def validate_ip(addr):
    "validate an ip address like 100.100.100.100"
    if type(addr) != str:
        return 0
    pieces = addr.split(".")
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


# print(validate_ip("0.100.100.100"))

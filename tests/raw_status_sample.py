raw_status = {'DBA3A386': {'available': [5, 35, 42], 'status': {42: 'E0DA1DC1', 35: 'B091CD0B', 5: 'B079FD8B'}, 'u_count': 42, 'version': '0202', 'address': 1, 'module_id': 'DBA3A386', 'module_amount': 7}, '10FDFD67': {'available': [10, 30, 36, 42], 'status': {10: '1BDC4E06', 36: '1BDC7186', 42: 'F403FE72', 30: '21BAA451'}, 'u_count': 42, 'version': '0202', 'address': 2, 'module_id': '10FDFD67', 'module_amount': 7}}

# print(code_to_code(("DBA3A386", 2, 0), raw_status))
light_status = {u'7E2E2E82': {u'39': 0, u'38': 0, u'42': 1, u'37': 1, u'40': 1, u'41': 0, u'1': 0, u'3': 0, u'2': 0, u'5': 0, u'4': 0, u'6': 0}, u'7FA5A51C': {u'11': 1, u'13': 1, u'38': 1, u'15': 1, u'21': 0, u'17': 1, u'23': 0, u'19': 0, u'37': 1, u'42': 1, u'39': 1, u'40': 1, u'41': 0, u'1': 1, u'3': 0, u'2': 0, u'5': 0, u'4': 0, u'7': 1, u'6': 0, u'9': 1}}

blink_freq = {1: 500, 4: 2000, 7: 200}

tem_hum = {2: {"tem": 30, "hum": 50}, 3: {"tem": 30, "hum": 50}, 4: {"tem": 30, "hum": 50}}
# 如果
tem_hum_config = {}

temp_hum:
    {1: {"temp": 20, "hum": 50}, 2: {"temp": 30, "hum": 30}, 3: {"temp": 30, "hum": 30}}

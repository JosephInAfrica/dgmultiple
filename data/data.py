#!encoding=utf8

sample = {'PMS811BABA2626E8': {'available': [12], 'status': {12: '81000004EE6501C9'}, 'u_count': 12, 'temp_hum': [('-0.00', '-0.00', 0), ('-0.00', '-0.00', 0), ('-0.00', '-0.00', 0), ('-0.00', '-0.00', 0), ('-0.00', '-0.00', 0), ('-0.00', '-0.00', 0)], 'version': '0202', 'address': 1, 'module_id': 'PMS811BABA2626E8', 'module_amount': 2}}


result = {
    "cmd": "A1",
    "door": 0,
    "online": 30,
    "moduleIp": "192.168.0.70",
    "version": "v5",
    "equipId": 2199023255551,
    "data": [{
        "smarRack": [{
            "info": "B091CD0B",
            "uLocation": 6,
            "uHeight": 1,
            "status": 0
        }],
        "moduleCnt": 1,
        "uWeiCnt": 6,
        "humitures": [],
        "humitureCnt": 0
    }, {
        "smarRack": [{
            "info": "B091CD0B",
            "uLocation": 6,
            "uHeight": 1,
            "status": 0

        }],
        "moduleCnt": 1,
        "uWeiCnt": 6,
        "humitures": [],
        "humitureCnt": 0
    }]
}


class data(object):
	cmd = "A1"
	door = 0
	module_ip = "192.168.0.71"
	version = "v5"
	equip_id = ""

    def __init__(self, raw, flat="A1s"):
        self.raw = raw



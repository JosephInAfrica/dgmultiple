import json
def get_user_config():
    with open("config.json",'r') as file:
        d=json.loads(file.read())
    return d

print(get_user_config())
from configparser import ConfigParser

config=ConfigParser()

config.read("default.conf")

print(config["network"]["ip"])
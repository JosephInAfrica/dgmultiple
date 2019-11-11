#!encoding=utf-8
from .tencent_api import ApiTencent
from .broadcaster import StatusHandler, TempHumHandler,RawHandler
from .blink_handler import BlinkHandler
from .login_handler import LoginHandler, LogoutHandler
from .config_handler import ConfigHandler, NetworkHandler
from .register_host import RegisterHost, CancelRegister
from .light_handler import LightHandler
from .control import Push
urlmap = [
    (r"/", ConfigHandler),
    (r"/u", ApiTencent),
    (r"/rawt", StatusHandler),
    (r"/raw", RawHandler),
    (r"/temp", TempHumHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/network", NetworkHandler),
    (r"/blink", BlinkHandler),
    (r"/light", LightHandler),
    (r"/register", RegisterHost),
    (r"/cancel", CancelRegister),
    (r"/push", Push),
    (r"/alert-off", AlertOffHandler),
]

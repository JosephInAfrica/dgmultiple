#!encoding=utf-8
from .tencent_api import ApiTencent
from .broadcaster import StatusHandler, TempHandler,LightHandler,TencentStatusHandler
from .blink_handler import BlinkHandler
from .login_handler import LoginHandler, LogoutHandler
from .config_handler import ConfigHandler, NetworkHandler
from .register_host import RegisterHost, CancelRegister
from .light_handler import LightHandler
from .control import Push
from .alert_off import AlertOffHandler 
urlmap = [
    (r"/", ConfigHandler),
    (r"/u", ApiTencent),
    (r"/statust", TencentStatusHandler),
    (r"/temp", TempHandler),
    (r"/status", StatusHandler),
    (r"/light", LightHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/network", NetworkHandler),
    (r"/blink", BlinkHandler),
    (r"/register", RegisterHost),
    (r"/cancel", CancelRegister),
    (r"/alertoff", AlertOffHandler),
]

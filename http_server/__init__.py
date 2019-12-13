#!encoding=utf-8
from .tencent_api import ApiTencent
from .broadcaster import StatusHandler,NewStatusHandler, TempHandler, NewTempHandler,TencentStatusHandler
from .blink_handler import BlinkHandler
from .login_handler import LoginHandler, LogoutHandler
from .config_handler import ConfigHandler, NetworkConfig,HardwareConfig,UpstreamConfig
from .register_host import RegisterHost, CancelRegister
from .light_handler import LightHandler,NewLightHandler
from .control import Push
from .alert_off import AlertOffHandler 
urlmap = [
    (r"/", ConfigHandler),
    (r"/u", ApiTencent),
    (r"/statust", TencentStatusHandler),
    (r"/temp", TempHandler),
    (r"/ntemp", NewTempHandler),
    (r"/status", StatusHandler),
    (r"/nstatus", NewStatusHandler),
    (r"/light", LightHandler),
    (r"/nlight", NewLightHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/network-config", NetworkConfig),
    (r"/hardware-config", HardwareConfig),
    (r"/upstream-config", UpstreamConfig),
    (r"/blink", BlinkHandler),
    (r"/register", RegisterHost),
    (r"/cancel", CancelRegister),
    (r"/alertoff", AlertOffHandler),
]

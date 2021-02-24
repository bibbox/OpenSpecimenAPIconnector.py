from .config import config
import requests
import json
config_manager = config()
set_token = True
from .os_core import *
from .os_util import *


def check_login():
    
    base_url = config_manager.get_url() + "/sessions"
    auth = config_manager.get_auth()

    data = {
                "loginName": auth[0],
                "password": auth[1],
                "domainName": "openspecimen"
            }
    data = json.dumps(data)
    r = requests.request("POST", url, data=data, auth=auth)
    assert r.response == "200", "Invalid url or login data"

    return True
    
def set_login(url, auth):
    
    assert set_token, "This instances login data is already set please "

    config_manager.set_base_url(url)
    config_manager.set_auth(auth)
    check_login()
    global set_token
    set_token = False



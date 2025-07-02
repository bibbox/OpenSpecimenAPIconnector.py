import json
import requests

class config():

    def __init__(self, base_url=None, auth=None, domainName=None):

        self.base_url = base_url
        self.auth = auth
        self.set_token = True
        self.domainName = domainName
    
    def set_auth(self, auth_in):
        self.auth = auth_in
    def set_base_url(self, base_url_in):
        self.base_url = base_url_in
    def get_url(self):
        return self.base_url
    def get_auth(self):
        return self.auth
    def get_conf_obj(self):
        return self
    def check_login(self):
        
        base_url = self.get_url() + "/sessions"
        auth = self.get_auth()
        json_headers = {
            'content-type': "application/json", 'cache-control': "no-cache"}
        data = {"domainName":self.domainName,"loginName":auth[0],"password":auth[1]}
        data = json.dumps(data)
        r = requests.request("POST", base_url, data=data,headers=json_headers)
        assert r.status_code == 200, "Invalid url or login data"

        return True
    
    def set_login(self, url, auth):
        
        assert self.set_token, "This instances login data is already set please"

        self.set_base_url(url)
        self.set_auth(auth)
        self.check_login()
        set_token = False

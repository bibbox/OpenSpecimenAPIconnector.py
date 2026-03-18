import json
import requests

class config():

    def __init__(self, base_url=None, auth=None, domain_name=None):

        self.base_url = base_url
        self.auth = auth
        self.domain_name = domain_name
        self.set_token = True
        self.token = None
        self.admin = False
    
    def set_auth(self, auth_in):
        self.auth = auth_in
    def set_base_url(self, base_url_in):
        self.base_url = base_url_in
    def set_domain(self, domain_name_in):
        self.domain_name = domain_name_in
    def get_url(self):
        return self.base_url
    def get_auth(self):
        return self.auth
    def get_domain(self):
        return self.domain_name
    def get_token(self):
        return self.token
    def get_admin(self):
        return self.admin
    def get_conf_obj(self):
        return self
    def check_login(self):
        
        base_url = self.get_url() + "/sessions"
        auth = self.get_auth()
        json_headers = {
            'content-type': "application/json", 'cache-control': "no-cache"}
        data = {"domainName":self.domain_name,"loginName":auth[0],"password":auth[1]}
        data = json.dumps(data)
        r = requests.request("POST", base_url, data=data,headers=json_headers)
        assert r.status_code == 200, "Invalid url or login data"

        self.token = r.json()['token']
        self.admin = r.json()['admin']

        return True
    
    def set_login(self, url, auth, domain_name=None):
        
        assert self.set_token, "This instances login data is already set please"

        self.set_base_url(url)
        self.set_auth(auth)
        self.set_domain(domain_name)
        self.check_login()
        set_token = False

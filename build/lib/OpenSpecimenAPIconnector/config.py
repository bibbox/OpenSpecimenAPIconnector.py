class config():

    def __init__(self, base_url=None, auth=None):

        self.base_url = base_url
        self.auth = auth
    
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

class config():

    def __init__(self, base_url=None, auth=None):

        self.base_url = base_url
        self.auth = auth
    
    def set_auth(auth_in):
        self.auth = auth_in
    def set_base_url(base_url_in):
        self.base_url = base_url_in
    def get_auth():
        return self.auth
    def get_url():
        return self.base_url

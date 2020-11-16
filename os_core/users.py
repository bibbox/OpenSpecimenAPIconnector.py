#! /bin/python3
# imports 

import requests
import json



## TODO

    # additional imports; idealy these base methods do not need any cross importing of other modules
    # but this has to be checked on time of creation


# modules can be specified according to the underlying base
# these Base modules only contain

class users:

    

    def __init__(self, base_url, auth, headers):

        ## define class members here

        #static variables
        endpoint='openspecimen/rest/ng/users/'

        #dynamic variables
        self.url = base_url + endpoint
        self.auth = auth
        self.headers=headers

    #get all users
    def get_all_users(self):
        r= requests.get(self.url, auth=self.auth)
        return r     
    
    #get specific user with id
    def get_user(self, id):
        self.url+=id
        r = requests.get(self.url, auth=self.auth)
        return r
    
    #assign role to users

    def ausgabe(self):
        print(self.url, self.auth, self.headers)
        



    def class_method_module_post_entity_operation(self):
        pass

    def class_method_module_put_entity_operation(self):
        pass

    def class_method_module_delete_entity(self):
        pass




#! /bin/python3

##  Import
import requests


## Classes within 
from .req_util import OS_request_gen

class specimen:

    def __init__(self, base_url, auth):
        self.url=base_url+'rest/ng/'
        self.auth=auth

##  Check URL, Password, header
    def ausgabe(self):
        print(self.url, self.auth,)
#! /bin/python3
import requests
import pickle
import json
import uuid
import faker
#from faker import Factory
import names
import random
import time
import datetime
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .jsons import Json_factory


class OS_request_gen():

    def __init__(self, auth):

        self.json_headers = {
            'content-type': "application/json", 'cache-control': "no-cache"}
        self.zip_headers = {
            'content-type': "application/zip", 'cache-control': "no-cache"}
        self.form_data_headers = {
            'content-type': "form-data", 'cache-control': "no-cache"}
        self.file_headers={
            'cache-control': "no-cache"}

        self.auth = auth
        self.user_name = auth[0]


    def get_request(self, url, stream=False):

        if stream:
            r = requests.request("GET", url, auth=self.auth,
                                 headers=self.zip_headers, stream=stream)
        else:
            r = requests.request("GET", url, auth=self.auth,
                                 headers=self.json_headers)

        return r


    def post_request(self, url, data=None, form_data=False, files=None):

        if form_data:
            r = requests.request("POST", url, data=data, auth=self.auth,
                                 headers=self.form_data_headers)
        if form_data==False and files==None:
            r = requests.request("POST", url, data=data, auth=self.auth,
                                 headers=self.json_headers)
        if files!=None:
            r= requests.request("POST", url, auth=self.auth, 
                                 headers=self.file_headers,files=files)
        return r


    def put_request(self, url, data):

        r = requests.request("PUT", url, data=data, auth=self.auth,
                             headers=self.json_headers)
        return r


    def delete_request(self, url):

        r = requests.request("DELETE", url, auth=self.auth)

        return r


    def head_request(self, url):

        r = requests.request("HEAD", url, auth=self.auth)

        return r

    def user_name(self):

        return self.user_name

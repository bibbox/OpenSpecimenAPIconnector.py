import requests
import json
import pickle
import json
import requests
import uuid
import faker
from faker import Factory
import names
import random
import time
import datetime
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from jsons import Json_factory


class RequestFactory():

    def __init__(self, auth):

        self.json_headers = {'content-type': "application/json", 'cache-control': "no-cache"}
        self.zip_headers = {'content-type': "application/zip", 'cache-control': "no-cache"}
        self.form_data_headers = {'content-type': "form-data", 'cache-control': "no-cache"}

        self.auth = auth

    def get_request(self, url, stream=False):

        if stream:
            r = requests.request("GET", url, auth=self.auth,
                             headers=self.zip_headers, stream=stream)
        else:
            r = requests.request("GET", url, auth=self.auth,
                                 headers=self.json_headers)

        return r

    def get_post_request(self, url, data, form_data=False):

        if form_data:
            r = requests.request("POST", url, data=data, auth=self.auth,
                                 headers=self.form_data_headers)
        else:
            r = requests.request("POST", url, data=data, auth=self.auth,
                                 headers=self.json_headers)
        return r

    def get_put_request(self, url, data):

        r = requests.request("PUT", url, data=data, auth=self.auth,
                             headers=self.json_headers)
        return r
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
import qrcode
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from jsons import Json_factory


class RequestFactory():

    def __init__(self, headers, auth):

        self.headers = headers
        self.down_headers = {'content-type': "application/zip", 'cache-control': "no-cache"}
        self.auth = auth

    def get_request(self, url, stream=False):

        if stream:
            r = requests.request("GET", url, auth=self.auth,
                             headers=self.down_headers, stream=stream)
        else:
            r = requests.request("GET", url, auth=self.auth,
                                 headers=self.headers, stream=stream)

        return r

    def get_post_request(self, url, data):

        r = requests.request("POST", url, data=data, auth=self.auth,
                             headers=self.headers)
        return r

    def get_put_request(self, url, data):

        r = requests.request("PUT", url, data=data, auth=self.auth,
                             headers=self.headers)
        return r
#! /bin/python3


from os_core.url import url_gen
from os_core.jsons import Json_factory
from os_core.institute import institutes

import jsons

class institutes_util:

    def __init__(self, base_url, auth):

        self.institutes = institutes(base_url = base_url, auth = auth)
        self.urls = url_gen()
        self.jsons =Json_factory()

    def create_institute(self, institutename=None):

        params = self.jsons.create_institute(institutename = institutename)
        r = self.institutes.create_institute(params = params)

        return r

    def update_institute(self, instituteid, institutename=None):

        params = self.jsons.create_institute(institutename = institutename)
        r = self.institutes.create_institute(inid =instituteid, params = params)

        return r


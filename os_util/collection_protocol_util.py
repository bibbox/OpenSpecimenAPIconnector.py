#! /bin/python3


from os_core.collection_protocoll import collection_protocol
from os_core.req_util import OS_request_gen
from os_core.jsons import Json_factory
from os_core.url import url_gen

import pandas as pd
import json

class site_util:

    #Konstruktor
    def __init__(self, base_url, auth):

        self.OS_request_gen = OS_request_gen(auth)
        self.jsons = Json_factory()
        self.urls = url_gen()
        self.cps = collection_protocol(base_url = base_url, auth = auth)

    ## Search sites with some parameters
    # Input:    - sitename: A part or the whole Name of the Site in Openspecimen, can also be lists
    #           - institutename: A part or the whole Name of the institue in Openspecimen, can also be lists
    #           - maxresults: Maximum of Results which should be displayed
    #           - siteExtension: boolean if ExtensionDetails should be shown
    # Output:   - 
    def search_cps(self, searchstring = None, title = None, piid = None, reponame = None, startat = none, maxresults = None, detailedlist = None):

        search_string = self.urls.cp_search_url_gen(searchstring = None, title = None, piid = None, reponame = None,
                                                    startat = none, maxresults = None, detailedlist = None)
        
        r = self.cps.search_collection_protocols(search_string = search_string)

        return r

    def merge_cps(self, src_cp, trg_cp):

        data = self.jsons.merge_cps(src_cp = src_cp, trg_cp = trg_cp)
        r = self.cps.merge_colelction_protocols(params = data)

        return r


'''

   def cp_get_cps_json(self):
        endpoint = "/collection-protocols"
        url = self.base_url + endpoint
        r = self.Req_Fact.get_request(url)
        req_json = json.loads(r.text)

        return req_json

    # basic filtering is tolerable on core layer or not ?
    def cp_get_cp_ids(self, record_ids=None):

        endpoint = "/collection-protocols"
        url = self.base_url + endpoint
        r = self.Req_Fact.get_request(url)
        req_json = json.loads(r.text)
        ids = np.zeros(len(req_json))
        for i, item in enumerate(req_json):
            ids[i] = item["id"]

        return ids


    def class_method_module_post_entity_operation(self):
        pass

    def class_method_module_put_entity_operation(self):
        pass

    def class_method_module_delete_entity(self):
        pass'''
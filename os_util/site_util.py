#! /bin/python3

from os_core.site import sites
from os_core.req_util import OS_request_gen
from os_core.jsons import Json_factory

import pandas as pd
import json

class site_util:

    #Konstruktor
    def __init__(self, base_url, auth):

        self.OS_request_gen = OS_request_gen(auth)
        self.jsons = Json_factory()
        self.sites = sites(base_url = base_url, auth = auth)

    ## Search sites with some parameters
    # Input:    - sitename: A part or the whole Name of the Site in Openspecimen, can also be lists
    #           - institutename: A part or the whole Name of the institue in Openspecimen, can also be lists
    #           - maxresults: Maximum of Results which should be displayed
    #           - siteExtension: boolean if ExtensionDetails should be shown
    # Output:   - 
    def search_sites(self, sitename=None, institutename=None, maxresults=100, siteExtension=True):

        search_string = self.jsons.site_search_url_gen(sitename = sitename, institutename = institutename, maxresults = maxresults)
        
        r = self.sites.search_sites(search_string = search_string)

        return r 
        #if siteExtension:




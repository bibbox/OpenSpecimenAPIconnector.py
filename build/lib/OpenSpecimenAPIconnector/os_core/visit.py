#! /bin/python3

# Import
import json
from datetime import datetime

from .req_util import OS_request_gen

class visit:

    def __init__(self, base_url, auth):

        # define class members here
        self.OS_request_gen = OS_request_gen(auth)

        self.base_url = base_url


# Check URL, Password, header
    def ausgabe(self):

        print(self.base_url, self.OS_request_gen.auth)        

#   Add Visit to CP
#   Input:  -params: Paramter as JSON-formatted string
#   Output: - either VISIT details as json formatted string
#           - or  error message with detail whats was wrong
    def add_visit(self, params):

        endpoint = '/visits'
        url = self.base_url + endpoint

        payload = params

        r = self.OS_request_gen.post_request(url, data=payload)

        return json.loads(r.text)


#   Create a Visit and Specimen in one call
#   Input:  - params: Parameter as json formatted string two field "Visit":params for visit, Specimens": params for specimens
#   Output: - either Details of visit and Specimen
#           - or error message with details
# JSON Parse ERROR can be created via add visit and add specimen seperatly
    def add_visit_specimen(self, params):

        endpoint = '/visits/collect'
        url = self.base_url + endpoint

        payload = params

        r = self.OS_request_gen.post_request(url, data=payload)

        return json.loads(r.text)


#   Delete a Visit with id
#   Input:  - visitId:  Id of the visit
#   Output  - either details of the deleted visit as json-formatted string
#           - or error message
    def delete_visit(self, visitid):

        endpoint = '/visits/' + str(visitid)
        url = self.base_url + endpoint

        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)

    
#   Get details of a Visit with id
#   Input:  - visitId:  Id of the visit
#   Output: - either details of the visit as json-formatted string
#           - or error message
    def get_visit(self, visitid):

        endpoint = '/visits/' + str(visitid)
        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


#   Get Visits By Name Or Surgical Pathology Number
#   Input:  - visitname:    Name of the visit
#           - sprnumber:    Surigical Pathology Number
#   Output: - either details of the visit as json formatted string
#           - or error message
    def get_visit_namespr(self, visitname=None, sprnumber=None):

        endpoint = '/visits/bynamespr?'

        if visitname!=None:
            endpoint += 'visitName=' + str(visitname)

        elif sprnumber!=None:
            endpoint += 'sprNumber=' + str(sprnumber)

        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


#   Get Visits By Registration Identifier
#   Input:  - cprid: Collection protocoll REgistration Id
#           - includestats: Default false, if true colletion status of visits
#   Output  - either json-formatted string
#           - or error messages
    def get_visits_cpr(self, cprid, includestats=None):
        
        endpoint = '/visits?cprId=' + str(cprid)
        print(bool(includestats))
        if bool(includestats):
            endpoint += '&includeStats=' + str(includestats)

        url= self.base_url + endpoint

        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)

        
#   Update Visit
#   Input:  - visitid:   ID of the visit
#           - params:   Parameter of the visit which should be updated as json-formatted string
#   Output: - either detail of the updated visit as json-formatted string
#           - or error message with details
    def update_visit(self, visitid, params):

        endpoint = '/visits/' + str(visitid)

        url = self.base_url +endpoint

        payload = params

        r = self.OS_request_gen.put_request(url, payload)

        return json.loads(r.text)

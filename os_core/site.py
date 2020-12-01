#! /bin/python3


import json
from os_core.req_util import OS_request_gen


class sites():

    def __init__(self, base_url, auth):

        self.OS_request_gen = OS_request_gen(base_url, auth)
        
        self.base_url = base_url + '/sites'
        

# Check URL, Password, header

    def ausgabe(self):

        print(self.base_url, self.OS_request_gen.auth)


#   Create Site
#   Input:  - params: Parameter of the Site as json-formatted string
#   Output: - either details of the Institute as json-formatted string
#           - or error message
    def create_sites(self, params):

        url = self.base_url + '/'

        payload = params

        r = self.OS_request_gen.post_request(url, payload)

        return json.loads(r.text)


#   Delete Site
#   Input:  - siid: ID of the Site
#   Output: - either json-formatted string with details of the deleted CP
#           - or error message
    def delete_sites(self, siid):

        endpoint = '/' + str(siid)

        url = self.base_url + endpoint

        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)


# Search Sites, with different parameters.
#   Input:  -json-dict (keys=OpenSpecimenKeys, value= values)
#           - for each key values can either be a single value or a list of values
#           Handle with care, some Params e.g availableQty are not searchable via API
#   Output: -returns: json-formatted string of all Sites wich fullfill searchParams
#           - or an error message
    def search_sites(self, search_params):

        endpoint = '?'

        params = json.loads(search_params)
        keys = params.keys()

        for key in keys:
            if isinstance(params[key],list):
                for param in params[key]:
                    endpoint += str(key)
                    endpoint += '='+str(param)+'&'
            else:
                endpoint += str(key)
                endpoint += '='+str(params[key])+'&'

        endpoint = endpoint[0:-1]

        url = self.base_url+endpoint

        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


#   Get all Sites
#   Output: json-formatted string of all Sites
    def get_all_sites(self):

        url = self.base_url

        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


#   Get site
#   Input:  - siid: Site ID
#   Output: - either json-formatted string with the details
#           - or error message
    def get_collection_protocol(self, siid):

        endpoint = '/' + str(siid)

        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


#   Update Site
#   Input:  - siid: ID of the Site which should get updated
#           - params: Paramters which should get updated
#   Output: - eiher details of the CP as json formatted  string
#           - or error message
    def update_collection_protocol(self, siid, params):

        endpoint = '/' + str(siid)

        url = self.base_url + endpoint

        payload = params

        r = self.OS_request_gen.put_request(url, payload)

        return json.loads(r.text)
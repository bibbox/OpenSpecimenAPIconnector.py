#! /bin/python3


import json
from os_core.req_util import OS_request_gen


class institutes():

    def __init__(self, base_url, auth):

        self.OS_request_gen = OS_request_gen(base_url, auth)
        
        self.base_url = base_url + '/institutes'
        

# Check URL, Password, header

    def ausgabe(self):

        print(self.base_url, self.OS_request_gen.auth)


#   Create CInstitute
#   Input:  - params: Parameter of the Insituee as json-formatted string
#   Output: - either details of the Institute as json-formatted string
#           - or error message
    def create_institute(self, params):

        url = self.base_url + '/'

        payload = params

        r = self.OS_request_gen.post_request(url, payload)

        return json.loads(r.text)


#   Delete Institute
#   Input:  - inid: ID of the Institute
#   Output: - either json-formatted string with details of the deleted CP
#           - or error message
    def delete_institute(self, inid):

        endpoint = '/' + str(inid)

        url = self.base_url + endpoint

        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)


# Search Institutes, with different parameters.
#   Input:  -json-dict (keys=OpenSpecimenKeys, value= values)
#           - for each key values can either be a single value or a list of values
#           Handle with care, some Params e.g availableQty are not searchable via API
#   Output: -returns: json-formatted string of all Insitutes wich fullfill searchParams
#           - or an error message
    def search_institutes(self, search_params):

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


#   Get all Insitutes
#   Output: json-formatted string of all institutes
    def get_all_institutes(self):

        url = self.base_url

        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


#   Get Institute
#   Input:  - inid: Insitute ID
#   Output: - either json-formatted string with the details
#           - or error message
    def get_collection_protocol(self, inid):

        endpoint = '/' + str(inid)

        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


#   Update Insitute
#   Input:  - inid: ID of the Institute which should get updated
#           - params: Paramters which should get updated
#   Output: - eiher details of the CP as json formatted  string
#           - or error message
    def update_collection_protocol(self, inid, params):

        endpoint = '/' + str(inid)

        url = self.base_url + endpoint

        payload = params

        r = self.OS_request_gen.put_request(url, payload)

        return json.loads(r.text)
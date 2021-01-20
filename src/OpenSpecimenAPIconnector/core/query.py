#! /bin/python3


import json
from os_core.req_util import OS_request_gen


class query:

    def __init__(self, base_url, auth):

        self.OS_request_gen = OS_request_gen(auth)
        
        self.base_url = base_url
        

# Check URL, Password, header

    def ausgabe(self):

        print(self.base_url, self.OS_request_gen.auth)


# Create a Query which will be saved in OpenSpecimen
# Input:    - param:  a Json-formatted string of the query using (OS's AQL)
# Output:   - List of Results from the query as json formatted string
#           - or an error message
    def create_query(self, params):

        endpoint = "/saved-queries/"
        url = self.base_url + endpoint

        data = params

        r = self.OS_request_gen.post_request(url,data)

        return json.loads(r.text)


# Executing any AQL
#   Input:  - params: JSON-formatted string with parameters for request
#   Output: - json-formatted string with results
#           - or error message
    def create_aql(self, params):

        endpoint = "/query"
        url = self.base_url + endpoint

        data = params

        r = self.OS_request_gen.post_request(url, data)

        return json.loads(r.text)


#   Getting list of saved queries
#   Input:  -json-dict (keys=OpenSpecimenKeys, value= values)
#           - for each key values can either be a single value or a list of values
#           Handle with care, some Params e.g availableQty are not searchable via API
#   output: -returns: json-formatted string of all specimens wich fullfill searchParams
#
    def search_query(self, search_params=None):

        endpoint = '/saved-queries?'

        if search_params!=None:
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
        print(endpoint)

        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url)

        return  json.loads(r.text)


# Executing a saved Query
#   Input:  - qryid: ID of the query
#           - params: JSON-formatted string with parameters for request
#   Output: - json-formatted string with results
#           - or error message
    def execute_query(self, qryid, params):

        endpoint = "/query/" + str(qryid)
        url = self.base_url + endpoint

        data = params

        r = self.OS_request_gen.post_request(url, data)

        return json.loads(r.text)
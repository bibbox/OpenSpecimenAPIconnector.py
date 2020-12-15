#! /bin/python3
# imports to be cleaned later

import json
from os_core.req_util import OS_request_gen

class collection_protocol():

    def __init__(self, base_url, auth):
        self.OS_request_gen = OS_request_gen(auth)
        self.base_url = base_url + '/collection-protocols'

# Check URL, Password, header

    def ausgabe(self):

        print(self.base_url, self.OS_request_gen.auth)


#   Create Collection Protocol
#   Input:  - params: Parameter of the Collection protocol as json-formatted string
#   Output: - either details of the CP as json-formatted string
#           - or error message
    def create_collection_protocol(self, params):

        url = self.base_url + '/'
        payload = params
        r = self.OS_request_gen.get_request(url)
        return json.loads(r.text)

#   Delete Collection Protocol
#   Input:  - cpid: ID of the collection protocol
#   Output: - either json-formatted string with details of the deleted CP
#           - or error message
    def delete_collection_protocol(self, cpid):

        endpoint = '/' + str(cpid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.delete_request(url)
        return json.loads(r.text)

# Search colelction protocol, with different parameters.
#   Input:  -json-dict (keys=OpenSpecimenKeys, value= values)
#           - for each key values can either be a single value or a list of values
#           Handle with care, some Params e.g availableQty are not searchable via API
#   Output: -returns: json-formatted string of all CPs wich fullfill searchParams
#           - or an error message
    def search_collection_protocols(self, search_params):

        endpoint = '?'

        params = json.loads(search_params)
        keys = params.keys()

        for key in keys:
            if isinstance(params[key],list):
                for param in params[key]:
                    endpoint += str(key)
                    endpoint += '='+str(param)+'&'
            else:        endpoint = '?'

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

#   Get all Collection Protocols
#   Output: json-formatted string of all collection protocol
    def get_all_collection_protocols(self):

        url = self.base_url
        r = self.OS_request_gen.get_request(url)
        return json.loads(r.text)

#   Get Collection Protocol
#   Input:  - cpid: Colletion Protocol ID
#   Output: - either json-formatted string with the details
#           - or error message
    def get_collection_protocol(self, cpid):

        endpoint = '/' + str(cpid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)

#   Merge two Colelction Protocols
#   Input:  - cpShortTitle_src: Collection Protocol Short Title of the Soruce CP
#           - cpshorttitle_tgt: Collection Protocol Short Title of the target CP
#   Output: - 
    def merge_colelction_protocols(self, cpShortTitle_src, cpShortTitle_tgt):

        endpoint = '/merge'
        url = self.base_url + endpoint
        payload = '{\"srcCpShortTitle\":\"' + str(cpShortTitle_src) + \
            '\",\"tgtCpShortTitle\":\"' + str(cpShortTitle_tgt) + '\"}'

        r = self.OS_request_gen.post_request(url, payload)

        return json.loads(r.text)


#   Update colelction Protocol
#   Input:  - cpid: ID of the Colelction Protocol which should get updated
#           - params: Paramters which should get updated
#   Output: - eiher details of the CP as json formatted  string
#           - or error message
    def update_collection_protocol(self, cpid, params):

        endpoint = '/' + str(cpid)
        url = self.base_url + endpoint
        payload = params
        r = self.OS_request_gen.put_request(url, payload)

        return json.loads(r.text)

    def get_cp_pandas_template(self):
        '''
        Input: None
        Returns: pandas data frame of csv template
        :return:
        '''

        site_template_endpoint = "/import-jobs/input-file-template?schema=cp"
        site_template_url = self.base_url + site_template_endpoint
        r = self.OS_request_gen.get_request(site_template_url)
        cp_pandas_template = pd.DataFrame(columns=[r.content.decode()])

        return cp_pandas_template

    def get_cp_def(self, ID):

        cp_endpoint = "/{}/definition".format(ID)
        cp_url = self.base_url + cp_endpoint
        r = self.OS_request_gen.get_request(cp_url)
        cp_def_json = json.loads(r.text)

        return cp_def_json
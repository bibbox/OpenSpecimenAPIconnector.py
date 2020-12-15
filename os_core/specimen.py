#! /bin/python3

# Import
import json
from datetime import datetime

from os_core.req_util import OS_request_gen


class specimen:

    # Constructor
    def __init__(self, base_url, auth):

        # define class members here
        self.OS_request_gen = OS_request_gen(auth)
        self.base_url = base_url

# Check URL, Password, header

    def ausgabe(self):

        print(self.base_url, self.OS_request_gen.auth)

# Get Specimen/s

    def get_specimen(self, specimenId):

        endpoint = '/specimens/' + str(specimenId)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


# Check if Specimen with Label 'xxx' exists

    def check_specimen(self, specimenLabel):

        endpoint = '/specimens?label=' + str(specimenLabel)
        url = self.base_url + endpoint
        r = self.OS_request_gen.head_request(url)

        if r.status_code == 200:
            r = 'Specimen with Label ' + str(specimenLabel) + ' exists.'
        else:
            r = 'Specimen with Label ' + \
                str(specimenLabel) + ' does not exist.'

        return r

# Create Specimen/aliquot/Derivative via API
#   Input:  -params: PArameter as json-formatted string
#   Output: -either specimen_details as json formatted string
#           -or  error message with details as python dict

    def create_specimen_api(self, params):

        endpoint = '/specimens'
        url = self.base_url + endpoint

        payload = params

        r = self.OS_request_gen.post_request(url, data=payload)

        return json.loads(r.text)

# Search specimens, with different parameters.
#   Input:  -json-dict (keys=OpenSpecimenKeys, value= values)
#           - for each key values can either be a single value or a list of values
#           Handle with care, some Params e.g availableQty are not searchable via API
#   output: -returns: json-formatted string of all specimens wich fullfill searchParams
#
    def search_specimens(self, search_params):

        endpoint = '/specimens?'

        params = json.loads(search_params)
        keys = params.keys()

        for key in keys:
            if isinstance(params[key],list):
                for param in params[key]:
                    endpoint += str(key)
                    endpoint += '='+str(param)+'&'
            else:
                endpoint += str(key)
                endpoint += '=' + str(params[key])+'&'

        endpoint = endpoint[0:-1]
        url = self.base_url+endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


# Update Specimen with Id
#   Input:  - specimenid Id of the specimen
#           - updateparams: Parameter to update as json_formatted string
#   Output: - Specimen Details, with updated params as python dict
#           - error message as python dict

    def update_specimen(self, specimenid, updateparams):

        endpoint = '/specimens/'+str(specimenid)
        url = self.base_url + endpoint
        data = updateparams
        r = self.OS_request_gen.put_request(url, data)
        return json.loads(r.text)

#   Delete Specimen with id
#       Input:  - specimenid: Id of specimen which should get deleted as value or list of values
#       Output: - Details of the specimen as python dict
#               - or error message as python dict

    def delete_specimen(self, specimenid):

        endpoint = '/specimens?id='
        if isinstance(specimenid, list):
            for spec_id in specimenid:
                endpoint += str(spec_id) + ','
            endpoint = endpoint[0:-1]
        else:
            endpoint += str(specimenid)

        url = self.base_url + endpoint
        r = self.OS_request_gen.delete_request(url)
        return json.loads(r.text)


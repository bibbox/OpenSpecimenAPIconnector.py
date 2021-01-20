#! /bin/python3

# Import
import json

from os_core.req_util import OS_request_gen

class collection_protocol_registration:

    def __init__(self, base_url, auth):

        # define class members here
        self.OS_request_gen = OS_request_gen(auth)
        self.base_url = base_url + '/collection-protocol-registrations'


#   Check URL, Password, header
    def ausgabe(self):

        print(self.base_url, self.OS_request_gen.auth)


#   CreateParticipant
#   Input:  - params:   json-formatted string with Parameter for the participant 
#   Output: - either details of the participant as json-formatted string
#           - or detailed error message
    def create_participant(self, params):

        url = self.base_url + '/'
        payload = params
        r = self.OS_request_gen.post_request(url, payload)
        return json.loads(r.text)


#   Delete Consent form
#   Input:  - cprid:   REgistration ID of a participant
#   Output: - status Code
    def delete_consent(self, cprid):

        endpoint = '/' + str(cprid) + '/consent-form'
        url = self.base_url + endpoint
        r = self.OS_request_gen.delete_request(url)
        return json.loads(r.text)


#   Delete Participant
#   Input:  - cprid:    Registration ID of a participant
#   Output: - either details of the participant
#           - or error message
    def delete_participant(self, cprid):

        endpoint = '/' + str(cprid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.delete_request(url)
        return json.loads(r.text)


#   Download Consent form
#   Input:  - cprid:    Registration ID of a participant
#   Output: - either binary file contents
#           - or error message
    def download_consent_form(self, cprid):

        endpoint = '/' + str(cprid) + '/consent-form'
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)
        return r


#   Get Consent
#   Input:  - cprid:    Registration ID of a participant
#   Output: - either consent details
#           - or error message
    def get_consents(self, cprid):

        endpoint = '/' + str(cprid) + '/consents'
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)
        return r


#   Get registration
#   Input:  - cprid:    Registration ID of a participant
#   Output: - either details of the Participant as json-formatted string
#           - or error message
    def get_registration(self, cprid):

        endpoint = '/' + str(cprid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)
        return json.loads(r.text)

    
#   Get matching participants
#   Input:  - params:   json-formatted string with Paramter to search
#   Output: - details of the participants as json-formatted string
    def get_registrations(self, params):

        endpoint = '/list'
        url = self.base_url + endpoint
        payload= params
        r = self.OS_request_gen.post_request(url, payload)
        return json.loads(r.text)

#   Register Participant to another protocol
#   Input:  - params:   json-formatted string with parameter of participant and new CP
#   Output: - either details of the participant and the new CP
#           - or error message       
    def register_to_cp(self, params):

        url = self.base_url + '/'
        payload = params
        r = self.OS_request_gen.post_request(url, payload)
        return json.loads(r.text)


#   Merging  Participant
#   Input:  - id_from:  Participant ID from which get merged
#           -   id_to:  Participant ID to which get mercged
#   Output: - either detailes of the merged participant
#           - or error message
    def merge_participants(self, id_from, id_to):

        endpoint = '/'+ str(id_from)
        url = self.base_url + endpoint
        payload = '{\"participant\":{\"id\":\"' + str(id_to) + '\"}}'
        r = self.OS_request_gen.put_request(url, payload)
        return json.loads(r.text)

    
#   Updating Participant
#   Input:  - cprId:    Registration ID of the Participant
#           - params:   Paramter of the Participant to be updated
#   Output: - either details of the updated Participant
#           - or error message
    def update_participant(self, cprid, params):

        endpoint = '/' + str(cprid)
        url = self.base_url + endpoint
        payload = params
        r = self.OS_request_gen.put_request(url, payload)
        return json.loads(r.text)


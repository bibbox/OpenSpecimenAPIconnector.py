#! /bin/python3

# Import
import json

from os_core.req_util import OS_request_gen

class collection_protocol_event:

    def __init__(self, base_url, auth):

        # define class members here
        self.OS_request_gen = OS_request_gen(auth)
        self.base_url = base_url + '/collection-protocol-events'


#   Check URL, Password, header
    def ausgabe(self):

        print(self.base_url, self.OS_request_gen.auth)


#   Create Collection Protocol Event
#   Input:  - params: Parameter of the event as json-formatted string
#   Output: - either details of the event as json-formatted string
#           - or error message
    def create_event(self, params):

        url = self.base_url
        payload = params
        r = self.OS_request_gen.post_request(url, payload)

        return json.loads(r.text)


#   Delete Collection Protocol Event
#   Input:  - eventid: ID of the event which should be deleted
#   Output: - either details of the deleted event
#           - or error message
    def delete_event(self, eventid):

        endpoint = '/' + str(eventid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)


#   Get all Events of a collection Protocol
#   Input:  - cpid: Collection Protocol ID
#   Output: - either details of events assigned to a CP as json-formatted string
#           - or error message
    def get_all_events(self, cpid):

        endpoint = '?cpId=' + str(cpid)
        url= self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


#   Get Event with ID
#   Input:  - eventid: ID of the event
#   Output: - either details as json-formatted string of the Event
#           - or error message
    def get_event(self, eventid):

        endpoint = '/' + str(eventid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


#   Update Event with ID
#   Input:  - eventid: Id of the Event which should get updated
#           - params: Parameter of the Event which should get updated
#   Output: - either details of the updated event as jsoon-formatted string
#           - or error message
    def update_event(self, eventid, params):

        endpoint = '/' + str(eventid)
        url = self.base_url + endpoint
        payload = params
        r = self.OS_request_gen.get_request(url, payload)

        return json.loads(r.text)
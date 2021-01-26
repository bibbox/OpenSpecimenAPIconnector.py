#! /bin/python3

# Import
import json
from datetime import datetime

from .req_util import OS_request_gen

class participant:

    def __init__(self, base_url, auth):

        # define class members here
        self.OS_request_gen = OS_request_gen(auth)

        self.base_url = base_url


# Check URL, Password, header
    def ausgabe(self):

        print(self.base_url, self.OS_request_gen.auth)        

# Get Participants
#   Input:  - ppid: Participant Protocoll ID
#   Output: - either json-formatted string of Participant with ppid
#           - or detailed error message
    def get_participant(self, ppid):

        endpoint = '/participants/' + str(ppid)

        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


# Get matsching Participants
#   Input:  - params: Json-formatted string with params to search
#   Output: - either json-formatted string of participants
#           - or detailed error message
    def get_participant_matches(self, params):

        endpoint = '/participants/match'

        url = self.base_url + endpoint

        payload=params

        r = self.OS_request_gen.post_request(url,data=payload)

        return json.loads(r.text)

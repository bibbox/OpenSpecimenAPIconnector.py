#! /bin/python3

from os_core.collection_protocol_event import collection_protocol_event
from os_core.req_util import OS_request_gen
from os_core.jsons import Json_factory
import json
import io
import pandas
import time

class cpevent_util:

    #   Constructor
    def __init__(self, base_url, auth):

        self.event = collection_protocol_event(base_url=base_url, auth=auth)
        self.jsons = Json_factory()

    #Create Event
    def create_event(self, label, point, cp, site, diagnosis,status,activity,unit, code):

        params = self.jsons.create_cp_event_json(label,point,cp,site,diagnosis,status,activity,unit,code)
        r = self.event.create_event(params)

        return r
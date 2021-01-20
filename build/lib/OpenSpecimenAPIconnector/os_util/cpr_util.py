#! /bin/python3

from os_core.collecttion_protocol_registration import collection_protocol_registration
from os_core.req_util import OS_request_gen
from os_core.jsons import Json_factory
import json
import io
import pandas
import time

class cpr_util:

    #Konstruktor
    def __init__(self, base_url, auth):

        self.cpr = collection_protocol_registration(base_url=base_url, auth=auth)
        self.jsons = Json_factory()


    #Get Registrations
    def get_registrations(self, cpid=None, registrationdate=None, ppid=None, name=None, birthdate=None,
                            uid=None, specimen=None, includestats=None, startat=None, maxresults=None):

        params = self.jsons.get_registrations(cpid, registrationdate, ppid, name, birthdate, uid, specimen, includestats, startat, maxresults)

        r = self.cpr.get_registrations(params)

        return r
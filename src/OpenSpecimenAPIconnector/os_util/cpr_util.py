#! /bin/python3

from ..os_core.collection_protocol_registration import collection_protocol_registration
from ..os_core.req_util import OS_request_gen
from ..os_core.jsons import Json_factory
from ..os_core.participant import participant
import json
import io
import pandas
import time

class cpr_util:

    #Konstruktor
    def __init__(self, base_url, auth):

        self.cpr = collection_protocol_registration(base_url=base_url, auth=auth)
        self.participant = participant(base_url = base_url, auth = auth)
        self.jsons = Json_factory()


    #Get Registrations
    def get_registrations(self, cpid=None, registrationdate=None, ppid=None, name=None, birthdate=None,
                            uid=None, specimen=None, includestats=None, startat=None, maxresults=None):

        params = self.jsons.get_registrations(cpid, registrationdate, ppid, name, birthdate, uid, specimen, includestats, startat, maxresults)

        r = self.cpr.get_registrations(params)

        return r

    def get_participants(self, lastname=None, uid = None, birthdate = None, pmi = None, empi = None, reqreginfo = None):

        params = self.jsons.get_participants(lastname = lastname, uid = uid, birthdate = birthdate,
                                            pmi = pmi, empi = empi, reqreginfo = reqreginfo)

        r = self.participant.get_participant_matches(params)

        return r

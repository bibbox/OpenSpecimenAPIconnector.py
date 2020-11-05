import requests
import json
import pickle
import json
import requests
import uuid
import faker
from faker import Factory
import names
import random
import time
import datetime
import qrcode
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Cp_factory():

    def __init__(self, base_url, Json_Fact, Req_Fact, File_Fact, Site_Fact, Form_Fact):

        self.base_url = base_url
        self.Req_Fact = Req_Fact
        self.File_Fact = File_Fact
        self.Json_Fact = Json_Fact
        self.Site_Fact = Site_Fact
        self.Form_Fact = Form_Fact

    def create_CP(self, data):
        pass

    def get_all_cp_ids(self, record_ids=None):

        endpoint = "/collection-protocols"
        url = self.base_url + endpoint
        r = self.Req_Fact.get_request(url)
        req_json = json.loads(r.text)
        ids = np.zeros(len(req_json))
        for i, item in enumerate(req_json):
            ids[i] = item["id"]

        return ids

    ##TODO: Create simpler flag if a CP is a active BBMRI Collection and get rid of if method not useable

    def get_BBMRI_cp_defs(self, pandas=True):

        cp_ids = self.get_all_cp_ids()
        cps = []
        for i, idx in enumerate(cp_ids):
            break
            cp = self.get_cp_def(idx)
            # if something:
                # cps.append(cp)

        return cps

    def get_all_cp_defs(self, pandas=True):
        
        cp_ids = self.get_all_cp_ids()
        cps = []
        for i, idx in enumerate(cp_ids):
            cp = self.get_cp_def(idx)
            if pandas:
                cp = self.File_Fact.pandas_from_jsom
            
            cps.append(cp)

        return cps

    def get_cp_def(self, ID):

        cp_endpoint = "rest/ng/collection-protocols/{}/definition".format(ID)
        cp_url = self.base_url + cp_endpoint
        r = self.Req_Fact.get_request(cp_url, stream=True)
        cp_def_json = json.loads(r.text)
        print(json.dumps(req_json, indent=4, sort_keys=True))
        
        return cp_def_json
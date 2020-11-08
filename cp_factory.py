import requests
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
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import tempfile

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

    ##TODO find best uploading way of uploading new CP's to OS ---> Check documentation and decide
    ## Decide how to handle custom CP variations and find common generic source data format to be converted
    ## to pandas dataframe.

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

    def get_cp_pandas_template(self):

        cp_template_endpoint = "/import-jobs/input-file-template?schema=cp"
        cp_template_url = self.base_url + cp_template_endpoint
        r = self.Req_Fact.get_request(cp_template_url)
        cp_pandas_template = pd.DataFrame(columns=[r.content.decode()])

        return cp_pandas_template

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

    def get_all_cp_defs_json(self, pandas=True):
        
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
        r = self.Req_Fact.get_request(cp_url)
        cp_def_json = json.loads(r.text)
        print(json.dumps(req_json, indent=4, sort_keys=True))
        
        return cp_def_json
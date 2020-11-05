import requests
import json
import pickle
import numpy as np
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
import pandas as pd
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from request_factory import RequestFactory
from jsons import Json_factory
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import zipfile
import tempfile


class SiteFactory():

    def __init__(self, base_url, Json_Fac, Req_Fac, File_Fact):

        self.base_url = base_url
        self.Json_Fac = Json_Fac
        self.Req_Fac = Req_Fac
        self.File_Fact = File_Fact

    def get_all_site_ids(self, record_ids=None):

        endpoint = "/sites"
        url = self.base_url + endpoint
        r = self.Req_Fac.get_request(url)
        req_json = json.loads(r.text)
        ids = np.zeros(len(req_json))
        for i, item in enumerate(req_json):
            ids[i] = item["id"]

        return ids
    
    ##TODO: Create simpler flag if a Site is a active BBMRI BIOBANK and get rid of if
    
    def get_BBMRI_sites_json(self, pandas=True):

        site_ids = self.get_all_site_ids()
        sites = []
        for i, item in enumerate(site_ids):
            endpoint = "/sites/{}".format(item)
            url = self.base_url + endpoint
            r = self.Req_Fac.get_request(url)
            req_json = json.loads(r.text)
            print(json.dumps(req_json, indent=4, sort_keys=True))
            if req_json["extensionDetail"].get("attrs", False) and \
                    "miabis" in req_json["extensionDetail"]["formCaption"].lower():
                if pandas:
                    sites.append(self.File_Fact.pandas_from_json)
                print(json.dumps(req_json, indent=4, sort_keys=True))
                input()

        return sites

    def get_all_sites(self, pandas=True):

        job_endpoint = "/export-jobs/"
        job_url = self.base_url + job_endpoint
        data = self.Json_Fac.create_site_export_job_json()
        r = self.Req_Fac.get_post_request(job_url, data)
        print(r.text)

        req_json = json.loads(r.text)
        job_id = req_json["id"]
        job_out_endpoint = "/export-jobs/{}/output".format(job_id)
        job_out_url = self.base_url + job_out_endpoint
        print(job_out_url)
        r = self.Req_Fac.get_request(job_out_url, stream=True)
        with tempfile.SpooledTemporaryFile(mode="wb") as fp:
            fp.write(r.content)
            with zipfile.ZipFile(fp, 'r', zipfile.ZIP_DEFLATED) as archive:
                with archive.open("output.csv", "r") as csv_file:
                    if pandas:
                        site_data = pd.read_csv(csv_file)
                    else:
                        site_data = csv_file

        return site_data
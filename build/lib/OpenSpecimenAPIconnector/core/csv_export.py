import pandas as pd
import zipfile
import json
import io
import requests
import json
import tempfile
import os

from datetime import datetime

from os_core.req_util import OS_request_gen

class CSV_exporter():

    def __init__(self, base_url, auth):
        # define class members here
        self.OS_request_gen = OS_request_gen(auth)
        self.base_url = base_url
        self.auth = auth

    def create_export_job(self, data):

        job_endpoint = "/export-jobs/"
        job_url = self.base_url + job_endpoint
        r = self.OS_request_gen.post_request(job_url, data)
        req_json = json.loads(r.text)
        job_id = req_json["id"]
        
        return job_id

    def get_job_output(self, job_id):

        job_out_endpoint = "/export-jobs/{}/output".format(job_id)
        job_out_url = self.base_url + job_out_endpoint

        r = self.OS_request_gen.get_request(job_out_url, stream=True)
        with open("testfile", "wb") as fp:
            fp.write(r.content)
        with zipfile.ZipFile("testfile", "r") as archive:
            job_data = archive.open("output.csv", "r")
            job_data = pd.read_csv(job_data)
        os.remove("testfile")

        return job_data





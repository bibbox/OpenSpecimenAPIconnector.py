#! /bin/python3

import pandas
import json
import io
import requests

from datetime import datetime

from os_core.req_util import OS_request_gen


class csv_bulk:

    # Constructor

    def __init__(self, base_url, auth):

        # define class members here
        self.OS_request_gen = OS_request_gen(auth)

        self.base_url = base_url + '/import-jobs'
        self.auth = auth


# Check URL, Password, header

    def ausgabe(self):

        print(self.base_url, self.OS_request_gen.auth)

# Get template_file, return pandas Dataframe

    def get_template(self, schemaname):

        endpoint = '/input-file-template?schema=' + str(schemaname)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        data = io.StringIO(r.text)
        ret_val = pandas.read_csv(data, sep=",")

        return ret_val

# Upload the CSV file

    def upload_csv(self, filename, file):

        endpoint = '/input-file'
        url = self.base_url + endpoint
        files = [('file', (filename, file, 'text/csv'))]
        headers = {'cache-control': "no-cache"}

        r = self.OS_request_gen.post_request(url=url, files=files)

        return json.loads(r.text)["fileId"]

#  create and run job

    def run_upload(self, schemaname, fileid, operation='CREATE'):

        url = self.base_url
        payload = '{\"objectType\":\"'+schemaname+'\",\"importType\":\"' + \
            operation+'\",\"inputFileId\":\"'+fileid+'\"}'

        r = self.OS_request_gen.post_request(url, data=payload)

        return r.text

#   get job status
    def get_job_status(self, jobid):

        endpoint = '/'+ str(jobid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return r.text

#   downlaod job report
    def job_report(self, jobid):
        endpoint = '/' + str(jobid) + '/output'
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)
        return r.text

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


# Check URL, Password

    def ausgabe(self):

        print(self.base_url, self.OS_request_gen.auth)


#   Get template_file, return pandas Dataframe
#       -schemaname:   https://docs.google.com/spreadsheets/d/1fFcL91jSoTxusoBdxM_sr6TkLt65f25YPgfV-AYps4g/edit#gid=0
#           e.g. specimen,masterSpecimen (camelCase)  

    def get_template(self, schemaname):

        endpoint = '/input-file-template?schema=' + str(schemaname)
        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url)

        data = io.StringIO(r.text)
        ret_val = pandas.read_csv(data, sep=",",encoding='UTF-8', engine='python')

        return ret_val


#   Upload the CSV file, returns fileId for upload job
#       - filename: string of the filename with ending
#       - file: file with datatyp .csv (OS standard separator is comma ',')

    def upload_csv(self, filename, file):

        endpoint = '/input-file'
        url = self.base_url + endpoint
        files = [('file', (filename, file, 'text/csv'))]

        r = self.OS_request_gen.post_request(url=url, files=files)

        return json.loads(r.text)["fileId"]


#   create and run job, returns json file with job id etc.
#       - schemaname: string with name of Inputtype https://docs.google.com/spreadsheets/d/1fFcL91jSoTxusoBdxM_sr6TkLt65f25YPgfV-AYps4g/edit#gid=0
#       - fileId: ID formatted Text which is generated in os_core.csv_bulk.upload_csv
#       - operation: UPDATE or CREATE
#       - dateformat: optional, needed if Format is incompatibel with OS systemconfiguration
#       - timeformat: optional, needed if Format is incompatibel with OS systemconfiguration

    def run_upload(self, schemaname, fileid, operation='CREATE',dateformat=None, timeformat=None):

        url = self.base_url
        payload = '{\"objectType\":\"'+schemaname+'\",\"importType\":\"' + \
            operation+'\",\"inputFileId\":\"'+fileid+'\"}'

        r = self.OS_request_gen.post_request(url, data=payload)

        return (json.loads(r.text)["id"], r.text)


#   get job status, returns status code
#       - 200:Bulk Import request was successfully processed.
#       - 401:uthorisation failed, user doesn’t have the authority.
#       - 500:Internal server error, encountered server error while performing operations.
#       - jobid= Id of the job

    def get_job_status(self, jobid):

        endpoint = '/'+ str(jobid)
        url = self.base_url + endpoint
        
        r = self.OS_request_gen.get_request(url)

        return r.text


#   downlaod job report, generates json output of the import job
#   last row of the csv contains information about upload.
#       - jobid= Id of the job

    def job_report(self, jobid):

        endpoint = '/' + str(jobid) + '/output'
        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url)

        return r.text

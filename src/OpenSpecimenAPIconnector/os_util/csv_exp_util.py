#! /bin/python3

from os_core.csv_export import CSV_exporter
from os_core.req_util import OS_request_gen
from os_core.jsons import Json_factory
import json
import io
import pandas
import time

class csv_export:

    # Constructor
    def __init__(self, base_url, auth):

        self.export = CSV_exporter(base_url = base_url, auth = auth)
        self.json = Json_factory()


    def cp_csv_export(self, objecttype, cpid, entitytype=None, formname=None):

        data = self.json.create_cp_csv_export_job(objecttype = objecttype, cpid = cpid,
                entitytype = entitytype, formname = formname)
        
        job_id = self.export.create_export_job(data = data)

        job = self.export.get_job_output(job_id = job_id)

        return job

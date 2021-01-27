import json
import io
import requests
import json
import tempfile
import time

from ..os_core.csv_export import CSV_exporter
from ..os_core.jsons import Json_factory
from ..os_core.req_util import OS_request_gen

class Export_OP():

    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth
        self.Json_fac = Json_factory()
        self.exporter = CSV_exporter(self.base_url, self.auth)

    def export_file(self, entity=None, param=None):
        '''
        export a given OS Entity line specimes to a CSV file

        :param entity: The Entity we wanna export Specimens Etc
        :param param:
        :return:
        '''
        # temporary solution until template file handling is clear

        if entity == "institute":
            pass
        elif entity == "user":
            pass
        elif entity == "site":
            data = self.Json_fac.create_site_export_job_json(record_ids=param)
        elif entity == "cpr":
            data = self.Json_fac.create_cpr_export_job_json(cp_id=param)

        job_id = self.exporter.create_export_job(data)
        export_file = self.exporter.get_job_output(job_id)

        return export_file

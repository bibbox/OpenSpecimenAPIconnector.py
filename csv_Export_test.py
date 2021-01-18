#! /bin/python3

#### This is for testing reasons online


from os_core.csv_export import CSV_exporter
from os_core.jsons import Json_factory
from os_core.req_util import OS_request_gen

from os_util.csv_exp_util import csv_export


import json
import pandas

# base_url='http://biobank.silicolab.bibbox.org/'
base_url = 'http://biobank-7-2.silicolab.bibbox.org/openspecimen/rest/ng'
auth = ('admin', 'Login@123')

exp_job = csv_export(base_url = base_url, auth = auth)


# Export Participants
jobfile = exp_job.cp_csv_export(objecttype = "cpr", cpid = "18")
print(jobfile)


# Export MIABIs Contact Information
jobfile = exp_job.cp_csv_export(objecttype = "extensions", cpid = "18", entitytype = "Participant", formname =  "contactInformation")
print(jobfile)

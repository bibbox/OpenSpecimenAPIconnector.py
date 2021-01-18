#! /bin/python3

from os_core.site import sites
from os_core.jsons import Json_factory
from os_core.users import users
from os_core.collecttion_protocol_registration import collection_protocol_registration
from os_core.collection_protocoll import collection_protocol

import json
import pandas as pd

# URL to OpenSpecimen and Logindata
base_url = 'http://biobank-7-2.silicolab.bibbox.org/openspecimen/rest/ng'
auth = ('admin', 'Login@123')

# Load headers of BBMRI_ERIC Directory
template_file_name="empty_eric_duo.xlsx"
biobank_header = pd.read_excel(template_file_name, sheet_name = "eu_bbmri_eric_biobanks")
collection_header = pd.read_excel(template_file_name, sheet_name="eu_bbmri_eric_collections")
person_header = pd.read_excel(template_file_name, sheet_name = "eu_bbmri_eric_persons")

print(type(collection_header))

biobank_header_json=biobank_header.to_json()
print(type(biobank_header_json))
print(biobank_header_json)

#load Openspecimen Collection Protocols
protocols = collection_protocol(base_url = base_url, auth = auth)
cp = protocols.get_collection_protocol(cpid = "18")
print(cp)
print('##########')
print(cp["principalInvestigator"])
print('##########')
print(cp["extensionDetail"])

# write headers to json



'''


cps=protocols.get_all_collection_protocols()
#print(cps)


print(cp)

'''
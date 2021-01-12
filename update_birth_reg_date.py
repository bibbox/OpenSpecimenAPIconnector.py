#! /bin/python3

#### This is for testing reasons online


from os_core.users import users
from os_core.specimen import specimen
from os_core.mandatory import mark_mandatory
from os_core.csv_bulk import csv_bulk
from os_core.visit import visit
from os_core.participant import participant
from os_core.collection_protocoll import collection_protocol
from os_core.collecttion_protocol_registration import collection_protocol_registration
from os_core.collection_protocol_event import collection_protocol_event
from os_core.query import query

from os_util.cpevent_util import cpevent_util
from os_util.bulk_operations import bulk_operations
from os_util.query_util import query_util
from os_util.cpr_util import cpr_util
from os_util.visit_util import visit_util
from faker import Faker
import json
import pandas
import random
import datetime


#base_url='http://biobank.silicolab.bibbox.org/openspecimen/rest/ng'
base_url='http://biobank-7-2.silicolab.bibbox.org/openspecimen/rest/ng'
#base_url = 'http://localhost:9013/openspecimen/rest/ng'
auth = ('admin', 'Login@123')
print('#1')
#Constants:
CPTitle="Hellenic Biobank of Overweight and Obesity in Childhood and Adolescence"
#CPTitle="Main collection of Clinical-biological Biobank at INAB, comprising of all the samples."
SiteName="Hellenic Biobank for Parkinson\'s Disease"
#SiteName="Clinical-biological Biobank at INAB affiliated with Hematology Department and HCT Unit, ?G. Papanicolaou? Hospital, Thessaloniki, Greece"

print('#2')
#Get cprId via Query
qry =query_util(base_url=base_url, auth=auth)
exqry = qry.create_aql(cpid=17, aql='select Participant.id where CollectionProtocol.id = 17')
cprID=exqry['rows']
print('#4')
#generate visit's and specimens
part = collection_protocol_registration(base_url=base_url, auth=auth)
fake = Faker()
start_date = datetime.date(year=2010, month=1, day=1)
for ID in cprID:
    params={"participant":{"birthDate": str(fake.date_between(start_date='-90y', end_date='-5y'))},
            "registrationDate": str(fake.date_between(start_date=start_date, end_date='today'))}
    params=json.dumps(params)
    partici=part.update_participant(ID[0],params)
    print(partici)

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
import json
import pandas
import random

base_url='http://biobank.silicolab.bibbox.org/openspecimen/rest/ng'
#base_url='http://biobank-7-2.silicolab.bibbox.org/openspecimen/rest/ng'
#base_url = 'http://localhost:9013/openspecimen/rest/ng'
auth = ('admin', 'Login@123')
print('#1')
#Constants:
#CPTitle="Hellenic Biobank of Overweight and Obesity in Childhood and Adolescence"
CPTitle="Main collection of Clinical-biological Biobank at INAB, comprising of all the samples."
#SiteName="Hellenic Biobank for Parkinson\'s Disease"
SiteName="Clinical-biological Biobank at INAB affiliated with Hematology Department and HCT Unit, “G. Papanicolaou” Hospital, Thessaloniki, Greece"
Type=[['Plasma','Fluid'],['Serum','Fluid'],['DNA','Molecular'],['Cell - Not Specified', 'Cell'],
    ['Tissue - Not Specified','Tissue'],['Lavage','Fluid'],['Slide','Cell'],['protein','Molecular'],['Fresh Tissue','Tissue']]
print('#2')
#generate Event
#event = cpevent_util(base_url,auth)
#evt =event.create_event(label="Base Event", point=0,cp=CPTitle, site=SiteName, diagnosis= "Not Specified",
#                        status="Not Specified", activity="Active", unit="DAYS", code="Event")
#print(evt)
eventid=4#evt['id']
print('#3')
#Get cprId via Query
qry =query_util(base_url=base_url, auth=auth)
exqry = qry.create_aql(cpid=9, aql='select Participant.id where CollectionProtocol.id = 9')
cprID=exqry['rows']
print('#4')
#generate visit's and specimens
vis = visit_util(base_url=base_url, auth=auth)
for ID in cprID:
    typ=Type[random.randrange(8)]
    label = 'specimen'+str(ID[0])
    visitname="visit"+str(ID[0])
    specisit= vis.add_visit_speci(cprid=ID[0], name=visitname, site=SiteName, eventid=eventid, visit_id=None, av_qty= 10, user=None,
                            lineage = "New", init_qty=10, spec_class=typ[1], spec_type=typ[0], anat_site=None,speclabel=label)
    print(specisit)
    
#print(specisit)


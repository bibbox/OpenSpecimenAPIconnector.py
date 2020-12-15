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
<<<<<<< HEAD
=======
from os_core.query import query
>>>>>>> dev_chri


from os_util.bulk_operations import bulk_operations
from os_util.query_util import query_util
import json
import pandas

# base_url='http://biobank.silicolab.bibbox.org/'
base_url = 'http://localhost:9013/openspecimen/rest/ng'
auth = ('admin', 'Login@123')


## User test
# user = users(base_url, auth)
# user.ausgabe()
# user_info = user.get_user(3)
# print(user_info)
# alluser = user.get_all_users()
# print(alluser)
# user_info=user.assign_role(3, 1,1, 'Coordinator')
# print(user_info)
# user_info=user.change_password(3,'Login@1234')
# print(user_info)

# user_info = user.create_user(dnd='false', firstname='Max', lastname='Mustermann', emailaddress='error@404.com',
# phonenumber = '0640123456', domainname='openspecimen', loginname='Max', institutename='Biobank Institute',
# type='SUPER', address='Address' ,activitystatus='Active')
# user_info = user.delete_user(12)
# user_info = user.get_roles(3)
# print(user_info)
# speci = specimen(base_url,auth)
# speci.ausgabe()

## Specimentest
# speci = specimen(base_url=base_url, auth=auth)
# speci.ausgabe()
# speci_info = speci.get_specimen(1)
# print(speci_info)
# speci_info = speci.check_specimen(specimenLabel='asd')
# print(speci_info)
#
# speci_info = speci.create_specimen_api(label='label2',cpId=2,specimenClass='Fluid',specimenType='Bile',
# pathology = 'Malignant',anatomicSite='Abdomen, NOS',
# laterality = 'Bilateral',lineage='New',status='Collected')
# print(speci_info)
# speci_info = speci.search_specimens(labels=['Jupyter'])
# print(speci_info)
# param = {}
# param['status']='Collected'
# param['reason']='BecauseIcan'
# updateparam = json.dumps(param)
# print(type(updateparam))
# print(json.loads(updateparam).keys())
# test='testos'
# print(test[0:-1])
# search = {}
# search['label']='Jupyter1'
# search['id'] = [1,2]
# print(search)
# search['id_'] = 2
# print(search)
# search['exactMatch'] = 'true'
# searchpar = json.dumps(search)
# speci_info = speci.search_specimens(searchpar)
# print(speci_info)
# speci_info = speci.delete_specimen(specimenid=[4,5])
# print(speci_info)
# speci_info = speci.update_specimen(specimenid=7,updateparams=updateparam)
# print(speci_info)

# csvfiles = csv_bulk(base_url,auth)
# csvfiles.ausgabe()
# file = csvfiles.get_template(schemaname='specimen')
# file.to_csv('specimen2.csv')
# print('##### filestart #####')
# print(file)
# print('##### fileend #####')
# print(len(file))
# print(type(file))
# input_= pandas.read_csv('/home/v/Programs/BBMRI_API/dev_chri/specimen.csv')
# file_id = csvfiles.upload_csv(filename='specimen.csv',file=input_.to_csv(index=None))
# uplo = csvfiles.run_upload(schemaname='specimen',fileid=file_id)
# stat = csvfiles.get_job_status(12)
# status = csvfiles.job_report(12)
# open(file)

# bulk_op = bulk_operations(base_url,auth)
# input_= pandas.read_csv('/home/v/Programs/BBMRI_API/dev_chri/specimen.csv')
# print('#### filestart #####')
# print('specimen.csv')
# print(input_)
# print('#### fileend ####')
# uplo = bulk_op.bulk_import(file=input_.to_csv(index=None),filename='specimen.csv',schemaname='specimen',operation='UPDATE')
# print(uplo)

# print(json.loads('nothing searched'))

# vis = visit(base_url=base_url, auth=auth)
# vis.ausgabe()

# params = '{\"name\":\"API-TEST1\",\"site\":\"Biobank Site\",\"ppid\":\"PPID2\",\"cpShortTitle\":\"PT\"}'

# addedvisit=vis.add_visit(params)
# print(addedvisit)

# params='{\"visit\":\n{\"name\":\"API-TEST-VISIT\",\"site\":\"Biobank Site\",\"ppid\":\"PPID2\",\"cpShortTitle\":\"PT\"},\n\
# \"specimens\":\n[\"label\":\"visittest\",\"lineage\":\"New\",\"status\":\"Collected\",\"initalQty\":\"10\",\"reqId\":\"1\",\
# \"specimenClass\":\"Fluid\",\"type\":\"Bile\",\"createdOn\":\"2020-30-11\",\"pathology\":\"Malignant\",\"atomicSite\":\"Abdomen, NOS\",\"laterality\":\"Bilateral\",\
# \"collectionEvent\":{\"user\":{\"id\":\"2\"},\"time\":\"2020-30-11\"},\
# \"receivedEvent\":{\"user\":{\"id\":\"2\"},\"time\":\"2020-30-11\"}]}'
# print(params)

#            ,\"createdOn\":\"' + now + '\",\"collectionEvent\":{\"user\":{\"id\":\"'+ str(userId) + '\"},\"time\":\"' \
#            + now + '\"},\"receivedEvent\":{\"user\":{\"id\":\"' + str(userId) +'\"},\"receivedQuality\":\"Acceptable\",\"time\":\"' \
#            + now + '\"},\"specimenClass\":\"' + str(specimenClass) +'\",\"type\":\"' + str(specimenType) + '\",\"pathology\":\"' + str(pathology) + '\",' \
#            + '\"anatomicSite\":\"'+ str(anatomicSite) + '\",\"laterality\":\"' + str(laterality) +'\"}'

# TODO:addedspecivisit=vis.add_visit_specimen(params=params)
# deleted_visit = vis.delete_visit(5)
# print(deleted_visit)
# visit_detail = vis.get_visit_namespr(visitname='visit01')
# print(visit_detail)
# visit_detail = vis.get_visit_namespr(sprnumber=123)
# print(visit_detail)
# visit_detail = vis.get_visit_namespr(visitname='visit01',sprnumber=123)
# print(visit_detail)
# visit_detail = vis.get_visits_cpr(cprid=3)
# print(visit_detail)
# visit_detail = vis.get_visits_cpr(cprid=3,includestats=True)
# print(visit_detail)


# params = '{\"name\":\"BABY\",\"site\":\"Biobank Site\",\"cpShortTitle\":\"PT\"}'#,\"eventLabel\":\"Unplanned Collection\"}'
# updatedvisit = vis.update_visit(visitid=5,params=params)
# print(updatedvisit)

# participant = participant(base_url=base_url, auth=auth)
# participant.ausgabe()

# participantdetail = party.get_participant(ppid=3)
# print(partydetail)

# params='{\"ppid\":\"PPID\"}'

#participant = collection_protocol_registration(base_url=base_url, auth=auth)
#participant.ausgabe()
#params = '{\"participant\":{\"birthDate\":\"2020-11-23\"},\"cpId\":\"2\"}'
#print(params)
#cp_tools = collection_protocol(base_url, auth)
#cps = cp_tools.get_all_collection_protocols()
#
#cp_tools.get_cp_def()
#cp_tools.get_collection_protocol()
#print(cps)
#input()



# part_info =participant.create_participant(params)
# part_info = participant.update_participant(cprid=10,params=params)
# print(part_info)
# part_info =participant.delete_participant(cprid=7)
# print(part_info)

# part_info = participant.merge_participants(id_from=9, id_to=6)
# print(part_info)
# part_info=participant.get_registration(cprid=6)
# print(part_info)

# params ='{\"participant\":{\"id\":\"10\"},\"registrationDate\":\"2020-12-01\",\"cpId\":\"3\",\"ppid\":\"PPID10\"}'

# part_info = participant.register_to_cp(params)
# print(part_info)

# event = collection_protocol_event(base_url=base_url, auth=auth)
# event.ausgabe()


# params='{\"eventLabel\":\"API-TESOS\","eventPoint\":\"0\",\"eventPointUnit\":\"DAYS\",\
# \"collectionProtocol\":\"PART\",\"defaultSite\":\"Biobank Site\", \"clinicalDiagnosis\":\"Not Specified\",\
# \"acitivtyStatus\":\"Active\",\"code\":\"TESTOS\"}'
# #print(params)
# eventinfo=event.create_event(params)
# print(eventinfo)
# eventinfo=event.get_all_events(cpid=2)
# print(eventinfo)
# params='{\"eventLabel\":\"TEST_UPDATE\"}'
# eventinfo=event.update_event(eventid=10, params=params)
# print(eventinfo)
# eventinfo=event.get_event(eventid=10)
# print(eventinfo)
# #eventinfo=event.delete_event(eventid=9)
# #print(eventinfo)
# #eventinfo=event.delete_event(eventid=9)
# #print(eventinfo)
# eventinfo=event.get_event(eventid=10)
# print(eventinfo)
<<<<<<< HEAD
=======

qry =query_util(base_url=base_url, auth=auth)

#exqry= qry.create_aql(cpid=1,aql='select Participant.ppid, SpecimenCollectionGroup.collectionDate, count(distinct Specimen.id) where Specimen.lineage = \"Aliquot\"')
#print(exqry)

exqry = qry.execute_query(23,0,10)
print(exqry)
>>>>>>> dev_chri

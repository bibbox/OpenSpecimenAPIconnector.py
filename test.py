#! /bin/python3


#### This is for testing reasons online



from os_core.users import users
from os_core.specimen import specimen
from os_core.mandatory import mark_mandatory
from os_core.csv_bulk import csv_bulk
from os_util.bulk_operations import bulk_operations
import json
import pandas


# base_url='http://biobank.silicolab.bibbox.org/'
base_url = 'http://localhost:9013/openspecimen/rest/ng'
auth = ('admin', 'Login@123')


## User test
#user = users(base_url, auth)
#user.ausgabe()
#user_info = user.get_user(3)
#print(user_info)
#alluser = user.get_all_users()
#print(alluser)
#user_info=user.assign_role(3, 1,1, 'Coordinator')
#print(user_info)
#user_info=user.change_password(3,'Login@1234')
#print(user_info)

#user_info=user.create_user(dnd='false', firstname='Max', lastname='Mustermann', emailaddress='error@404.com', phonenumber='0640123456' , domainname='openspecimen', loginname='Max', institutename='Biobank Institute', type='SUPER', address='Address' ,activitystatus='Active')
#user_info=user.delete_user(12)
#user_info=user.get_roles(3)
#print(user_info)
#speci=specimen(base_url,auth)
#speci.ausgabe()

## Specimentest
#speci=specimen(base_url=base_url, auth=auth)
#speci.ausgabe()
#speci_info=speci.get_specimen(1)
#print(speci_info)
#speci_info=speci.check_specimen(specimenLabel='asd')
#print(speci_info)
#speci_info=speci.create_specimen_api(label='label2',cpId=2,specimenClass='Fluid',specimenType='Bile',pathology='Malignant',anatomicSite='Abdomen, NOS'\
#    ,laterality='Bilateral',lineage='New',status='Collected')
#print(speci_info)

#csvfiles=csv_bulk(base_url,auth)
#csvfiles.ausgabe()
#file=csvfiles.get_template(schemaname='specimen')
#print(file)
#print(len(file))
#input_=pandas.read_csv('/home/v/Programs/BBMRI_API/dev_chri/specimen.csv')
#file_id=csvfiles.upload_csv(filename='specimen.csv',file=input_.to_csv(index=None))
#uplo=csvfiles.run_upload(schemaname='specimen',fileid=file_id)
#stat=csvfiles.get_job_status(12)
#statu=csvfiles.job_report(12)
#open(file)

bulk_op=bulk_operations(base_url,auth)
input_=pandas.read_csv('/home/v/Programs/BBMRI_API/dev_chri/specimen.csv')
uplo=bulk_op.bulk_import(file=input_.to_csv(index=None),filename='specimen.csv',schemaname='specimen')
print(uplo)






#### This is for testing reasons online


#! /bin/python3
from os_core.users import users
from os_core.specimen import specimen
import json


# base_url='http://biobank.silicolab.bibbox.org/'
base_url = 'http://localhost:9013/openspecimen/rest/ng'
auth = ('admin', 'Login@123')


## User test
user = users(base_url, auth)
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












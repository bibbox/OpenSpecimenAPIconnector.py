#! /bin/python3
from os_core.users import users
import json


# base_url='http://biobank.silicolab.bibbox.org/'
base_url = 'http://localhost:9013/'
auth = ('admin', 'Login@123')
headers = {'Content-Type': 'application/json', 'cache-control': 'no-cache'}
user = users(base_url, auth, headers)
#user.ausgabe()
#user_info = user.get_user('2')
##print(user_info)
#alluser = user.get_all_users()
#print(alluser)
#user_info=user.assign_role(3, 1,1, 'Coordinator')
#print(user_info)
#user_info=user.change_password(3,'Login@123')
#print(user_info)
#user_info=user.create_user(dnd='false', firstname='Max', lastname='Mustermann', emailaddress='error@404.com', phonenumber='0640123456' , domainname='openspecimen', loginname='Max', institutename='Biobank Institute', type='SUPER', address='Address' ,activitystatus='Active')
#user_info=user.delete_user(10)
user_info=user.get_roles(3)
print(user_info)












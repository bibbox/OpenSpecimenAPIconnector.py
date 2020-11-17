#! /bin/python3

# imports
import json
import requests



# TODO

    # additional imports; idealy these base methods do not need any cross importing of other modules
    # but this has to be checked on time of creation
    # change requests with req_util


# modules can be specified according to the underlying base
# these Base modules only contain

class users:

    # constructor
    def __init__(self, base_url, auth, headers):

        # define class members here

        # static variables
        endpoint = 'openspecimen/rest/ng/'

        # dynamic variables
        self.url = base_url + endpoint
        self.auth = auth
        self.headers = headers

##  Check URL, Password, header
    def ausgabe(self):
        print(self.url, self.auth, self.headers)

##  Users
    #   get all users, nothing required
    def get_all_users(self):
        r = requests.get(self.url+'users/', auth=self.auth)
        return json.loads(r.text)

    #   get specific user with id, can be expanded via tokkens which can be added in the link(e.g. ?loginName=loginName) as far as i know from other API calls
    def get_user(self, id):
        r = requests.get(self.url+'users/'+id, auth=self.auth)
        return json.loads(r.text)

    #   change password, ToDo with "userId, oldPassword, newPassword" also others than superadmin chan change der Password
    def change_password(self,userId,newPassword):
        payload="{\n  \"userId\":" +str(userId)+",\n  \"newPassword\": \""+newPassword+"\"\n}"
        print(payload)
        r= requests.put(self.url+"/users/password",auth=self.auth,headers=self.headers,data=payload)
        return r
    
    #   create User
    def create_user(self, dnd, firstname, lastname, emailaddress, phonenumber, domainname, loginname, institutename, type, address, activitystatus):
        payload="{\"dnd\":"+dnd+",\"domainName\":\""+domainname+"\",\"instituteName\":\""+institutename+"\",\"type\":\""+type+"\",\"firstName\":\""+firstname+"\",\"lastName\":\""+lastname+"\",\"emailAddress\":\""+emailaddress+"\",\"phoneNumber\":\""+phonenumber+"\",\"loginName\":\""+loginname+"\",\"address\":\""+address+"\"}"
        r =requests.post(self.url+'users',auth=self.auth,headers=self.headers,data=payload)
        return r

    #   delete User, via UserId
    def delete_user(self,userid):  
        r=requests.delete(self.url+'/users/'+str(userid)+'?close=true',auth=self.auth)
        return r

##  Roles

    #   get roles of specific user
    def get_roles(self, userid):
        r=requests.get(self.url+'rbac/subjects/'+str(userid)+'/roles',auth=self.auth)
        return json.loads(r.text)

    # assign role to users
    # inputs are the Users ID and the  site_id, Collection protocol id and role
    # ToDO Openspecimen allows different 'unique' identifier eg for CP {'id':1}, {'shortTitle':'sT'}, {'title':'Title'}
    def assign_role(self, userid, siteid, cpid, role):
        payload="{\n  \"site\":{\"id\":\""+str(siteid)+"\"},\n  \"collectionProtocol\":{\"id\":\""+str(cpid)+"\"},\n  \"role\":{\"name\":\""+role+"\"}\n}"
        r= requests.post(self.url+'rbac/subjects/'+str(userid)+'/roles', auth=self.auth,headers=self.headers,data=payload)
        return r

#ToDo The RoleID have to be added,  PUT from OS-API doku doesn't work
    #def update_role(self, userid, sitename, cpst,role):
    #    payload="{\n  \"site\":{\"name\":\""+sitename+"\"},\n  \"collectionProtocol\":{\"shortTitle\":\""+cpst+"\"},\n  \"role\":{\"name\":\""+role+"\"}\n}"
    #    r= requests.put(self.url+'/rbac/subjects/'+str(userid)+'/roles/8',auth=self.auth, headers=self.headers,data=payload)
    #    return r

    






    







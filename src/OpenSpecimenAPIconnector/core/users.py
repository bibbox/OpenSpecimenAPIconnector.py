#! /bin/python3

# imports
import json

from os_core.req_util import OS_request_gen

# TODO

# additional imports; idealy these base methods do not need any cross importing of other modules
# but this has to be checked on time of creation
# change requests with req_util


# modules can be specified according to the underlying base
# these Base modules only contain

class users:

##  Constructor
    def __init__(self, base_url, auth):

        # define class members here
        self.OS_request_gen = OS_request_gen(auth)
        
        self.base_url = base_url


##  Check URL, Password
    def ausgabe(self):

        print(self.base_url, self.OS_request_gen.auth)


##   Users
    #   get all users, nothing required
    def get_all_users(self):

        endpoint = "/users"
        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url=url)

        return json.loads(r.text)


    #   get specific user with id, can be expanded via tokkens which can be added in the link(e.g. ?loginName=loginName) as far as i know from other API calls
    def get_user(self, userId):

        endpoint = "/users/"+str(userId)

        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url=url)

        return json.loads(r.text)


    #   change password, ToDo with "userId, oldPassword, newPassword" also others than superadmin chan change der Password
    def change_password(self, params):

        endpoint = "/users/password"

        url = self.base_url+endpoint

        payload=params

        r = self.OS_request_gen.put_request(url=url, data=payload)

        return json.loads(r.text)


    #   create User
    def create_user(self, params):

        endpoint = "/users"

        url = self.base_url+endpoint

        payload = params

        r = self.OS_request_gen.post_request(url=url, data=payload)

        return json.loads(r.text)


    #   delete User, via UserId
    def delete_user(self, userid):

        endpoint = "/users/"+str(userid)+"/?close=true"
        url = self.base_url+endpoint

        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)


##   Roles

    #   get roles of specific user
    def get_roles(self, userid):

        endpoint = '/rbac/subjects/'+str(userid)+'/roles'
        url = self.base_url+endpoint

        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    #   assign role to users
    #   inputs are the Users ID and the  site_id, Collection protocol id and role
    #   ToDO Openspecimen allows different 'unique' identifier eg for CP {'id':1}, {'shortTitle':'sT'}, {'title':'Title'}
    def assign_role(self, userid, params):

        endpoint = '/rbac/subjects/'+str(userid)+'/roles'

        url = self.base_url+endpoint

        payload = params
            
        r = self.OS_request_gen.post_request(url=url, data=payload)

        return json.loads(r.text)

##  ToDo The RoleID have to be added,  PUT from OS-API doku doesn't work
    # def update_role(self, userid, sitename, cpst,role):
    #    payload="{\n  \"site\":{\"name\":\""+sitename+"\"},\n  \"collectionProtocol\":{\"shortTitle\":\""+cpst+"\"},\n  \"role\":{\"name\":\""+role+"\"}\n}"
    #    r= requests.put(self.url+'/rbac/subjects/'+str(userid)+'/roles/8',auth=self.auth, headers=self.headers,data=payload)
    #    return r

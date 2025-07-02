#! /bin/python3

# imports
import json

from .req_util import OS_request_gen
from .. import config_manager

class users:

    """Handles the API calls for Users

    This class handles the API calls for users. Get all or specific user information, create a user, change his/her/their password,
    get user-roles of or assign a specific role to a user.

    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. The users have to know which requests
    are needed and what content should be uploaded. The API documentation of OpenSpecimen is in:
    https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs
    """
    def __init__(self):

        """Constructor of the Class Users
        
        Constructor of the class users can handle the basic API-calls of the users in OpenSpecimen.
        Connects this class to OpenSpecimen specific request handle (os_core.request_util.py).
        
        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consists of two strings ( loginname , password)
        """ 
        self.base_url = config_manager.get_url()
        self.auth = config_manager.get_auth()
        self.OS_request_gen = OS_request_gen(self.auth)


    def ausgabe(self):

        """Testing of the URL and authentification.
        
        If there are any unexpected errors, one can easily test if the URL and login data is spelled correctly.
        The function prints the URL and login data  to the output terminal, which was handed over to the class.
        """

        print(self.base_url, self.OS_request_gen.auth)


    def get_all_users(self):

        """Get all Users from OpenSpecimen

        Returns all users within the OpenSpecimen disrtibution.

        Returns
        -------
        dict
            Returns all users as JSON dict, or an OpenSpecimen's error message
        """

        endpoint = "/users"
        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url=url)

        return json.loads(r.text)


    def get_user(self, userId):

        """ Get the User with ID

        Get the User with ID from OpenSpecimen. To use this function, one has to know the ID of the user.
        This can be seen in the GUI if one clicks on the User and reads from the URL, which has
        the format: http(s)://<host>:<port>/openspecimen/users/{userid}/... .
        Or with the function get_all_users and then extract the ID to the wanted user.

        Parameters
        ----------
        userId : int
            ID of the User which one wants to get.
        
        Returns
        -------
        dict
            JSON dict of the details of the specified user with ID or the OpenSpecimen's error message
        """

        endpoint = "/users/"+str(userId)

        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url=url)

        return json.loads(r.text)


 
    def change_password(self, params):

        """ Change the password of a user

        Change the password of a user. If the API-User is Superadmin, the parameters are userId,newPassword.
        If the user isn't a Superadmin nor the Superadmin changes his own password, the parameters are userId,
        oldPassword, newPassword.

        Parameters
        ---------
        params : string
            JSON formatted string with parameters userId, oldPassword[mandatory, if not SuperAdmin] newPassword
        
        Returns
        -------
        dict
            Dict with status code. 200 password updated, 400 invalid Parameters, 500 unknown error.
        """

        endpoint = "/users/password"
        url = self.base_url+endpoint
        payload=params
        r = self.OS_request_gen.put_request(url=url, data=payload)

        return json.loads(r.text)


    def create_user(self, params):

        """Create a user

        Create a user in OpenSpecimen. To use this function, one has to know the parameters.
        They are explained in the parameters section. Or one can use the os_util class user_util.

        Parameters
        ----------
        params : string
            JSON formatted string with parameters: firstName, lastName, emailAddress, phoneNumber,
            domainName, loginName, instituteName, type, address[optional], activityStatus

        Returns
        -------
        dict
            JSON dict with details of the created user or the OpenSpecimen's error message.
        """

        endpoint = "/users"
        url = self.base_url+endpoint
        payload = params
        r = self.OS_request_gen.post_request(url=url, data=payload)

        return json.loads(r.text)


    def delete_user(self, userid):

        """Delete a user

        Delete a user in OpenSpecimen. To use this function, one has to know ID of the user.
        This can be seen in the GUI, if one clicks on the user and reads from the URL, which has
        the format: http(s)://<host>:<port>/openspecimen/users/{userid}/... .
        Or with the function get_all_users and then extract the ID to the wanted user.

        Parameters
        ----------
        userid : int
            String or int of the User Id which one wants to delete. Gets converted to a string.

        Returns
        -------
        dict
            JSON dict with details of the deleted user or the OpenSpecimen's error message.
        """

        endpoint = "/users/"+str(userid)+"/?close=true"
        url = self.base_url+endpoint
        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)


    def get_roles(self, userid):

        """Get the roles of a user

        Get the roles of a user with ID in OpenSpecimen. To use this function, one has to know the ID of 
        the user. This can be seen in the GUI, if one clicks on the user and reads from the URL, which has
        the format: http(s)://<host>:<port>/openspecimen/users/{userid}/... .
        Or with the function get_all_users and then extract the ID to the wanted user.

        Parameters
        ----------
        userid : int
            Int of the User Id which one wants to delete. Gets converted to a string.

        Returns
        -------
        dict
            JSON dict with Details of the Roles of the User with ID userid or the OpenSpecimen's error message.
        """
        endpoint = '/rbac/subjects/'+str(userid)+'/roles'
        url = self.base_url+endpoint

        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def assign_role(self, userid, params):

        """Assign a role to a User

        Assign a role to a user with ID in OpenSpecimen. To use this function, one has to know the ID of 
        the user. This can be seen in the GUI, if one clicks on the user and reads from the URL, which has
        the format: http(s)://<host>:<port>/openspecimen/users/{userid}/... .
        Or with the function get_all_users and then extract the ID to the wanted user.

        Parameters
        ----------
        userid : int
            Int of the User ID, which one wants to delete. Gets converted to a string.
        
        params : string
            JSON formatted string with parameters: site(dict with sitedetail), collectionProtocol
            (dict with Collection protocol detail), role(dict with detail of the role)

        Returns
        -------
        dict
            JSON dict with Details of the Roles of the User with ID userid or the OpenSpecimen's error message.
        """

        endpoint = '/rbac/subjects/'+str(userid)+'/roles'
        url = self.base_url + endpoint
        payload = params
        r = self.OS_request_gen.post_request(url=url, data=payload)

        return json.loads(r.text)


    def update_user(self, userid, params):
        
        """Update a User

        Update a User in OpenSpecimen. To use this function, one has to know the parameters.
        They are explained in the parameters section. Or one can use the os_util class user_util.
        Also the ID of the user, which gets updated, has to be known.
        This can be seen in the GUI, if one clicks on the user and reads from the URL, which has
        the format: http(s)://<host>:<port>/openspecimen/users/{userid}/... .
        Or with the function get_all_users and then extract the ID to the wanted user.

        Parameters
        ----------
        userid : int
            ID of the User.

        params : string
            JSON formatted string with parameters: firstName, lastName, emailAddress, phoneNumber,
            domainName, loginName, instituteName, type, address[optional], activityStatus

        Returns
        -------
        dict
            JSON dict with Details of the updated User or the OpenSpecimen's error message.
        """

        endpoint = "/users/" + str(userid)
        url = self.base_url+endpoint
        payload = params
        r = self.OS_request_gen.put_request(url=url, data=payload)

        return json.loads(r.text)

#! /bin/python3

from ..os_core.users import users
from ..os_core.jsons import Json_factory
from ..os_core.url import url_gen

class user_util:

    def __init__(self):

        self.users = users()
        self.jsons = Json_factory()
        self.urls = url_gen()

    def create_user(self, first, last, email,  login, institute, type_, phone=None, address = None, domain = "openSpecimen"):

        """Create a user

        Create a User in OpenSpecimen. This function parses the input to a dict,
        what OpenSpecimen can understand.

        Parameters
        ----------
        first : string
            Firstname of the User.
        
        last : string
            Lastname of the User.

        email : string
            Emailaddress of the user.

        phone : string
            Phonenumber of the user.
        
        login : string
            Loginename of the user, which has to be  unique within the domain.

        institute : string
            Name of the institute where the user belongs.
        
        type_ : string
            Name of the usertype, defined in the OpenSpecimen distribution.
        
        address : string
            Address of the user. [optional]
        
        domain : string
            Domainname, by default OpenSpecimen.
        
        Returns
        -------
        dict
            JSON dict with Details of the created User or the OpenSpecimen's error message.
        """

        params = self.jsons.create_user_json(first = first, last = last, email = email, phone = phone, login = login,
                                         institute = institute, type_ = type_, address = address, domain = domain)
        r = self.users.create_user(params = params)

        return r

    def update_user(self, userid, first, last, email, login, institute, phone = None,
                    type_ = None, address = None, domain = 'openspecimen'):

        """Update a user

        Update a User in OpenSpecimen. To use this function one has to know the ID of the user.
        This can be seen in the GUI if one clicks on the user and reads from the URL which has
        the format: http(s)://<host>:<port>/openspecimen/users/{userid}/... .
        Or with the function get_all_users and then extract the ID to the wanted user.

        Note
        -----
        For updating, the user has to be identified with its unique id {userid},
        all the other parameters of the user are optional. If they are not passed
        to the function, they stay the same.

        Parameters
        ----------
        userid : int
            Unique Id of the user.

        first : string
            Firstname of the User.
        
        last : string
            Lastname of the User.

        email : string
            Emailaddress of the user.

        phone : string
            Phonenumber of the user.
        
        login : string
            Loginename of the user, which has to be unique within the domain.

        institute : string
            Name of the institute where the user belongs to.
        
        type_ : string
            Name of the usertype, defined in the OpenSpecimen distribution.
        
        address : string
            Address of the user. [optional]
        
        domain : string
            Domainname, by default OpenSpecimen.
        
        Returns
        -------
        dict
            JSON dict with Details of the created User or the OpenSpecimen's error message.
        """

        params = self.jsons.create_user_json(first = first, last = last, email = email, phone = phone, login = login,
                                         institute = institute, type_ = type_, address = address, domain = domain)
        r = self.users.update_user(userid = userid, params = params)

        return r

    def assign_role(self, userid, siteid, cpid, role):

        """Assign a role to a user

        Assign a role to a user with ID {userid} in OpenSpecimen. To use this function one has to know the ID of 
        the user, the site, the collection protocol and the name of the role. The user Id can be seen in the
        GUI, if one clicks on the user and reads from the URL which has the format: 
        http(s)://<host>:<port>/openspecimen/users/{userid}/... .
        Or with the function get_all_users and then extract the ID to the wanted user.

        Parameters
        ----------
        userid : int
            The ID of the user.
        
        siteid : int
            The ID of the site.

        cpid : int
            The ID of the collection protocol.
        
        role : string
            The name of the role.

        Returns
        -------
        dict
            JSON dict with Details of the Roles of the User with ID userid or the OpenSpecimen's error message.
        """

        params = self.jsons.assign_user_role_json(siteid = siteid, cpid = cpid, role = role)
        r = self.users.assign_role(userid = userid, params = params)

        return r

    def change_password(self, userid, newpw, oldpw = None):

        """Change the password of a user

        Change the Password of a user. If the API-User is Superadmin, the parameters are userid, newpassword.
        If the User isn't the Superadmin, nor the Superadmin changes his own password the parameters are userid,
        oldpassword, new password.

        Note
        -----
        In the Systemsetting the Superadmin can define the passwords' complexity.

        Parameters
        ---------
        userid : int
            ID of the user, whose password should be changed.
        
        newpw : string
            The  new password of the user.

        oldpw : string
            The old password of the user, has to be specified if the API user is not the Superadmin or
            the Superadmin changes his password.
        
        Returns
        -------
        dict
            Dict with status code. 200 password updated, 400 invalid Parameters, 500 unknown error.
        """

        params = self.jsons.change_user_pw_json(userid = userid, newpw = newpw, oldpw = oldpw)
        r = self.users.change_password(params = params)

        return r
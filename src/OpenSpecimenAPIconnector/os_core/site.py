#! /bin/python3

#Import
from .req_util import OS_request_gen
from .. import config_manager
import pandas as pd

import json


class sites():
    
    """Handles the calls for sites
    
    This class handles the API calls for OpenSpecimen Sites. It can create, delete, search 
    sites with different parameters, get all sites and  get the template of the sites as
    Pandas dataframe.  The output is a JSON dict or the error message as JSON dict, except 
    the Pandas dataframe.
    
    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes, one can
    just pass the parameters via a JSON-formatted string. This means the user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.
    
    Examples
    --------
    A code Examples, where the Collection protocols are handled, is in the Jupyter-Notebook
        $ jupyter notebook main.ipynb
    """

    def __init__(self):

        """Constructor of the Class sites

        Constructor of the class sites can handle the basic API-calls
        of the sites in OpenSpecimen. Connects this class to OpenSpecimen
        specific request handle (os_core.request_util.py). And generates the site specific API-URL.
        
        Parameters
        ----------
        base_url : string
            URL to openspecimen, which has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consists of two strings ( loginname , password)
        """
        self.base_url = config_manager.get_url() + '/sites'
        self.auth = config_manager.get_auth()
        self.OS_request_gen = OS_request_gen(self.auth)

    def ausgabe(self):
        
        """Testing of the URL and authentification.
        If there are any unexpected errors, one can easily test if the URL and login data is spelled correctly.
        The function prints the URL and login data and hand it over to the output terminal.
        """

        print(self.base_url, self.OS_request_gen.auth)


    def create_sites(self, params):
        
        """Create a site in OpenSpecimen
        
        Create a site in OpenSpecimen with an API call. In order to use this function, one has to know
        the OpenSpecimen specific permissable values. With the os_util class site_util.py a site with
        standard OpenSpecimen fields can be created, which is calling this function.
        
        Parameters
        ----------
        params : string
            JSON-formatted string with parameters: name, instituteName, coordinators, type, 
            activityStatus, address
        
        Returns
        -------
        dict
            Details of the created site as dictionary or the OpenSpecimen's error message.
        """  

        url = self.base_url + '/'
        payload = params
        r = self.OS_request_gen.post_request(url, payload)

        return json.loads(r.text)


    def delete_sites(self, siid):
        
        """Delete a site with OpenSpecimen's uniques Site ID
        
        Delete an already existing site. The Parameters <siid> is the uniqe ID of the site
        which is generated automatically from OpenSpecimen. To get the ID, one can click in the GUI on the sites
        page of the desired site and read it from the URL, with format: http(s)://<host>:<port>/openspecimen/#/sites/{siid}/overview .
        Another possibility is to search via 'search_sites' for a specific Parameters and then extract the ID
        from the JSON-dict which get returned.
        
        Parameters
        ----------
        siid: int
            The unique ID of the site which OpenSpecimen creates itself as an integer. 
            
        Returns
        -------
        JSON-dict
            Details of the site which is deleted or the OpenSpecimen error message as dict.
        """

        endpoint = '/' + str(siid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)


    def search_sites(self, search_string):
        
        """Search for sites with specific values.
        Search for one or more sites with the values in search_string defined. The search string looks like:
        http(s)://<host>:<port>/openspecimen/rest/np/sites?{param_1}={value_1}&...&{param_x}={value_x}
        With the class sites_util from os_util and function <search_sites> the search string is generated
        automatically and this function is called. Not all keys from OpenSpecimen can be easily searched for.
        
        Parameters
        ----------
        search_string : string
            String with the following format: ?{param_1}={value_1}&...&{param_x}={value_x} . The parameters can be one of the following:
            startAt[optional], maxResults[optional], name[optional], exactMatch[optional], institute[optional]
            
        Returns
        -------
        JSON-dict
            Details of the matching sites, if no one matches, it is an empty list.
        """

        url = self.base_url + search_string
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def get_all_sites(self):
        
        """Get all Sites
        
        Get all sites within the OpenSpecimen distribution defined with the base_url.
        
        Returns
        -------
        dict
            Details of all sites as dictionary in the OpenSpecimen distribution
        """

        url = self.base_url
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def get_site(self, siteid):
        
        """Get the Site with the ID siteid
        
        Get the details of a site with the system wide unique ID siteid.
        This ID is generated automatically from OpenSpecimen when the site is created.
        
        Parameters
        ----------
        siteid : int
            The system wide unique ID of the side as int.
            
        Returns
        -------
        dict
            Details of the site with the specified ID as dictionary or the OpenSpecimen' error message.
        """

        endpoint = '/' + str(siteid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def update_site(self, siid, params):
        
        """Updates an existing Site with ID siid with the Parameters params
        
        Updates an existing site with the automatically generated OpsenSpecimen's system wide
        unique site ID siid, with the parameters params which are passed to the function.
        The ID of the site has to be known and can, for Examples, be seen in the GUI by clicking on 
        the site, which has the format http(s)://<host>:<port>/openspecimen/site/{cpid}/... .
        Or via the function search_sites or get_all_sites and extracted with key ["id"]
        
        Note
        ----
        The optional parameters are those, which are optional for a site. For updating, all parameters are optional,
        those which are not passed to the function will stay the same as before.
        
        Parameters
        ---------
        siid : int
            Unique site ID which is generated automatically from the system.
        
        params : string
            JSON-formatted string with the parameters which should get updated.The keys which can get updated are: 
            name, instituteName, coordinators, type, activityStatus, address
            
        Returns
        -------
        JSON-dict
            JSON-dict with the details of the updated site or the OpenSpecimen's error message.
        """

        endpoint = '/' + str(siid)
        url = self.base_url + endpoint
        payload = params
        r = self.OS_request_gen.put_request(url, payload)
        return json.loads(r.text)

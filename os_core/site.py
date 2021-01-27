#! /bin/python3

#Import
from os_core.req_util import OS_request_gen

import json


class sites():
    
    """Handles the calls for sites
    
    This class handles the API calls for OpenSpecimen Sites. It can create, delete, search 
    a sites with different parameters, get all sites and  get the template of the sites as
    Pandas dataframe.  The output is a JSON dict or the Error message as JSON dict, except 
    the Pandas dataframe.
    
    Notes
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes one can
    just pass the parameters via JSON-formatted string. This means the user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.
    
    Example
    -------
    A code example, where the Collection protocols are handled is in the Jupyter-Notebook::
        $ jupyter notebook main.ipynb
    """

    def __init__(self, base_url, auth):

        """Constructor of the Class collection_protocol
        Constructor of the class colelction_protocol, can handle the basic API-calls
        of the collection protocol in OpenSpecimen. Connects this class to OpenSpecimen
        specific request handle (os_core.request_util.py). And generates the site specific API-URL.
        
        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consits of two strings ( loginname , password)
        """
        
        self.OS_request_gen = OS_request_gen(auth)
        self.base_url = base_url + '/sites'
        

    def ausgabe(self):
        
        """Testing of the URL and authentification.
        If there are unexpected errors one can easily test if the URL and login data is correctly spelled.
        the function prints the URL and login data, handed over to the class, to the output terminal.
        """

        print(self.base_url, self.OS_request_gen.auth)


    def get_site_pandas_template(self):
        
        """Get the template for sites
        
        Get the template for creating sites as empty pandas dataframe, where the OpenSpecimen keys
        for sites are the header. 

        Returns
        -------
        pandas dataframe
            Empty pandas dataframe, with the OpenSpecimen keys of the sites as header.
        """

        site_template_endpoint = "/import-jobs/input-file-template?schema=site"
        site_template_url = self.base_url + site_template_endpoint
        r = self.Req_Fac.get_request(site_template_url)
        site_pandas_template = pd.DataFrame(columns=[r.content.decode()])

        return site_pandas_template


    def create_sites(self, params):
        
        """Create a site in OpenSpecimen
        
        Create a site in OpenSpecimen with an API call. In order to use this function one has to know
        the OpenSpecimen specific permissable values. With the os_util class site_util.py a site with
        standard OpenSpecimen fields can be created, which is calling this function.
        
        Parameters
        ----------
        params : string
            JSON-formatted string with parameters: name, instituteName, coordinators, type, 
            acitvityStatus, address
        
        Returns
        -------
        dict
            Details of the created site as dictornary or the OpenSpecimen's error message.
        """  

        url = self.base_url + '/'
        payload = params
        r = self.OS_request_gen.post_request(url, payload)

        return json.loads(r.text)


    def delete_sites(self, siid):
        
        """Delete a site with OpenSpeimen's uniques Site ID
        
        Delete an already existing Site. The parameter ::siid:: is the uniqe ID of the Site
        which is generated automatically from OpenSpecimen. To get the ID one can click in the GUI on the Sites
        page on the desired Site and read it from the URL, with format: http(s)://<host>:<port>/openspecimen/#/sites/{siid}/overview .
        An other possibility is to search via 'search_sites' for a specific parameter and then extract the ID
        from the JSON-dict which get returned.
        
        Parameters
        ----------
        siid: string or int
            The unique ID of the Site which OpenSpecimen creates itselfs as a string or integer. 
            It will get converted to a string.
            
        Returns
        -------
        JSON-dict
            Details of the Site which is deleted or the OpenSpecimen error message as dict.
        """

        endpoint = '/' + str(siid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)


    def search_sites(self, search_string):
        
        """Search for  Sites with specific values.
        Search for one or more Sites with the values in search_string defined. The search string looks like:
        http(s)://<host>:<port>/openspecimen/rest/np/sites?{param_1}={value_1}&...&{param_x}={value_x}
        With the class sites_util from os_util and function ::search_sites:: the search string is generated
        automatically and this function is called. Not all keys from OpenSpecimen can be easily searched after.
        
        Parameters
        ----------
        search_string : string
            String with the following format: ?{param_1}={value_1}&...&{param_x}={value_x} . The parameters can be one of the following:
            startAt[optional], maxResults[optional], name[optional], exactMatch[optional], institute[optional]
            
        Returns
        -------
        JSON-dict
            Details of the matching Sites, if no one matches it is an empty list.
        """

        url = self.base_url + search_string
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def get_all_sites(self):
        
        """Get all Sites
        
        Get all Sites within the OpenSpecimen Distribution defined with the base_url.
        
        Returns
        -------
        dict
            Details of all Sites as dictornary in the OpenSpecimen distribution
        """

        url = self.base_url
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def get_site(self, siteid):
        
        """Get the Site with the ID ::siteid::
        
        Get the details of a Site with the System wide unique ID ::siteid::.
        This ID is generated automatically from OpenSpecimen when the Site is created.
        
        Parameters
        ----------
        siteid : string or int
            The system wide unique ID of the side as int or string. It get converted to a string.
            
        Returns
        -------
        dict
            Details of the site with the specified ID as dictornary or the OpenSpecimen' error message.
        """

        endpoint = '/' + str(siteid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def update_site(self, siid, params):
        
        """Updates a existing Site with ID ::siid:: with the Parameters ::params::
        
        Updates a existing Site with the automatically generated OpsenSpecimen's system wide
        unique Site ID ::siid::, with the Parameters ::params:: which are passed to the function.
        The ID of the Site have to be known and can for example be seen in the GUI by clicking on 
        the Site, which has the format http(s)://<host>:<port>/openspecimen/site/{cpid}/... .
        Or via the function search_sites or get_all_sites and extracted with key ["id"]
        
        Note
        ----
        The optional parameters are those, which are optional for a Site. For updating all parameters are optional,
        those which are not passed to the function will stay the same as before.
        
        Parameter
        ---------
        siid : strinf or int
            Unique Site ID which is generated automatically from the System. It will be converted to a string.
        
        params : string
            JSON-formatted string with the parameters which should get updated.The keys which can get updated are: 
            name, instituteName, coordinators, type, acitvityStatus, address
            
        Returns
        -------
        JSON-dict
            JSON-dict with the details of the updated Site or the OpenSpecimen's error message.
        """

        endpoint = '/' + str(siid)
        url = self.base_url + endpoint
        payload = params
        r = self.OS_request_gen.put_request(url, payload)
        return json.loads(r.text)

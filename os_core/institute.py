#! /bin/python3


import json
from os_core.req_util import OS_request_gen


class institutes():

    """Handles the API calls for the institutes

    Handles the OpenSpecimen API calls for the institutes. This class can 
    create, delete, update Insitutes. One can search via different parameters an institute,
    get all Collection protocols corresponding to an institute. Get one or all institutes.
    
    Notes
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes one can
    just pass the parameters via JSON-formatted string. This means the user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Example
    -------

    A code example, where the Institutes are handled is in the Jupyter-Notebook:

        $ jupyter notebook main.ipynb
    """

    def __init__(self, base_url, auth):

        """Constructor of the Class institutes

        Constructor of the class institutes, can handle the basic API-calls
        of the institutes in OpenSpecimen. Connects this class to OpenSpecimen
        specific URL Generator Class (os_core/url.py)

        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consits of two strings ( loginname , password)
        """

        self.OS_request_gen = OS_request_gen(base_url, auth)
        self.base_url = base_url + '/institutes'
        self.urls = url_gen()


    def ausgabe(self):

        """Testing of the URL and authentification.

        If there are unexpected errors one can easily test if the URL and login data is correctly spelled.
        the function prints the URL and login data, handed over to the class, to the output terminal.
        """

        print(self.base_url, self.OS_request_gen.auth)


    def create_institute(self, params):

        """Creates an Insitute.

        Creates an Institute in OpenSpecimen. In order to use this function one has to know
        the parameters which OpenSpecimen needs to create an Insitute. One can use it via the os_util class
        institute_util. This allows just the basic definition. 

        Parameters
        ----------
        params : string
            JSON formatted string with parameter: name (Name of the Institute)

        Returns
        -------
        json-dict
            Either details of the created institute as JSON-dict or the OpenSpecimen's error message. 
        """

        url = self.base_url + '/'
        payload = params
        r = self.OS_request_gen.post_request(url, payload)

        return json.loads(r.text)


    def delete_institute(self, inid):

        """Delete an Institute 

        Delete an existing Institute In OpenSpecimen with ID ::inid::.
        The ID is created from OpenSpecimen and can for eample be seen in the GUI
        under Institutes when clicking on the Institute, the URL looks like:
        http(s)://<host>:<port>/openspecimen/institutes/{inid}/overview .
        Or with the function search_institutes for example by name and extract the id from there.

        Parameter
        ---------
        inid : string or int
            The System generated ID of the Institute. Will get converted to a string.

        Returns
        -------
        JSON-dict
            Details of the deleted Institue or the OpenSpecimen's error message.
        """

        endpoint = '/' + str(inid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)


    def search_institutes(self, substring):

        """Search for  Institutes with specific substring.

        Search for one or more Institutes with the substring in their name defined. The search URL looks like:
        http(s)://<host>:<port>/openspecimen/rest/np/institutes?{param_1}={value_1}&...&{param_x}={value_x}

        Parameters
        ----------
        substring : string
            Substring of the Institutename.

        Returns
        -------
        JSON-dict
            Details of all matching Institue or the OpenSpecimen's error message.
        """

        endpoint = '?name=' + str(substring)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def get_all_institutes(self):

        """Get all Institutes

        Get all Institutes within the OpenSpecimen distribution, which is defined in the base_url.

        Returns
        -------
        JSON-dict
            Details of all Institutes which are in the OpenSpecimen Distribution.
        """

        url = self.base_url
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def get_institute(self, inid):

        """Get the institute with the ID ::inid::

        Get the details of the Institute with the unique ID ::inid::.
        This ID is generated automatically from OpenSpecimen when the Protocol is created.

        Parameters
        ----------
        inid : string or int
            The System's ID of the Institute, will be converted to a string.

        Returns
        -------
        JSON-dict
            Details of the Institute with the specified ID, or the OpenSpecimen error message.
        """

        endpoint = '/' + str(inid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def update_institute(self, inid, params):

        """Updates a existing Institute with ID ::inid:: with the Parameters ::params::

        Updates a existing Institute with the automatically generated OpsenSpecimen's system wide
        unique Institute ID ::instituteid::, with the Parameter ::params:: which are passed to the function.
        The ID of the Institute have to be known and can for example be seen in the GUI by clicking on 
        the Institutes, which has the format http(s)://<host>:<port>/openspecimen/institutes/{inid}/... .
        Or via the function search_institutes.

        Parameter
        ---------
        instituteid :  int
            Unique Institute ID which is generated automatically from the System. It will be converted to a string.
        
        institutename : string
            New name of the isntitute, if it is leaved empty nothing will be updated.
        Returns
        -------
        JSON-dict
            JSON-dict with the details of the updated Institute or the OpenSpecimen's error message.
        """

        endpoint = '/' + str(inid)
        url = self.base_url + endpoint
        payload = params
        r = self.OS_request_gen.put_request(url, payload)

        return json.loads(r.text)
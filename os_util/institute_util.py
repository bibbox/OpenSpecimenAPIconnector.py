#! /bin/python3


from ..os_core.url import url_gen
from ..os_core.jsons import Json_factory
from ..os_core.institute import institutes

import jsons

class institutes_util:

    """Handles the API calls for the institutes

    Handles the OpenSpecimen API calls for the institutes. This class can 
    create, and update Insitutes. The other calls are in the os_core class institutes.
    
    Notes
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. 
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Example
    -------
    A code example, where the Institutes are handled is in the Jupyter-Notebook:

        $ jupyter notebook main.ipynb
    """

    def __init__(self, base_url, auth):

        """Constructor of the Class institutes_util

        Constructor of the class institutes_util, can handle the  API-calls
        create and update of the institutes in OpenSpecimen. Connects this class os_core
        classes institutes and Json_factory

        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consits of two strings ( loginname , password)
        """

        self.institutes = institutes(base_url = base_url, auth = auth)
        self.jsons = Json_factory()

    def create_institute(self, institutename):

        """Creates an Insitute.

        Creates an Institute in OpenSpecimen. 

        Parameters
        ----------
        institutename : string
            the name of the institute.

        Returns
        -------
        json-dict
            Either details of the created institute as JSON-dict or the OpenSpecimen's error message. 
        """"

        params = self.jsons.create_institute(institutename = institutename)
        r = self.institutes.create_institute(params = params)

        return r

    def update_institute(self, instituteid, institutename=None):

        """Updates a existing Institute with ID ::inid:: and the new name institutename

        Updates a existing Institute with the automatically generated OpsenSpecimen's system wide
        unique Institute ID ::instituteid::, with the Parameter ::params:: which are passed to the function.
        The ID of the Institute have to be known and can for example be seen in the GUI by clicking on 
        the Institutes, which has the format http(s)://<host>:<port>/openspecimen/institutes/{inid}/... .
        Or via the function search_institutes.

        Parameter
        ---------
        inid : string or int
            Unique Institute ID which is generated automatically from the System. It will be converted to a string.
        
        params : string
            JSON-formatted string with the key name. 

        Returns
        -------
        JSON-dict
            JSON-dict with the details of the updated Institute or the OpenSpecimen's error message.
        """

        params = self.jsons.create_institute(institutename = institutename)
        r = self.institutes.create_institute(inid =instituteid, params = params)

        return r

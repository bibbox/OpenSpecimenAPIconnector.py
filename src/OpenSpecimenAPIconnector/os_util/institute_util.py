#! /bin/python3

from ..os_core.url import url_gen
from ..os_core.jsons import Json_factory
from ..os_core.institute import institutes


class institutes_util:

    """Handles the API calls for the institutes

    Handles the OpenSpecimen API calls for the institutes. This class can 
    create, and update institutes. The other calls are in the os_core class institutes.
    
    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. 
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Examples
    --------
    A code Examples, where the institutes are handled is in the Jupyter-Notebook:

        $ jupyter notebook main.ipynb
    """

    def __init__(self):

        """Constructor of the Class institutes_util

        Constructor of the class institutes_util, can handle the  API-calls
        to create and update the institutes in OpenSpecimen. Connects this class os_core
        classes institutes and Json_factory

        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consists of two strings ( loginname , password)
        """

        self.institutes = institutes()
        self.jsons = Json_factory()

    def create_institute(self, institutename):

        """Creates an Institute.

        Creates an Institute in OpenSpecimen. 

        Parameters
        ----------
        institutename : string
            the name of the institute.
        """

        params = self.jsons.create_institute(institutename = institutename)
        r = self.institutes.create_institute(params = params)

        return r
        

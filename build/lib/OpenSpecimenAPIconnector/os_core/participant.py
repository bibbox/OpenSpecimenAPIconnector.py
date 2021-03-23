#! /bin/python3

# Import
import json
from datetime import datetime
from .req_util import OS_request_gen
from .. import config_manager

class participant:

    """Handles the API calls for the participant

    Handles the OpenSpecimen API calls for the participants. This class can 
    get a participant with a Participant Protocoll ID PPID or via search parameters.
    
    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes, one can
    just pass the parameters via a JSON-formatted string. This means the user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Examples
    --------

    A code Examples, where the institutes are handled, is in the Jupyter-Notebook:

        $ jupyter notebook main.ipynb
    """

    def __init__(self):

        """Constructor of the Class institutes

        Constructor of the class institutes can handle the basic API-calls
        of the institutes in OpenSpecimen. Connects this class to OpenSpecimen
        specific URL Generator Class (os_core/url.py) and the os_util class participant_util

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

    def get_participant(self, ppid):

        """Get the participant with the Participant Protocol ID ppid

        Get the details of the Participant with the Collection protocol wide unique ID ppid.
        This ID can be generated automatically from OpenSpecimen or generated manually, which has
        to be specified when the Collection Protocol is created.

        Parameters
        ----------
        ppid : int
            The Collection Protocol  wide unique Participant Protocol ID of the Institute will be converted to a string.

        Returns
        -------
        JSON-dict
            Details of the Participant with the specified PPID, or the OpenSpecimen error message.
        """

        endpoint = '/participants/' + str(ppid)

        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def get_participant_matches(self, params):

        """Get the Participants who matches the params.

        Get one or more participants who match the criteria passed with params. This class can be used via
        the os_util class cpr_util.py.
        
        Note
        ----
        In the response the matching attributes are listed.

        Parameters
        ----------
        params : string
            Json formatted string with parameters: lastName (substring)[optional], uid[optional], birthDate[optional],
            pmi(dict with keys mrn[optional], siteName[optional]) [optional], empi[optional], reqRegInfo(default =false)[optional]

        Returns
        -------
        JSON-dict
            Details of all matching participants or the OpenSpecimen's error message.
        """

        endpoint = '/participants/match'
        url = self.base_url + endpoint
        payload=params
        r = self.OS_request_gen.post_request(url,data=payload)

        return json.loads(r.text)

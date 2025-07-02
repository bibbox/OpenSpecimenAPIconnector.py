#! /bin/python3

# Import
from datetime import datetime
from .req_util import OS_request_gen
from .. import config_manager
import json


class specimen_event:
    """Handles the calls for Specimen events

    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes, one can
    just pass the parameters via a JSON-formatted string. This means the user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and
    the calls refer to this site. More details can be seen in the documentation.

    Examples
    --------

    """

    def __init__(self):

        """Constructor of the Class specimen event

        Parameters
        ----------
        base_url : string
            URL to openspecimen, which has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consists of two strings ( loginname , password)
        """
        self.base_url = config_manager.get_url() + '/specimens'
        self.auth = config_manager.get_auth()
        self.OS_request_gen = OS_request_gen(self.auth)

    def ausgabe(self):

        """Testing of the URL and authentification.

        If there are any unexpected errors, one can easily test if the URL and login data is spelled correctly.
        The function prints the URL and login data  to the output terminal, which was handed over to the class.
        """

        print(self.base_url, self.OS_request_gen.auth)

    def get_specimen_events(self, specimenid):

        """Get the Specimen events for the specimen ID specimenid


        Parameters
        ----------
        specimenid : string or int
            The System's ID of the Specimen, which will be converted to a string.
        Returns
        -------
        JSON-dict
            Details of the Specimen with the specified ID, or the OpenSpecimen error message.
        """

        endpoint = '/' + str(specimenid) + '/events'
        url = self.base_url + endpoint
        # print(url)
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)



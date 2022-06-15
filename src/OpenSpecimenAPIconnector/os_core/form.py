#! /bin/python3

# Import
from datetime import datetime
from .req_util import OS_request_gen
from .. import config_manager
import json


class form:
    """Handles the calls for forms

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
        """Constructor of the Class form

        Parameters
        ----------
        base_url : string
            URL to openspecimen, which has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consists of two strings ( loginname , password)
        """
        self.base_url = config_manager.get_url() + '/forms'
        self.auth = config_manager.get_auth()
        self.OS_request_gen = OS_request_gen(self.auth)

    def ausgabe(self):
        """Testing of the URL and authentification.

        If there are any unexpected errors, one can easily test if the URL and login data is spelled correctly.
        The function prints the URL and login data  to the output terminal, which was handed over to the class.
        """

        print(self.base_url, self.OS_request_gen.auth)

    def get_form_details(self, formId, recordId, includeMetadata=True):
        """Get the form details for a specific form entry with/without metadata


        Parameters
        ----------
        formId : string or int
            The System's ID of the form, which will be converted to a string.
        recordId: string or int
            The System's ID of a spefic record of the specified form, which will be converted to a string
        includeMetadata: bool
            Whether or not metadata should be included. Default = True.
        Returns
        -------
        JSON-dict
            Details of the Specimen with the specified ID, or the OpenSpecimen error message.
        """

        endpoint = '/' + str(formId) + '/data/' + str(recordId) + '?includeMetadata=' + str(includeMetadata)
        url = self.base_url + endpoint
        # print(url)
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)

    def get_all_forms(self):
        """Get the details for all forms.

        Parameters
        ---------

        Returns
        -------
        JSON-dict
            Details of the forms or the openSpecimen's error message.
        """


        endpoint = ''
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def get_record(self, formId, recordId):
        """Get the details for a single record (instance of a form).

        Parameters
        ---------
        formId: int
            id of the form that has been filled out
        recordId: int
            id of the specific record

        Returns
        -------
        JSON-dict
            Details of the forms or the openSpecimen's error message.
        """

        endpoint = f'/{formId}/data/{recordId}'
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def add_record(self, formid, data):
        """Fills a specific form

        Parameters
        ---------
        formid: int
            id of the form
        data: string
            JSON formatted string to fill the form; must follow form specific structure

        Returns
        -------
        JSON-dict
            Details of the form or the openSpecimen's error message.
        """

        endpoint = f'//{formid}/data'
        #print(endpoint)
        url = self.base_url + endpoint
        r = self.OS_request_gen.put_request(url, data)

        return json.loads(r.text)


    def delete_record(self, formId, recordId):
        """Get the details for a single record (instance of a form).

        Parameters
        ---------
        formId: int
            id of the form that has been filled out
        recordId: int
            id of the specific record to be deleted

        Returns
        -------
        JSON-dict
            RecordId that has been deleted or the openSpecimen's error message.
        """

        endpoint = f'/{formId}/data/{recordId}'
        url = self.base_url + endpoint
        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)




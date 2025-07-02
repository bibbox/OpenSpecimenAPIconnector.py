#! /bin/python3

from ..os_core.url import url_gen
from ..os_core.jsons import Json_factory
from ..os_core.form import form


class forms_util:

    """Handles the API calls for the forms

    Handles the OpenSpecimen API calls for the forms. This class can
    fill a form. The other calls are in the os_core class form.
    
    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. 
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Examples
    --------
    """

    def __init__(self):

        """Constructor of the Class form_util

        Constructor of the class form_util, can handle the  API-calls
        to fill forms in OpenSpecimen. Connects this class os_core
        classes form and Json_factory

        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consists of two strings ( loginname , password)
        """

        self.form = form()
        self.jsons = Json_factory()

    def add_record(self,form_id, form_ctx_id, object_id, form_data, form_status="COMPLETE"):

        """
        Adds a record to the form with the given parameters.

        This method is intended to facilitate the addition of a record to
        a specific form by preparing the necessary parameters in JSON format
        and interacting with the appropriate backend or system.

        Parameters
        ----------
        form_id : int
            The identifier for the form to which the record will be added.
        form_ctx_id : int
            The context identifier for the form. (Differs when the form is not a global form)
        object_id : int
            The identifier for the object associated with the form data. (Specimen, Participants, ...)
        form_data : dict
            The data to be added as a record to the form. The data type and structure
            must adhere to the requirements of the form's backend system.
        form_status : str, optional
            The status of the form record for submission or saving. Defaults to "COMPLETE".

        Returns
        -------

        """

        params = self.jsons.add_form_record_json(form_ctx_id, object_id, form_data, form_status)
        r = self.form.add_record(form_id, params = params)

        return r

    def attach_form(self, form_id, level, cp_id):
        """
        Attaches a form to a specified entity using provided parameters. This method
        communicates with an external system or API to perform the attachment
        operation. It prepares the required parameters in a formatted JSON,
        sends the request, and returns the response from the system.

        Parameters
        ----------
        form_id : int
            The unique identifier of the form to be attached.
        level : str
            Level of the entity to which the form is attached. (Specimen, CommonParticipant, ...)
        cp_id : int
            The unique identifier of the collection protocol.

        Returns
        -------

        """

        params = self.jsons.attach_form_json(form_id=form_id , cp_id=cp_id, level=level)
        r = self.form.attach_form(form_id, params = params)

        return r

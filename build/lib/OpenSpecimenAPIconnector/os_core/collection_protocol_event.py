#! /bin/python3

# Import
import json

from .req_util import OS_request_gen
from .. import config_manager

class collection_protocol_event:

    """Handles the Events of corresponding to a Colelction Protocol

    This class allows you to handle the Events in Openspecimen. One can create an event,
    but first the corresponding Colelction Protocol have to be created, for Examples via os_core.collection_protocol.py.
    Get all events or just get one event, delete or update an existing event.
    The output is a JSON dict with either details or the Openspecimen error message.

    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes one can
    just pass the parameters via JSON-formatted string. This means the user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Examples
    --------

    A code Examples, where also Events are handled is in the Jupyter-Notebook

        $ jupyter notebook main.ipynb
    """

    def __init__(self):

        """Constructor of the Class collection_protocol_event

        Constructor of the class collection_protocol_event can handle the basic API-calls
        of the collection protocol events in OpenSpecimen which connects this class to OpenSpecimen's
        specific request handle (os_core.request_util.py).

        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consits of two strings ( loginname , password)
        """
        self.base_url = config_manager.get_url() + '/collection-protocol-events' 
        self.auth = config_manager.get_auth()
        self.OS_request_gen = OS_request_gen(self.auth)

    def ausgabe(self):

        """Testing of the URL and authentification.

        If there are any unexpected errors one can easily test if the URL and login data are spelled correctly.
        The function prints the URL and login data to the output terminal, which was handed over to the class.
        """

        print(self.base_url, self.OS_request_gen.auth)


    def create_event(self, params):

        """Create an event for a given Collection Protocol.

        Create an event for a given Collection Protocol. In order to use this function one
        has to know the parameters, which OpenSpecimen needs for to create an event. Another way
        to use it is with the class os_util.cpevent_util.py. An advantage of creating events with
        API calls is that the event Code "code" can be set, which is needed to add conditional forms
        via the workflow.

        Parameters
        ----------
        params : string
            json-formatted string with parameters: eventLabel, eventPoint, collectionProtocol, defaultSite,
            clinicalDiagnosis, clinicalStatus, activityStatus, code[optional]

        Returns
        -------
        json dict
            Returns a json dict with the details of the created event, or the OpenSpecimen error message. 
        """

        url = self.base_url
        payload = params
        r = self.OS_request_gen.post_request(url, payload)

        return json.loads(r.text)


    def delete_event(self, eventid):

        """Delete an event with the ID eventid.

        Delete an event, which is already in OpenSpecimen. The unique ID is generated from OpenSpecimen
        and can for Examples be seen in the URL, if one clicks on the event in the GUI. The URL looks like:
        http(s)://<host>:<port>/openspecimen/#/cps/{CollectionProtocolId}/specimen-requirements?eventId={eventid}
        For Examples, one can extract the eventid with an event-key from OpenSpecimen, when the function
        "get_all_events(self, cpid)" for a specific Collection Protocol, with the Collection Protocol ID is called first.


        Parameters
        ----------
        eventid : int
            The unique ID of the event, which is created by OpenSpecimen.

        Returns
        -------
        json dict
            Details of the deleted event or OpenSpecimens error message as JSON dict.
        """

        endpoint = '/' + str(eventid)
        url = self.base_url + endpoint

        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)


    def get_all_events(self, cpid):

        """Get all events for a specific Collection Protocol with ID cpid.

        Get the details of all events within a given Collection Protocol with the ID cpid.
        For Examples, the ID can be seen in the URL if one clicks on the overview of a Collection
        Protocol. The URL looks like: http(s)://<host>:<port>/openspecimen/#/cps/{cpid}/overview .
        Another possibility is to search via the  function "search_collection_protocols(self, search_params)"
        from the class os_core.collection_protocol with an OpenSpecimen specific key and value.

        Parameters
        ----------
        cpid : int
            Unique ID within OpenSpecimen from a given Collection Protocol. OpenSpecimen generates this ID automatically.

        Returns
        -------
        json-dict
            Details of all events within a given Collection Protocol as dict, where each event is a JSON-dict, or
            an error message, which is generated from OpenSpecimen.
        """

        endpoint = '?cpId=' + str(cpid)
        url= self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def get_event(self, eventid):

        """Get the details of an event with the unique ID eventid.

        Get the details of an event, which is already in OpenSpecimen. The unique ID is generated from OpenSpecimen
        and can for Examples be seen in the URL, if one clicks on the event in the GUI. The URL looks like:
        http(s)://<host>:<port>/openspecimen/#/cps/{CollectionProtocolId}/specimen-requirements?eventId={eventid}
        For Examples, one can extract the eventid with an event-key from OpenSpecimen, when the function
        "get_all_events(self, cpid)" for a specific Collection Protocol, with the Collection Protocol ID is called first.

        Parameters
        ----------
        eventid : int
            Unique ID of the event within OpenSpecimen, which is generated automatically.
        Returns
        -------
        json-dict
            Details of an event JSON-dict with  ID eventid, or an error message, which is generated from OpenSpecimen.
        """

        endpoint = '/' + str(eventid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def update_event(self, eventid, params):

        """Update an existing event with ID eventid and the parameters params.

        Update an existing event with ID eventid. In order to use this function, one
        has to know the parameters, which OpenSpecimen allows to update. 
        For Examples, one can 'add' the Parameters "code" to an existing event which was created via GUI.
        This is needed if one wants to add conditional forms via the workflow.

        Parameters
        ----------
        eventid : string or int
            Unique ID of the event within OpenSpecimen, which is generated automatically.
        params : string
            json-formatted string with parameters: eventLabel, eventPoint, collectionProtocol, defaultSite,
            clinicalDiagnosis, clinicalStatus, activityStatus, code[optional]
        
        Returns
        -------
        json-dict
            Details of the event  as JSON-dict which was updated, or an error message, which is generated from OpenSpecimen.
        """
        
        endpoint = '/' + str(eventid)
        url = self.base_url + endpoint
        payload = params
        r = self.OS_request_gen.get_request(url, payload)

        return json.loads(r.text)

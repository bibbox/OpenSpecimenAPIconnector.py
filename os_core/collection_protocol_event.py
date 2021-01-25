#! /bin/python3

# Import
import json

from os_core.req_util import OS_request_gen

class collection_protocol_event:

    """Handles the Events of corresponding to a Colelction Protocol

    This class allows you to handle the Events in Openspecimen. One can create an event,
    but first the corresponding Colelction Protocol have to create, for example via os_core.collection_protocol.py.
    Get all events or just get one event, delete or update an existing event.

    Notes
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes one can
    just pass the parameters via JSON-formatted string. This means the user has to know the keywords.

    Example
    -------

    A code example, where also Events are handled is in the Jupyter-Notebook::

        $ jupyter notebook main.ipynb
    """
    def __init__(self, base_url, auth):

        """Constructor of the Class collection_protocol_event

        Constructor of the class colelction_protocol_event, can handle the basic API-calls
        of the collection protocol events in OpenSpecimen. Connects this class to OpenSpecimen
        specific request handle (os_core.request_util.py).

        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consits of two strings ( loginname , password)
        """
        
        self.OS_request_gen = OS_request_gen(auth)
        self.base_url = base_url + '/collection-protocol-events'


    def ausgabe(self):

        """Testing of the URL and authentification.

        If there are unexpected errors one can easily test if the URL and login data is correctly spelled.
        the function prints the URL and login data, handed over to the class, to the output terminal.
        """

        print(self.base_url, self.OS_request_gen.auth)


    def create_event(self, params):

        """Create an event for a given Collection Protocol.

        Create an event for a given Collection Protocol. In order to use this function one
        has to know the parameters, which OpenSpecimen needs to create an event. An other way
        to use it is with the class os_util.cpevent_util.py. An advantage of creating events with
        API calls is that the event Code "code" can be sett, which is needed to add conditional forms
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

        Delete an event, which is allready in OpenSpecimen. The unique ID is generated from OpenSpecimen
        and can for example be seen in the URL, if one click on the event in the GUI. The URL looks like:
        http(s)://<host>:<port>/openspecimen/#/cps/{CollectionProtocolId}/specimen-requirements?eventId={eventid}
        For example, one can extract the eventid with an event-key from OpenSpecimen, when first the function
        "get_all_events(self, cpid)" for a specific Collection Protocol, with the Collection Protocol ID is called.


        Parameters
        ----------
        eventid : int or string
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
        For example the ID can be seen in the URL if one click on the overview of a Collection
        Protocol. The URL looks like: http(s)://<host>:<port>/openspecimen/#/cps/{cpid}/overview .
        An other possibility is to search, via the  function "search_collection_protocols(self, search_params)"
        from the class os_core.collection_protocol with a OpenSpecimen specific key and value.

        Parameters
        ----------
        cpid : string or int
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

        Get the details of an event, which is allready in OpenSpecimen. The unique ID is generated from OpenSpecimen
        and can for example be seen in the URL, if one click on the event in the GUI. The URL looks like:
        http(s)://<host>:<port>/openspecimen/#/cps/{CollectionProtocolId}/specimen-requirements?eventId={eventid}
        For example, one can extract the eventid with an event-key from OpenSpecimen, when first the function
        "get_all_events(self, cpid)" for a specific Collection Protocol, with the Collection Protocol ID is called.

        Parameters
        ----------
        eventid : string or int
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


#   Update Event with ID
#   Input:  - eventid: Id of the Event which should get updated
#           - params: Parameter of the Event which should get updated
#   Output: - either details of the updated event as jsoon-formatted string
#           - or error message
    def update_event(self, eventid, params):

        """Update an existing event with ID eventid and the parameters params.

        update an existing event with ID eventid. In order to use this function one
        has to know the parameters, which OpenSpecimen allows to update. 
        For example one can 'add' the parameter "code" to an existing event which was created via GUI.
        This is needed if one want to add conditional forms via the workflow.

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

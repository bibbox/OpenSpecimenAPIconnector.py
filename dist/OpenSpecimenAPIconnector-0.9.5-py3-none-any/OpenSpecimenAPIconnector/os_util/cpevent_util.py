#! /bin/python3

from ..os_core.collection_protocol_event import collection_protocol_event
from ..os_core.jsons import Json_factory
import json
import io
import pandas
import time

class cpevent_util:

    """Handles the Events of corresponding to a Collection Protocol

    This class allows you to handle the events in Openspecimen. One can create an event,
    but first the corresponding Collection Protocol has to be created, for Examples via os_core.collection_protocol.py.
    or one can update an existing event. The other calls are in the os_core class collection_protocol_event.py.
    The output is a JSON dict with either details or the Openspecimen error message.

    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Examples
    --------

    A code Examples, where also events are handled is in the Jupyter-Notebook

    $ jupyter notebook main.ipynb
    """

    def __init__(self):

        """Constructor of the Class cpevent_util

        Constructor of the class cpevent_util, can handle the basic API-calls
        of the collection protocol events in OpenSpecimen. Connects this class to the
        os_core classes collection_protocol_event and Json_factory.

        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consists of two strings ( loginname , password)
        """

        self.event = collection_protocol_event()
        self.jsons = Json_factory()


    def create_event(self, label, point, cp, site, diagnosis, status, activity, unit, code = None):

        """Create an event for a given Collection Protocol.

        Create an event for a given Collection Protocol. Details of the parameters can be found in
        the parameters section.

        Parameters
        ----------
        label : string
            Label of the Event, has to be unique.
        
        point : string or int
            Starting Point of the event, Value + unit (e.g. DAYS).
        
        cp : string
            title of the collection protocol.
        
        site : string
            The default Site of the event.
        
        diagnosis : string
            Defines the permissable values of the diagnosis.
        
        status : string
            Defines the permissable values of the clinical status.
        
        acitivity : string
            Defines the activity status of the event.
        
        unit : string
            Defines which unit has the starting point.
        
        code : string
            the event code, is optional. In order to define condionals in the workflow, one needs the event code.

        Returns
        -------
        json dict
            Returns a json dict with the details of the created event, or the OpenSpecimen error message. 
        """

        params = self.jsons.create_cp_event_json(label = label, point = point, cp = cp, site = site, 
                    diagnosis = diagnosis, status = status, activity = activity, unit = unit, code = code)
        r = self.event.create_event(params = params)

        return r


    def update_event(self, eventid, label = None, point = None, cp = None, site = None, diagnosis = None,
                     status = None , activity = None, unit = None, code = None):
    
        """Update an event for a given Collection Protocol.

        Update an event for a given Collection Protocol. To use this function one has to know the eventid,
        it can for Examples be seen in the URL, if one click on the event in the GUI. The URL looks like:
        http(s)://<host>:<port>/openspecimen/#/cps/{CollectionProtocolId}/specimen-requirements?eventId={eventid}
        For Examples, one can extract the eventid with an event-key from OpenSpecimen, when first the function
        "get_all_events(self, cpid)" for a specific Collection Protocol, with the Collection Protocol ID is called.

        Note
        -----
        All parameters except the eventid are optional. If they are not passed to the function they stay the same as before.

        Parameters
        ----------
        eventid : int
            The ID of the event. Gets converted to a string.

        label : string
            Label of the event, has to be unique.
        
        point : int
            Starting Point of the event, Value + unit (e.g. DAYS).
        
        cp : string
            title of the collection protocol.
        
        site : string
            The default Site of the event.
        
        diagnosis : string
            Defines the permissable values of the diagnosis.
        
        status : string
            Defines the permissable values of the clinical status.
        
        acitivity : string
            Defines the activity status of the event.
        
        unit : string
            Defines which unit has the starting point.
        
        code : string
            the event code, is optional. In order to define condionals in the workflow, one needs the event code.

        Returns
        -------
        json dict
            Returns a json dict with the details of the created event, or the OpenSpecimen error message. 
        """

        params = self.jsons.create_cp_event_json(label = label, point = point, cp = cp, site = site, 
                    diagnosis = diagnosis, status = status, activity = activity, unit = unit, code = code)
        r = self.event.update_event(eventid = eventid, params = params)

        return r

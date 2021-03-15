#! /bin/python3

# Import
import json
from datetime import datetime
from .. import config_manager

from .req_util import OS_request_gen

class visit:

    """Handles the API calls for Visits
    
    This class handles the API calls for OpenSpecimen visits. It can create, delete, 
    search visits with different parameters. Further visits can be added to a collection protocol within the system.
    The outputs are JSON dicts or the error messages as dict.
    
    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes one can
    just pass the parameters via a JSON-formatted string. This means the user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.
    
    Examples
    --------
    A code Examples, where the visits are handled, is in the Jupyter-Notebook
        $ jupyter notebook main.ipynb
    """

    def __init__(self):

        """Constructor of the Class visit
        
        Constructor of the class visit, can handle the basic API-calls
        of the visits in OpenSpecimen. Connects this class to OpenSpecimen
        specific request handle (os_core.request_util.py).
        
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


    def add_visit(self, params):

        """Add a visit to a Participant.
        
        Add a visit to a participant in OpenSpecimen via API call. To use this function, one has to know the
        parameters of the participant, event and site.

        Note
        ----
        Mandatory fields are -cprId or (ppid and cpTitle) or (ppid and cpShortTitle)
        - name, site

        Parameters
        ----------
        params : string
            JSON formatted string with parameters: cprId, eventId, eventLabel, ppid, cptitle, cpShorttitle, name,
            clinicalDiagnoses[optional], clinicalStatus[optional], activityStatus [optional], site, status(permissable
            values: COMPLETE, PENDING, MISSED), missedReason[optional], missedBy[optional], comments[optional],
            surgicalPathologyNumber[optional], cohort[optional], visitDate[optional]
        
        Returns
        -------
        dict
            Details of the visit as JSON dict or the Openspecimen's error message.
        """

        endpoint = '/visits'
        url = self.base_url + endpoint
        payload = params
        r = self.OS_request_gen.post_request(url, data=payload)

        return json.loads(r.text)


    def add_visit_specimen(self, params):

        """Generate a visit and corresponding specimens

        Create a visit and specimens in one call. To use this function one has to know the parameters
        of the participants and events. Or one can use the create_visit_specimens function from the os_util
        class visit_util. 

        Note
        ----
        The visit fields can be seen in add_visit and the ones for specimens are in create specimen.

        Parameters
        ----------
        params : string
            JSON formatted string with parameters visit (dict-like string with details of the visit),
            specimens(dict-like string with details of the specimens)

        Returns
        -------
        dict
            JSON dict with the details of the created visit and specimens or OpenSpecimen's error message
        """

        endpoint = '/visits/collect'
        url = self.base_url + endpoint
        payload = params
        r = self.OS_request_gen.post_request(url, data=payload)

        return json.loads(r.text)



    def delete_visit(self, visitid):

        """Delete a Visit from OpenSpecimen

        Delete an existing visit in OpenSpecimen with the Visit ID visitid. This has to be known and can
        be found out in the GUI by clicking on a participant and the visit. It looks like:
        http(s)://<host>:<port>/openspeicmen/cp-view/{cpid}/participant/{cprid}/visits/detail/ocerview?visitId={visitid}&eventId={eventId} .
        Or via the function get_visit_namespr, when one knows the name of the visit and then extract the ID from there.

        Parameters
        ----------
        visitid : int
            ID of the visit, gets converted to a string.

        Returns
        -------
        dict
            JSON-dict with the details of the deleted visit or the OpenSpecimen's error message
        """

        endpoint = '/visits/' + str(visitid)
        url = self.base_url + endpoint

        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)


    def get_visit(self, visitid):

        """Get a Visit from OpenSpecimen

        Get an existing visit in OpenSpecimen with the Visit ID visitid. This has to be known and can
        be found out in the GUI by clicking on a participant and the visit. It looks like:
        http(s)://<host>:<port>/openspeicmen/cp-view/{cpid}/participant/{cprid}/visits/detail/ocerview?visitId={visitid}&eventId={eventId} .
        Or via the function get_visit_namespr, when one knows the name of the visit and then extract the id from there.

        Parameters
        ----------
        visitid : int
            ID of the visit, gets converted to a string.

        Returns
        -------
        dict
            JSON-dict with the details of the visit with ID visitid or the OpenSpecimen's error message
        """
        endpoint = '/visits/' + str(visitid)
        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def get_visit_namespr(self, search_string):

        """Get a Visit by the Name or the Surgical Pathology Number

        Get one or more visits by name or surgical pathology number. Parameters have to be known in advance 
        in order to use this function. If just the visitname is passed, one returns a visit with the corresponding name.
        If just the surgical pathology number is passed, it returns all visits attached to this number. If both are passed,
        it works as logical AND.

        Parameters
        ----------
        search_string : string
            string in the format '?name=visitname(optional)&sprNumer=sprnumber(optional)
        
        Returns
        -------
        dict
            JSON-dict with details of the visits.
        """

        endpoint = '/visits/bynamespr'+ str(search_string)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def get_visits_cpr(self, search_string):

        """Get a Visit by the Collection Protocol Registration ID.

        Get a visit by the collection protocoll registration ID. Parameters have to be known in advance 
        in order to use this function. They can be extracted from calling a search function in the 
        os_core class visits.

        Parameters
        ----------
        search_string : string
            string in the format '?cprId=cprid&includeStats=true/false(optional)'
        
        Returns
        -------
        dict
            JSON-dict with details of the visit.
        """
        
        endpoint = '/visits' + str(search_string)
        url= self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)

        
    def update_visit(self, visitid, params):

        """Updating a visit

        Update an existing visit with ID visitid and the parameters params. All parameters are
        optional for updating and those which are not passed, stay the same. Those parameters and 
        the visit ID have to be known to use this function and can
        be found out in the GUI by clicking on a participant and the visit. It looks like:
        http(s)://<host>:<port>/openspeicmen/cp-view/{cpid}/participant/{cprid}/visits/detail/ocerview?visitId={visitid}&eventId={eventId} .
        Or via the function get_visit_namespr, when one knows the name of the visit and then extract the ID from there.

        Note
        ----
        Mandatory fields are -cprId or (ppid and cpTitle) or (ppid and cpShortTitle),
        - name, -site

        Parameters
        ----------
        visitid : int
            ID of the visit as int or string, gets converted to a string
        
        params : string
            JSON- formatted string with parameters: cprId, eventId, eventLabel, eventPoint[optional], ppid, cptitle, cpShorttitle, name,
            clinicalDiagnoses[optional], clinicalStatus[optional], activityStatus [optional], site, status(permissable
            values: COMPLETE, PENDING, MISSED), missedReason[optional], missedBy[optional], comments[optional],
            surgicalPathologyNumber[optional], cohort[optional], visitDate[optional]

        Returns
        -------
        dict
            JSON-dict with details of the updated visit or OpenSpecimens error message 
        """

        endpoint = '/visits/' + str(visitid)
        url = self.base_url +endpoint
        payload = params
        r = self.OS_request_gen.put_request(url, payload)

        return json.loads(r.text)

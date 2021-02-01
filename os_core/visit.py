#! /bin/python3

# Import
import json
from datetime import datetime

from os_core.req_util import OS_request_gen

class visit:

    """Handles the API calls for Visits
    
    This class handles the API calls for OpenSpecimen Visits. It can create, delete, 
    search visits with different parameters, add visits to a collection protocol the Sytem.
    The outputs are JSON dicts or the Error messages as dict. I
    
    Notes
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes one can
    just pass the parameters via JSON-formatted string. This means the user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.
    
    Example
    -------
    A code example, where the Visits are handled is in the Jupyter-Notebook::
        $ jupyter notebook main.ipynb
    """

    def __init__(self, base_url, auth):

        """Constructor of the Class visit
        
        Constructor of the class visit, can handle the basic API-calls
        of the Visits in OpenSpecimen. Connects this class to OpenSpecimen
        specific request handle (os_core.request_util.py).
        
        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consits of two strings ( loginname , password)
        """ 

        self.OS_request_gen = OS_request_gen(auth)
        self.base_url = base_url


    def ausgabe(self):

        """Testing of the URL and authentification.
        
        If there are unexpected errors one can easily test if the URL and login data is correctly spelled.
        the function prints the URL and login data, handed over to the class, to the output terminal.
        """

        print(self.base_url, self.OS_request_gen.auth)        


    def add_visit(self, params):

        """Add a visit to a Participant.
        
        Add a visit to a participant in OpenSpecimen via API call. To use this function, one has to know the
        Parameters of the Participant, event and site.

        Note
        ----
        Mandatory fields are -cprId or (ppid and cpTitle) or (ppid and cpShortTitle)
        - name, site

        Parameters
        ----------
        params : string
            JSON formatted string with parameters: cprId, eventId, eventLabel, ppid, cptitle, cpShorttitle, name,
            clinicalDiagnoses[optional], clinicalStatus[optional], acitivtyStatus [optional], site, status(permissable
            values: COMPLETE, PENDING, MISSED), missedReason[optional], missedBy[optional], comments[optional],
            surgicalPathologyNumber[optional], cohort[optional], visitDate[optonal]
        
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
        of the Participants and event. Or one can use the create_visit_specimens function from the os_util
        class visit_util. 

        Note
        ----
        The visit fields can be seen in add_visit and the ones for specimens in create specimen.

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

        Delete an existing Visit in OpenSpecimen with the Visit ID visitid. This has to be known and can
        be found out in the GUI by clicking on a participant and the visit. It looks like:
        http(s)://<host>:<port>/openspeicmen/cp-view/{cpid}/participant/{cprid}/visits/detail/ocerview?visitId={visitid}&eventId={eventId} .
        Or via the function get_visit_namespr, when one know the name of the visit and then extract the id from there.

        Parameters
        ----------
        visitid : string or int
            Id of the visit, gets converted to a string.

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

        Get an existing Visit in OpenSpecimen with the Visit ID visitid. This has to be known and can
        be found out in the GUI by clicking on a participant and the visit. It looks like:
        http(s)://<host>:<port>/openspeicmen/cp-view/{cpid}/participant/{cprid}/visits/detail/ocerview?visitId={visitid}&eventId={eventId} .
        Or via the function get_visit_namespr, when one know the name of the visit and then extract the id from there.

        Parameters
        ----------
        visitid : string or int
            Id of the visit, gets converted to a string.

        Returns
        -------
        dict
            JSON-dict with the details of the visit with Id visitid or the OpenSpecimen's error message
        """
        endpoint = '/visits/' + str(visitid)
        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def get_visit_namespr(self, search_string)::

        """Get a Visit by the name or the Surgical pathology number

        Get one or more visits by the name or the surgical pathology number. Those parameters have to be known 
        in order to know this function. If just the visitname is passed one return a visit with the corresponding name.
        If just the surgical pathology number is passed it returns all visits with this number. If both are passed
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

        """Get a Visit by the Collection protocol Registration Id.

        Get a visits by the colelction Protocoll Registration ID. Those parameters have to be known 
        in order to know this function. They can be extracted from calling a search function in the 
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

        Update an existing Visit with Id visitid and the parameters params. All parameters are
        optional for updating and  those which are not passed stays the same. Those parameters and 
        the visit Id have to be known to use this function and can
        be found out in the GUI by clicking on a participant and the visit. It looks like:
        http(s)://<host>:<port>/openspeicmen/cp-view/{cpid}/participant/{cprid}/visits/detail/ocerview?visitId={visitid}&eventId={eventId} .
        Or via the function get_visit_namespr, when one know the name of the visit and then extract the id from there.

        Note
        ----
        Mandatory fields are -cprId or (ppid and cpTitle) or (ppid and cpShortTitle),
        - name, -site

        Parameters
        ----------
        visitid : int or string
            Id of the visit as int or string, gets converted to a string
        
        params : string
            JSON- formatted string with parameters: cprId, eventId, eventLabel, eventPoint[optional], ppid, cptitle, cpShorttitle, name,
            clinicalDiagnoses[optional], clinicalStatus[optional], acitivtyStatus [optional], site, status(permissable
            values: COMPLETE, PENDING, MISSED), missedReason[optional], missedBy[optional], comments[optional],
            surgicalPathologyNumber[optional], cohort[optional], visitDate[optonal]

        Returns
        -------
        dict
            JSON-dict with details of the updated visit or OpenSpecimens Error message
        """

        endpoint = '/visits/' + str(visitid)
        url = self.base_url +endpoint
        payload = params
        r = self.OS_request_gen.put_request(url, payload)

        return json.loads(r.text)
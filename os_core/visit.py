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
        of the Participants and event. 

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
        be found out in the GUI by clicking on a participant and the 

        Returns
        -------
        [type]
            [description]
        """

        endpoint = '/visits/' + str(visitid)
        url = self.base_url + endpoint

        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)

    
#   Get details of a Visit with id
#   Input:  - visitId:  Id of the visit
#   Output: - either details of the visit as json-formatted string
#           - or error message
    def get_visit(self, visitid):

        endpoint = '/visits/' + str(visitid)
        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


#   Get Visits By Name Or Surgical Pathology Number
#   Input:  - visitname:    Name of the visit
#           - sprnumber:    Surigical Pathology Number
#   Output: - either details of the visit as json formatted string
#           - or error message
    def get_visit_namespr(self, visitname=None, sprnumber=None):

        endpoint = '/visits/bynamespr?'

        if visitname!=None:
            endpoint += 'visitName=' + str(visitname)

        elif sprnumber!=None:
            endpoint += 'sprNumber=' + str(sprnumber)

        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


#   Get Visits By Registration Identifier
#   Input:  - cprid: Collection protocoll REgistration Id
#           - includestats: Default false, if true colletion status of visits
#   Output  - either json-formatted string
#           - or error messages
    def get_visits_cpr(self, cprid, includestats=None):
        
        endpoint = '/visits?cprId=' + str(cprid)
        print(bool(includestats))
        if bool(includestats):
            endpoint += '&includeStats=' + str(includestats)

        url= self.base_url + endpoint

        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)

        
#   Update Visit
#   Input:  - visitid:   ID of the visit
#           - params:   Parameter of the visit which should be updated as json-formatted string
#   Output: - either detail of the updated visit as json-formatted string
#           - or error message with details
    def update_visit(self, visitid, params):

        endpoint = '/visits/' + str(visitid)

        url = self.base_url +endpoint

        payload = params

        r = self.OS_request_gen.put_request(url, payload)

        return json.loads(r.text)
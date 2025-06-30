#! /bin/python3

# Import
from datetime import datetime
from .req_util import OS_request_gen
from .. import config_manager
import json


class specimen:
    
    """Handles the calls for Specimens
    
    This class handles the API calls for OpenSpecimen Specimens/Aliquots/Derivatives. It can create, delete, 
    search, and determine the existence of specimens with different parameters. Further, a list of all specimens in the system can be created.
    The output is a JSON dict or the error message as dict. 
    
    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes, one can
    just pass the parameters via a JSON-formatted string. This means the user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.
    
    Examples
    --------
    A code Examples, where the Specimens/Derivatives/Aliquots are handled, is in the Jupyter-Notebook
        $ jupyter notebook main.ipynb
    """

    def __init__(self):

        """Constructor of the Class collection_protocol
        
        Constructor of the class collection_protocol can handle the basic API-calls
        of the collection protocol in OpenSpecimen. Connects this class to OpenSpecimen
        specific request handle (os_core.request_util.py).
        
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
        

    def get_specimen(self, specimenid):
        
        """Get the Specimen with the ID specimenid
        
        Get the details of the Specimen with the unique ID specimenid.
        This ID is generated automatically from OpenSpecimen when the Specimen is created.
        It can be seen in the GUI by clicking on the desired Specimen, and read from the URL:
        http(s)://<host>:<port>/openspecimen/cps/{cpid}/specimens/{specimenid}/... .
        Otherwise via search Specimen, for Examples by name and then extract the ID via key ["id"].
        
        Parameters
        ----------
        specimenid : string or int
            The System's ID of the Specimen, which will be converted to a string.
        Returns
        -------
        JSON-dict
            Details of the Specimen with the specified ID, or the OpenSpecimen error message.
        """

        endpoint = '/' + str(specimenid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def check_specimen(self, specimenLabel):
        
        """Check if a Specimen with Label exists
        
        Check if a specimen with Label specimenLabel already exists in the System.
        Can be interesting if one manually creates a label to avoid specimens with the same label.
        
        Parameters
        ----------
        specimenLabel : string
            Label which should be checked as string. Gets converted to a string
        
        Returns
        -------
        string
            If Specimen exists, returns "Specimen with label <specimenLabel> exists".
            Or Else "Specimen with label <specimenLabel> does not exist".
        """

        endpoint = '?label=' + str(specimenLabel)
        url = self.base_url + endpoint
        r = self.OS_request_gen.head_request(url)

        if r.status_code == 200:
            r = 'Specimen with Label ' + str(specimenLabel) + ' exists.'
        else:
            r = 'Specimen with Label ' + \
                str(specimenLabel) + ' does not exist.'

        return r


    def create_specimen(self, params):

        """Creates a Specimen
        
        Creates a Specimen. In order to use this function one has to know
        the parameters which OpenSpecimen needs to create a Specimen. One can use it via the os_util class
        specimen_util.py. This allows just the basic definition, if one has extensions 
        e.g. BBMRI contact, this fields has to be added separately. 
        
        Parameters
        ----------
        params : string
            JSON formatted string with parameters: label[mandatory if its created manually, leave empty if the System creates it
            automatically], specimenclass, type, pathology, atomicSite, laterality, initialQty, availableQty, lineage,
            visitId,  status, storageLocation(dict with keys positionX[optional], 
            positionY[optional])[optional], concentration[optional], biohazards[optional], comments[optional],
            collectionEvent(DICT with keys user,time, container[otpional], procedure[optional]),
            receivedEvent(DICT with keys user, time, receivedQuality), extensionDetails(DICT with keys useUdn, attrsmap,
            DICT with extension keys)[optional]
            
        Returns
        -------
        json-dict
            Either details of the created specimen as dictionary or OpenSpecimen's error message
        """
        
        url = self.base_url 
        payload = params
        r = self.OS_request_gen.post_request(url, data=payload)

        return json.loads(r.text)

    
    def search_specimens(self, search_string):
        
        """Search for  Specimen with specific values.
        
        Search for one or more Specimens with the values in the search_string defined. The search string looks like:
        http(s)://<host>:<port>/openspecimen/rest/np/specimens?{param_1}={value_1}&...&{param_x}={value_x}
        With the class specimen_util from os_util and function search_specimens the search string is generated
        and this function is called. Not all keys from OpenSpecimen can be easily searched for.
        
        Parameters
        ----------
        search_string : string
            String with the following format: ?{param_1}={value_1}&...&{param_x}={value_x} . The parameters can be one of the following:
            label[optional], cprId[optional], eventId[optional], visitId[optional]
        Returns
        -------
        dict
            Details of the matching Specimens, if no one matches, it is an empty list.
        """
        
        endpoint = str(search_string)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)

    def update_specimen(self, specimenid, params):
        
        """Updates an existing Specimen/Aliquot/Derivative
        
        Updates an existing Specimen/Derivative/Aliquot with the automatically generated OpsenSpecimen's system wide
        unique specimen ID specimenid, with the parameters updateparams which are passed to the function.
        The ID of the specimen has to be known and can, for Examples, be seen in the GUI by clicking on 
        theSpecimen, which has the format http(s)://<host>:<port>/openspecimen/cps/{cpid}/specimen/{specimenid} .
        Or via the function search_specimens and extract from there with the key ["id"]
        
        Note
        ----
        The optional parameters are those, which are optional for a Specimen. For updating, all parameters are optional,
        those which are not passed to the function will stay the same as before.
        
        Parameters
        ---------
        cpid : int
            Unique Collection Protocol ID which is generated automatically from the System.
        
        params : string
            JSON formatted string with parameters: label[mandatory if its created manually, leave empty if the System creates it
            automatically], specimenclass, type, pathology, atomicSite, laterality, initialQty, availableQty, lineage,
            visitId, parentId[mandatory if Aliquot/Derivative], status, storageLocation(dict with keys positionX[optional],
            positionY[optional])[optional], concentration[optional],         biohazards[optional], comments[optional],
            collectionEvent(DICT with keys user,time, container[otpional], procedure[optional]),
            receivedEvent(DICT with keys user, time, receivedQuality), extensionDetails(DICT with keys useUdn, attrsmap,
            DICT with extension keys)[optional]
            
        Returns
        -------
        JSON-dict
            JSON-dict with the details of the updated Collection Protocol or the OpenSpecimen's error message.
        """

        endpoint = '/'+str(specimenid)
        url = self.base_url + endpoint
        data = params
        r = self.OS_request_gen.put_request(url, data)
        
        return json.loads(r.text)

    def delete_specimen(self, specimenids):
        
        """Delete a Specimen/Derivative/Aliquot
        
        Delete an already existing Specimen/Derivative/Aliquot. The Parameters specimenid is the uniqe ID of the Specimen/
        Derivative/Aliquot which is generated automatically from OpenSpecimen. To get the ID, one can click in the GUI on the 
        Specimen/Derivative/Aliquot and read it from the URL, with format:
        http(s)://<host>:<port>/openspecimen/cp-view/{cpid}/specimen/{specimenid}/... .
        Another possibility is to search via 'search_specimens' for a specific Parameters and then extract the ID
        from the JSON-dict which gets returned. The function allows also to delete a list of specimen
        
        Parameters
        ----------
        specimenids: string 
            The unique ID(s) of the Specimen/Aliquot/Derivative which OpenSpecimen creates itself. 
            Deleting specimens has the form "?id=specimenid_1+...+specimenid_n"
            
        Returns
        -------
        JSON-dict
            Details of the Specimens which are deleted or the OpenSpecimen error message as dict.
        """

        url = self.base_url + specimenids
        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)

##TODO create aliquot

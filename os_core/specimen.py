#! /bin/python3

# Import
from datetime import datetime
from os_core.req_util import OS_request_gen

import json


class specimen:
    
    """Handles the calls for Specimens
    
    This class handles the API calls for OpenSpecimen Specimens/Aliquots/Derivatives. It can create, delete, 
    search specimens with different parameters, get all specimens in the Sytem.
    The output is a JSON dict or the Error message as dict. It also can check if a
    specimen exists which returns a string which tells you if it exists.
    
    Notes
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes one can
    just pass the parameters via JSON-formatted string. This means the user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.
    
    Example
    -------
    A code example, where the Specimens/Derivatives/Aliquots are handled is in the Jupyter-Notebook::
        $ jupyter notebook main.ipynb
    """

    def __init__(self, base_url, auth):

        """Constructor of the Class collection_protocol
        
        Constructor of the class colelction_protocol, can handle the basic API-calls
        of the collection protocol in OpenSpecimen. Connects this class to OpenSpecimen
        specific request handle (os_core.request_util.py).
        
        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consits of two strings ( loginname , password)
        """ 
        
        self.OS_request_gen = OS_request_gen(auth)
        self.base_url = base_url + '/specimens'


    def ausgabe(self):
        
        """Testing of the URL and authentification.
        
        If there are unexpected errors one can easily test if the URL and login data is correctly spelled.
        the function prints the URL and login data, handed over to the class, to the output terminal.
        """

        print(self.base_url, self.OS_request_gen.auth)
        

    def get_specimen(self, specimenid):
        
        """Get the Specimen with the ID ::specimenid::
        
        Get the details of the Specimen with the unique ID ::cspecimenid::.
        This ID is generated automatically from OpenSpecimen when the Specimen is created.
        It can be seen in the GUI by clicking on the desired Specimen, and read from the URL:
        http(s)://<host>:<port>/openspecimen/cps/{cpid}/specimens/{specimenid}/... .
        Or via search Specimen, for example by name and then extract the ID via key ["id"].
        
        Parameters
        ----------
        specimenid : string or int
            The System's ID of the Specimen, will be converted to a string.
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
        
        Check if a Specimen with Label ::specimenLabel:: already exists in the System.
        Can be interesting if one manually creates Label to avoid Specimens with the same label.
        
        Parameters
        ----------
        specimenLabel : string
            Label which should be checked as string. Get converted to a string
        
        Returns
        -------
        string
            If Specimen exists, returns "Specimen with label <specimenLabel> exists".
            Else "Specimen with label <specimenLabel> does not exist".
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
        specimen_util.py. This allows just the basic definition, if one has Extensions 
        e.g. BBMRI contact, this fields has to be added separatly. 
        
        Parameters
        ----------
        params : string
            JSON formatted string with parameters: label[mandatory if its created manually, leave empty if the System creates it
            automatically], specimenclass, type, pathology, atomicSite, laterality, initialQty, availableQty, lineage,
            visitId,  status, storageLocation(dict with keys positionX[optional], 
            positionY[optional])[optional], concetration[optional], biohazards[optional], comments[optional],
            collectionEvent(DICT with keys user,time, container[otpional], procedure[optional]),
            receivedEvent(DICT with keys user, time, receivedQuality), extensionDetails(DICT with keys useUdn, attrsmap,
            DICT with extension keys)[optional]
            
        Returns
        -------
        json-dict
            Either details of the created Specimen as dictornary or OpenSpecimen's error message
        """
        
        url = self.base_url 
        payload = params
        r = self.OS_request_gen.post_request(url, data=payload)

        return json.loads(r.text)

    
    def search_specimens(self, search_string):
        
        """Search for  Specimen with specific values.
        
        Search for one or more Specimens with the values in the search_string defined. The search string looks like:
        http(s)://<host>:<port>/openspecimen/rest/np/specimens?{param_1}={value_1}&...&{param_x}={value_x}
        With the class specimen_util from os_util and function ::search_specimens:: the search string is generated
        and this function is called. Not all keys from OpenSpecimen can be easily searched after.
        
        Parameters
        ----------
        search_string : string
            String with the following format: ?{param_1}={value_1}&...&{param_x}={value_x} . The parameters can be one of the following:
            label[optional], cprId[optional], eventId[optional], visitId[optional]
        Returns
        -------
        dict
            Details of the matching Specimens, if no one matches it is an empty list.
        """
        
        endpoint = str(search_string)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)

    def update_specimen(self, specimenid, updateparams):
        
        """Updates a existing Specimen/Aliquot/Derivative
        
        Updates a existing Specimen/Derivative/Aliquot with the automatically generated OpsenSpecimen's system wide
        unique Specimen ID ::specimenid::, with the Parameters ::updateparams:: which are passed to the function.
        The ID of the Specimen have to be known and can for example be seen in the GUI by clicking on 
        theSpecimen, which has the format http(s)://<host>:<port>/openspecimen/cps/{cpid}/specimen/{specimenid} .
        Or via the function search_specimens and extract from there with the key ["id"]
        
        Note
        ----
        The optional parameters are those, which are optional for a Specimens. For updating all parameters are optional,
        does which are not passed to the function will stay the same as before.
        
        Parameter
        ---------
        cpid : strinf or int
            Unique Collection Protocol ID which is generated automatically from the System. It will be converted to a string.
        
        params : string
            JSON formatted string with parameters: label[mandatory if its created manually, leave empty if the System creates it
            automatically], specimenclass, type, pathology, atomicSite, laterality, initialQty, availableQty, lineage,
            visitId, parentId[mandatory if Aliquot/Derivative], status, storageLocation(dict with keys positionX[optional],
            positionY[optional])[optional], concetration[optional],         biohazards[optional], comments[optional],
            collectionEvent(DICT with keys user,time, container[otpional], procedure[optional]),
            receivedEvent(DICT with keys user, time, receivedQuality), extensionDetails(DICT with keys useUdn, attrsmap,
            DICT with extension keys)[optional]
            
        Returns
        -------
        JSON-dict
            JSON-dict with the details of the updated Colelction Protocol or the OpenSpecimen's error message.
        """

        endpoint = '/'+str(specimenid)
        url = self.base_url + endpoint
        data = updateparams
        r = self.OS_request_gen.put_request(url, data)
        
        return json.loads(r.text)


    def delete_specimen(self, specimenids):
        
        """Delete a Specimen/Derivative/Aliquot
        
        Delete an already existing Specimen/Derivative/Aliquot. The parameter ::specimenid:: is the uniqe ID of the Specimen/
        Derivative/Aliquot which is generated automatically from OpenSpecimen. To get the ID one can click in the GUI on the 
        Specimen/Derivative/Aliquot and read it from the URL, with format:
        http(s)://<host>:<port>/openspecimen/cp-view/{cpid}/specimen/{specimenid}/... .
        An other possibility is to search via 'search_specimens' for a specific parameter and then extract the ID
        from the JSON-dict which get returned. The function allows also to delete a list of specimen
        
        Parameters
        ----------
        specimenids: string 
            The unique ID(s) of the Specimen/Aliquot/Derivative which OpenSpecimen creates itselfs. 
            Deleting specimens has the form "?id=specimenid_1+...+specimenid_n"
            
        Returns
        -------
        JSON-dict
            Details of the Specimens which is deleted or the OpenSpecimen error message as dict.
        """

        url = self.base_url + specimenids
        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)

##TODO create aliquot
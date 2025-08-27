#! /bin/python3

# Import
from datetime import datetime
from .req_util import OS_request_gen
from .. import config_manager
import json


class catalog:
    
    """Handles the calls for Shipments
    
    This class handles the API calls for OpenSpecimen Shipments.
    The output is a JSON dict or the error message as dict. 
    
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

        """Constructor of the Class shipment
        
        Constructor of the shipment can handle the basic API-calls
        of the shipments in OpenSpecimen. Connects this class to OpenSpecimen
        specific request handle (os_core.request_util.py).
        
        Parameters
        ----------
        base_url : string
            URL to openspecimen, which has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consists of two strings ( loginname , password)
        """ 
        self.base_url = config_manager.get_url() + '/specimen-catalogs'
        self.auth = config_manager.get_auth()
        self.token = config_manager.get_token()
        self.OS_request_gen = OS_request_gen(self.auth, self.token)

        # https://pad.medunigraz.at/rest/ng/specimen-catalogs/6/specimen-requests/4

    def ausgabe(self):
        
        """Testing of the URL and authentification.
        
        If there are any unexpected errors, one can easily test if the URL and login data is spelled correctly.
        The function prints the URL and login data  to the output terminal, which was handed over to the class.
        """

        print(self.base_url, self.OS_request_gen.auth)
        

    def get_all_catalogs(self):
        """
        Retrieves all shipments by sending a GET request to a designated endpoint.

        This function constructs the full URL endpoint for fetching shipment data by appending
        an endpoint string to the base URL of the API. A GET request is then sent using the
        request generating utility, and the response is parsed as JSON.

        Returns
        -------
        dict
            A dictionary containing shipment data parsed from the JSON response.
        """


        endpoint = ""
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def get_metadata(self, catalog_id):
        
        """Get the Shipment with the ID shipmentid
        
        Get the details of the Shipment with the unique ID shipmentid.
        This ID is generated automatically from OpenSpecimen when the Shipment is created.
        It can be seen in the GUI by clicking on the desired Shipment, and read from the URL:
        http(s)://<host>:<port>/openspecimen/cps/{cpid}/specimens/{specimenid}/... .
        Otherwise via search Specimen, for Examples by name and then extract the ID via key ["id"].
        
        Parameters
        ----------
        shipmentid : string or int
            The System's ID of the Shipment, which will be converted to a string.
        Returns
        -------
        JSON-dict
            Details of the Specimen with the specified ID, or the OpenSpecimen error message.
        """

        endpoint = '/' + str(catalog_id)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def get_all_requests(self, catalog_id):

        """Get the Specimens of the Shipment with the ID shipmentid

        Get the details of the Specimens of the Shipment with the unique ID shipmentid.
        This ID is generated automatically from OpenSpecimen when the Shipment is created.
        It can be seen in the GUI by clicking on the desired Shipment, and read from the URL:
        http(s)://<host>:<port>/openspecimen/cps/{cpid}/specimens/{specimenid}/... .
        Otherwise via search Specimen, for Examples by name and then extract the ID via key ["id"].
        """
        endpoint = '/' + str(catalog_id) + '/specimen-requests'
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def get_specimens_request(self, catalog_id, request_id):

        endpoint = '/' + str(catalog_id) + '/specimen-requests/' + str(request_id)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def get_all_specimens(self, catalog_id):

        endpoint = '/' + str(catalog_id) + '/search'
        url = self.base_url + endpoint
        
        data = json.dumps({"criteria": []})

        r = self.OS_request_gen.post_request(url, data=data)

        return json.loads(r.text)


    def close_request(self, catalog_id, request_id, comment=""):

        endpoint = '/' + str(catalog_id) + '/specimen-requests/' + str(request_id) + '/status'
        url = self.base_url + endpoint

        data = json.dumps({
            "id": request_id,
            "reason": comment,
            "status": "Closed"
        })

        r = self.OS_request_gen.put_request(url, data)

        return json.loads(r.text)

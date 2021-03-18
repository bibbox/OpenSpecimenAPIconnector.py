#! /bin/python3

# Import
import json
from datetime import datetime
from .req_util import OS_request_gen
from .. import config_manager

class container:

    """Handles the API calls for the container operations

    Handles the OpenSpecimen API calls related to Container Management. This class can 
    get a container with a Participant Protocoll ID PPID or via search parameters.
    
    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes, one can
    just pass the parameters via a JSON-formatted string. This means the user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Examples
    --------

    A code Examples, where the institutes are handled, is in the Jupyter-Notebook:

        $ jupyter notebook main.ipynb
    """
    def __init__(self):

        """Constructor of the Class container

        Constructor of the class container to handle the basic API-calls
        of containers in OpenSpecimen.

        """
        self.base_url = config_manager.get_url() + '/storage-containers'
        self.auth = config_manager.get_auth()
        self.OS_request_gen = OS_request_gen(self.auth)
        self.jsons = Json_factory()

def create_container(self, params):

        """Creates a Container

        Creates a Container in OpenSpecimen. In order to use this function, one has to know
        the parameters which OpenSpecimen needs to create a protocol. One can use it via the os_util class
        container_util. This allows just the basic definition, if one has Extensions 
        e.g. BBMRI contact, this fields have to be added separately. 

        Parameters
        ----------
        params : string
            JSON formatted string with parameters: name(mandatory), barcode(optional), typeName(optional), 
            activitystatus(optional), sitename(mandatory), storageloc(optional), numcols(mandatory), numrows(mandatory), 
            storespecimens(mandatory), childcontainers(optional), temp(optional), columnlabelscheme(optional), 
            rowlablescheme(optional), comment(optional), specimenclasses(optional), specimentypes(optinal), 
            collectionprotocols(optional)

        Returns
        -------
        json-dict
            Either error details of the created container 
        """

        url = self.base_url + '/'
        payload = params
        r = self.OS_request_gen.post_request(url, payload)

        return json.loads(r.text)

def disable_container(self, containerid)
    """Delete a container

        Delete an already existing container. The Parameter <containerid> is the uniqe ID of the given Container
        which is generated automatically from OpenSpecimen. To get the ID, one can click in the GUI on the Container
        Details button and read it from the URL, with the format: http(s)://<host>:<port>/openspecimen/#/cp-view/{containerid}/overview.

    Parameters
    ----------
    containerid: int
        The unique ID of the collection protocol which OpenSpecimen creates itself as a string or integer. 
        It will get converted to a string.

    Returns
    -------
    JSON-formatted string
        
        Details of the Collection Protocol which is deleted or the OpenSpecimen error message as dict.
        """

        endpoint = '/' + str(containerid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)

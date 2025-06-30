#! /bin/python3

import json
from .req_util import OS_request_gen
from .jsons import Json_factory
from .. import config_manager

class collection_protocol():

    """Handles the calls Collection Protocol

    This class handles the API calls for OpenSpecimen Collection Protocol. It can create, delete, 
    search a Protocol with different parameters, can get all Collection Protocols in the system and can 
    get the template of the Collection Protocols as JSON dict or as Pandas dataframe.
    The output is a JSON dict or the error message as JSON dict, except the Pandas dataframe.
    

    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes, one can
    just pass the parameters via a JSON-formatted string. This means the user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Examples
    --------
    A code Examples, where the Collection protocols are handled, is in the Jupyter-Notebook

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
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consists of two strings (loginname , password)
        """
        self.base_url = config_manager.get_url() + '/collection-protocols'
        self.auth = config_manager.get_auth()
        self.OS_request_gen = OS_request_gen(self.auth)
        self.jsons = Json_factory()

    def ausgabe(self):

        """Testing of the URL and authentification.

        If there are any unexpected errors, one can easily test if the URL and login data is spelled correctly.
        The function prints the URL and login data to the output terminal, which was handed over to the class.
        """

        print(self.base_url, self.OS_request_gen.auth)


    def create_collection_protocol(self, data):

        """Creates a Collection Protocol

        Creates a Collection Protocol in OpenSpecimen. In order to use this function, one has to know
        the parameters which OpenSpecimen needs to create a protocol. One can use it via the os_util class
        collection_protocol_util. This allows just the basic definition, if one has Extensions 
        e.g. BBMRI contact, this fields have to be added separately. 

        Parameters
        ----------
        data : JSON-formatted string
            JSON formatted string with parameters: title, shortTitle, code[optional], startDate[optional],
            endDate[optional], principalInvestigator, coordinators[optional], irbId[optonal],
            anticipatedParticipantsCount[optional], activityStatus, visitNameFmt[optional],
            specimenLabel[optional], derivedlabelFormat[optional], ppIdFormat[optional], cpSites,
            manualPpidEnabled[optional], manualVisitNameEnabled[optional], manualSpecLabelEnabled[optional]

        Returns
        -------
        json-dict
            Either error details of the created protocol 
        """

        url = self.base_url + '/'
        payload = data
        r = self.OS_request_gen.post_request(url,payload)

        return json.loads(r.text)


    def delete_collection_protocol(self, cpid):

        """Delete a Collection Protocol with OpenSpecimens unique CollectionProtocolID

        Delete an already existing Collection Protocol. The Parameters <cpid> is the uniqe ID of the Collection Protocol
        which is generated automatically from OpenSpecimen. To get the ID, one can click in the GUI on the Collection Protocol
        Details button and read it from the URL, with the format: http(s)://<host>:<port>/openspecimen/#/cp-view/{cpid}/overview.
        Another possibility is to search via 'search_collection_protocols' for a specific Parameters and then extract the ID
        from the JSON-dict which gets returned.

        Parameters
        ----------
        cpid: int
            The unique ID of the collection protocol which OpenSpecimen creates itself as a string or integer. 
            It will get converted to a string.

        Returns
        -------
        JSON-dict
            Details of the Collection Protocol which is deleted or the OpenSpecimen error message as dict.
        """

        endpoint = '/' + str(cpid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.delete_request(url)

        return json.loads(r.text)


    def search_collection_protocols(self, search_string):

        """Search for  Collection Protocols with specific values.

        Search for one or more Collection Protocols with the search_string defined. The search string looks like:
        http(s)://<host>:<port>/openspecimen/rest/np/collection-protocols?{param_1}={value_1}&...&{param_x}={value_x}
        With the class collection_protocol_util from os_util and function <search_cps> the search string is generated
        and this function is called. Not all keys from OpenSpecimen can be easily searched for.

        Parameters
        ----------
        search_string : string
            String with the following format: ?{param_1}={value_1}&...&{param_x}={value_x} . The parameters can be one of the following:
            searchString (OpenSpecimen's AQL)[optional], title[optional], piId (Principa Investigator)[optional], 
            repositoryName[optional], startAt[optional], maxResults[optional], detailedList[optional]

        Returns
        -------
        JSON-dict
            [Details of the matching Collection Protocols, if no one matches it, is an empty list.
        """

        endpoint =  str(search_string)
        url = self.base_url+endpoint
        
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def get_all_collection_protocols(self):

        """Get all Collection Protocol

        Get all Collection Protocols within the OpenSpecimen distribution, which is defined in the base_url.


        Returns
        -------
        JSON-dict
            Details of all Collection Protocols, which are in the OpenSpecimenDistribution.
        """

        url = self.base_url
        r = self.OS_request_gen.get_request(url)
        return json.loads(r.text)


    def get_collection_protocol(self, cpid):

        """Get the Collection Protocol with the ID cpid

        Get the details of the Collection Protocol with the unique ID cpid.
        This ID is generated automatically from OpenSpecimen when the Protocol is created.

        Parameters
        ----------
        cpid : int
            The System's ID of the Collection Protocol will be converted to a string.

        Returns
        -------
        JSON-dict
            Details of the Collection Protocol with the specified ID, or the OpenSpecimen error message.
        """

        endpoint = '/' + str(cpid)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return json.loads(r.text)


    def merge_colelction_protocols(self, params):

        """Merge two Collection Protocols

        Merge two Collection Protocols which are defined in params. To call this function the short titles of
        the source and target collection protocol have to be known. The Parameters <params> is a json-formatted string,
        with keys srcCPShortTitle and tgtCpShorttitle. The merged Protocol is the one with short title tgtCpShortTitle,
        with merge logic outer. 

        Note
        ----
        Merging is restricted to Super Admins. The CPs must have the same format for PPID, visits and specimens. 
        Or the target CP has no specific formats. 

        Parameters
        ----------
        params : string
            JSON formatted string with keys srcCpShortTitle and tgtCpShortTitle and the corresponding short titles as values.

        Returns
        -------
        JSON-dict
            JSON dict with the short titles of the source and target Collection Protocols.           
        """

        endpoint = '/merge'
        url = self.base_url + endpoint
        r = self.OS_request_gen.post_request(url, params)

        return json.loads(r.text)

    def update_collection_protocol(self, cpid, params):

        """Updates an existing Collection Protocol with ID cpid with the Parameters params

            Updates an existing Collection Protocol with the automatically generated OpenSpecimen's system wide
            unique Collection Protocol ID cpid, with the Parameters params which are passed to the function.
            The ID of the Collection Protocol has to be known and can, for example, be seen in the GUI by clicking on 
            the Collection Protocol, which has the format http(s)://<host>:<port>/openspecimen/cps/{cpid}/... .
            Or via the function search_collection_protocols or get_all_collection_protocols

        Note
        ----
            For updating, all parameters are optional. Those parameters which are not passed to the function, will stay the same as before.

        Parameters
        ---------
        cpid : int
            Unique Collection Protocol ID which is generated automatically from the System. It will be converted to a string.

        params : string
            JSON-formatted string with the parameters should get updated. The keys which can get updated are: 
            title, shortTitle, code[optional], startDate[optional], endDate[optional], principalInvestigator, 
            coordinators[optional], irbId[optonal], anticipatedParticipantsCount[optional], activityStatus, visitNameFmt[optional],
            specimenLabel[optional], derivedlabelFormat[optional], ppIdFormat[optional], cpSites,
            manualPpidEnabled[optional], manualVisitNameEnabled[optional], manualSpecLabelEnabled[optional]

        Returns
        -------
        JSON-dict
            JSON-dict with the details of the updated Collection Protocol or the OpenSpecimen's error message.
        """

        endpoint = '/' + str(cpid)
        url = self.base_url + endpoint
        payload = params
        r = self.OS_request_gen.put_request(url, payload)

        return json.loads(r.text)

    def get_cp_pandas_template(self):

        """Template for the Collection Protocol

        Template for the Collection Protocol as specified within the system. If, for Examples, some extension details
        for the Collection Protocols exists, this function will return also those values. These values are converted into a pandas 
        dataframe, precisely, it is the header of a pandas data frame.

        Returns
        -------
        pandas.core.dataframe
            Empty pandas dataframe with OpenSpecimen keys as header inclusive extension details.
        """

        site_template_endpoint = "/import-jobs/input-file-template?schema=cp"
        site_template_url = self.base_url + site_template_endpoint
        r = self.OS_request_gen.get_request(site_template_url)
        cp_pandas_template = pd.DataFrame(columns=[r.content.decode()])

        return cp_pandas_template



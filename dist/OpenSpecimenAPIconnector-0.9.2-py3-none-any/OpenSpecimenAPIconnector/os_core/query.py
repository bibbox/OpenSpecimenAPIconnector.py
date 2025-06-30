#! /bin/python3


import json
from .req_util import OS_request_gen
from .. import config_manager

class query:

    """Handles the API calls for the queries

    Handles the OpenSpecimen API calls for the queries. This class can 
    create, execute, search for queries. Also it can create a query in the OpenSpecimen specific Querylanguage AQL.
    
    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes, one can
    just pass the parameters via a JSON-formatted string. This means the user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Examples
    --------

    A code Examples, where the Queries are handled, is in the Jupyter-Notebook:

        $ jupyter notebook main.ipynb
    """

    def __init__(self):

        """Constructor of the Class query.

        Constructor of the class query can handle the basic API-calls
        of the query in OpenSpecimen. Connects this class to OpenSpecimen
        specific URL Generator Class (os_core/url.py)

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


    def execute_aql(self, params):


        """Write and Execute a Query in OpenSpecimen

        Creates a query which then is executed. The query language AQL can be extracted from the OpenSpecimen GUI query generator.
        The possible metainfos are written like schemaname.key. To use this class, one has to know the AQL language.

        Parameters
        ---------
        params : string
            JSON-formatted string with the desired parameters. cpId, aql, wideRowMode(default ='OFF') [optional] ,
            outputColumnExprs (default= 'true')[optional], outputIsoDateTime (default = 'true)[optional]

        Returns
        -------
        JSON-dict
            Details of the outcomes of the query with metadata, labels, and columns or the OpenSpecimen's error message.
        """

        endpoint = "/query"
        url = self.base_url + endpoint
        data = params
        r = self.OS_request_gen.post_request(url, data)

        return json.loads(r.text)


    def search_query(self, suburl):

        """Search for list of queries with specific suburl.

        Search for one or more queries with the parameters in the suburl defined. The search URL looks like:
        http(s)://<host>:<port>/openspecimen/rest/np/saved-queries?{param_1}={value_1}&...&{param_x}={value_x}

        Parameters
        ----------
        suburl : string
            Suburl of the queries with parameters: cpId, searchString, start, max, countReq

        Returns
        -------
        JSON-dict
            Details of all matching queries or the OpenSpecimen's error message.
        """

        endpoint = '/saved-queries' + str(suburl)
        url = self.base_url + endpoint
        r = self.OS_request_gen.get_request(url)

        return  json.loads(r.text)


    def execute_query(self, qryid, params):

        """Execute a saved Query.

        Execute an already existing query with the OpenSpecimen's unique Query ID <qryid> .
        The query ID can be seen via clicking on the queries in OpenSpecimen and it is the
        number after # in the title.

        Parameters
        ----------
        qryid : string or int
            The systems ID of the query will be converted to a string.

        params : string
            JSON-formatted string with parameters: drivingForm, wideRowmode,
            startAt, maxResults  

        Returns
        -------
        JSON-dict
            Details of all matching queries or the OpenSpecimen's error message.
        """

        endpoint = "/query/" + str(qryid)
        url = self.base_url + endpoint
        data = params
        r = self.OS_request_gen.post_request(url, data)

        return json.loads(r.text)

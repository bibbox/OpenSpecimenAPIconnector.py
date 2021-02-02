#! /bin/python3


import json
from ..os_core.req_util import OS_request_gen


class query:

    """Handles the API calls for the queries

    Handles the OpenSpecimen API calls for the queries. This class can 
    create, execute, search for queries. Also it can create a Query in the OpenSpecimen specific Querylanguage AQL.
    
    Notes
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes one can
    just pass the parameters via JSON-formatted string. This means the user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Example
    -------

    A code example, where the Queries are handled is in the Jupyter-Notebook:

        $ jupyter notebook main.ipynb
    """

    def __init__(self, base_url, auth):

        """Constructor of the Class query.

        Constructor of the class query, can handle the basic API-calls
        of the query in OpenSpecimen. Connects this class to OpenSpecimen
        specific URL Generator Class (os_core/url.py)

        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consits of two strings ( loginname , password)
        """

        self.OS_request_gen = OS_request_gen(auth = auth)
        self.base_url = base_url
        

    def ausgabe(self):

        """Testing of the URL and authentification.

        If there are unexpected errors one can easily test if the URL and login data is correctly spelled.
        the function prints the URL and login data, handed over to the class, to the output terminal.
        """

        print(self.base_url, self.OS_request_gen.auth)


    def create_query(self, params):

        """Create a Query in OpenSpecimen

        Creates a Query which is stored in the Queries in OpenSpecimen. The query language 
        can be extracted from the OpenSpecimen GUI query generator.

        Parameter
        ---------
        params : string
            JSON-formatted string with the desired parameters.

        Returns
        -------
        JSON-dict
            Details of the saved query or the OpenSpecimen's error message.
        """

        endpoint = "/saved-queries/"
        url = self.base_url + endpoint
        data = params
        r = self.OS_request_gen.post_request(url,data)

        return json.loads(r.text)


    def create_aql(self, params):


        """Write and Execute a Query in OpenSpecimen

        Creates a Query which then is executed. The query language AQL can be extracted from the OpenSpecimen GUI query generator.
        The possible metainfos are written like schemaname.key. To use this class one has to know the AQL language.

        Parameter
        ---------
        params : string
            JSON-formatted string with the desired parameters. cpId, aql, wideRowMode(default ='OFF') [optional] ,
            outputColumnExprs (default= 'true')[optional], outputIsoDateTime (default = 'true)[optional]

        Returns
        -------
        JSON-dict
            Details of the outcomes of the query with metadata, labels, and coloumns or the OpenSpecimen's error message.
        """

        endpoint = "/query"
        url = self.base_url + endpoint
        data = params
        r = self.OS_request_gen.post_request(url, data)

        return json.loads(r.text)


    def search_query(self, suburl):

        """Search for list of queries with specific suburl.

        Search for one or more queries with the parameters in thesuburl defined. The search URL looks like:
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

        Execute a already existing Query with the OpenSpecimen's unique Query ID ::qryid:: .
        The query ID can be seen via clicking on the Queries in OpenSpecimen and it is the
        number after # in the title.

        Parameters
        ----------
        qryid : string or int
            The System's ID of the Query, will be converted to a string.

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
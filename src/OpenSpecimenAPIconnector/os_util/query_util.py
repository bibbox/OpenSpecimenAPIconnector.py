#! /bin/python3

from ..os_core.query import query
from ..os_core.jsons import Json_factory
from ..os_core.url import url_gen
import json
import io
import pandas
import time

class query_util:

    """Handles the API calls for the queries

    Handles the OpenSpecimen API calls for the queries. This class can 
    create, execute, search for queries.  The other calls are in the os_core class query.
    
    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. 
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Examples
    --------

    A code Examples, where the queries are handled is in the Jupyter-Notebook:

        $ jupyter notebook main.ipynb
    """

    def __init__(self):

        """Constructor of the Class query.

        Constructor of the class query, can handle the basic API-calls
        of the query in OpenSpecimen. Connects this class to the os_core classes
        query, Json_factory and url_gen.

        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consists of two strings ( loginname , password)
        """

        self.query = query()
        self.jsons = Json_factory()
        self.url = url_gen()
        

    def create_aql(self, cpid, aql, rowmode='OFF', columnexpr='true', isodate='true'):
        
        """Create a Query in OpenSpecimen

        Creates a Query which is stored in the Queries in OpenSpecimen. The query language 
        can be extracted from the OpenSpecimen GUI query generator.

        Parameters
        ---------
        cpid : int
            The collection Protocol ID  where the query gets assigned to.

        aql : string
            Command to execute in the OpenSpecimen's Advanced Query Language.

        rowmode : string
            Permissable Values OFF/SHALLOW/DEEP. Specify if multi-valued attributes result in a single row or one row per value.
        
        columnexpr : string
            Permissable values true/false. If true Userfriendly column labels are included in the response.

        isodate : string
            Permissable values are true/false. If true, the API accepts a ISO-date-format(yyy-MM-dd'T'HH:mm:ss), or else it takes the format from the OS local settings.

        Returns
        -------
        JSON-dict
            Details of the saved query or the OpenSpecimen's error message.
        """

        params = self.jsons.execute_aql(cpid, aql, rowmode, columnexpr, isodate)
        r = self.query.execute_aql(params)

        return r


    def execute_query(self, qryid, start='0', results='100', rowmode="OFF", drivingform="Participant"):

        """Execute a saved Query.

        Execute an already existing Query with the OpenSpecimen's unique Query ID <qryid> .
        The query ID can be seen via clicking on the Queries in OpenSpecimen and it is the
        number after # in the title.

        Parameters
        ----------
        qryid : int
            The System's ID of the Query, will be converted to a string.

        start : int
            Defines the row of the outcomes from which they will be displayed.
        
        results : int
            Defines how many results will be displayed.

        rowmode : string
            Permissable values are DEEP/SHALLOW/OFF.  If OFF all values of a multivalued field are shown in one row.
        
        drivingform : string
            Defines the search perspective, precisely which tables are searched at, permissable values are Participant, Specimen.

        Returns
        -------
        JSON-dict
            Details of all matching queries or the OpenSpecimen's error message.
        """

        params = self.jsons.execute_query(start = start, results = results, drivingform = drivingform, rowmode = rowmode)
        r = self.query.execute_query(qryid = qryid, params = params)

        return json.dumps(r)


    def search_query(self, cpid = None, searchstring = None, start = None, max_ = None, countreq = None):

        """Search for list of queries with specific suburl.

        Search for one or more queries with the parameters in the suburl defined. The search URL looks like:
        http(s)://<host>:<port>/openspecimen/rest/np/saved-queries?{param_1}={value_1}&...&{param_x}={value_x}

        Parameters
        ----------
        cpid : int
            The collection Protocol ID  where the query is assigned to.

        searchstring : string
            Substring of the query title.
        
        start : int
            Defines the row of the outcomes from which they will be displayed.
        
        max_ : int
            Defines how many results will be displayed.

        countreq : string
            OpenSpecimen's boolean, if true total number of saved queries will be shown.

        Returns
        -------
        JSON-dict
            Details of all matching queries or the OpenSpecimen's error message.
        """

        params = self.url.query_url_gen(cpid = cpid, searchstring = searchstring, start = start,
                                        max_ = max_, countreq = countreq)
        r = self.query.search_query(suburl = params)

        return r

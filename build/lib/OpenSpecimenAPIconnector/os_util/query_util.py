#! /bin/python3

from ..os_core.query import query
from ..os_core.jsons import Json_factory
from ..os_core.url import url_gen
import json
import re

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


    def aql_helper(self, datafields=["Participant.id", "Specimen.id"], search=[('CollectionProtocol.id', 'exists', None)], limit=None, binder="and"):
        """Builds an AQL query string from components.

        This helper function constructs a valid AQL (Advanced Query Language)
        string from a list of data fields to select and a list of search
        conditions. It includes validation for field names, operators, and
        values to prevent malformed queries and provides basic protection
        against injection by whitelisting operators and validating field formats.

        Parameters
        ----------
        datafields : list[str], optional
            A list of strings representing the data fields to be returned by
            the query (e.g., ["Participant.id", "Specimen.id"]).
        search : list[tuple], optional
            A list of tuples, where each tuple defines a search condition
            in the format (field, operator, value).
            Example: [('CollectionProtocol.id', '=', 1), ('Specimen.label', 'contains', 'S1')].
        limit : int, optional
            The maximum number of records to return. If None, no limit is applied.
        binder : str, optional
            The logical operator ('and' or 'or') used to join multiple search
            conditions in the 'where' clause. Defaults to "and".

        Returns
        -------
        str
            A formatted AQL query string ready to be executed.

        Raises
        ------
        AssertionError
            If `datafields` or `search` are empty, or if inputs have incorrect types.
        ValueError
            If an invalid binder, operator, field format, or value is provided.
        """



        assert len(datafields) > 0, "You have to specify datafields to return!"
        assert isinstance(datafields, list), "Variable <datafields> has to be a list of strings."
        assert len(search) > 0, "You have to search for something!"
        assert isinstance(search, list), "Variable <search> has to be a list of tuples."
        assert isinstance(binder, str), "Variable <binder> has to be a string."

        # Whitelist validation for binder
        allowed_binders = ['and', 'or']
        if binder.lower() not in allowed_binders:
            raise ValueError(f"Invalid binder: '{binder}'. Allowed values are {allowed_binders}.")

        # Regex validation for datafields
        field_pattern = re.compile(r"^[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)+$")
        for field in datafields:
            if not field_pattern.match(field):
                raise ValueError(f"Invalid datafield format: '{field}'")

        # Whitelist validation for search operators
        allowed_ops = ['=', '!=', '<', '>', '<=', '>=',
                       'exists', 'not exists', 'any',
                       'in', 'not in', 'between',
                       'starts with', 'ends with', 'contains']

        # Safely build search conditions
        where_clauses = []
        for condition in search:
            field, op, value = condition
            if not field_pattern.match(field):
                raise ValueError(f"Invalid field format in search condition: '{field}'")
            if op.lower() not in allowed_ops:
                raise ValueError(f"Invalid operator in search condition: '{op}'")

            op_lower = op.lower()

            if op_lower in ['exists', 'not exists', 'any']:
                where_clauses.append(f"{field} {op}")
            elif op_lower in ['in', 'not in']:
                if not isinstance(value, (list, tuple)):
                    raise ValueError(f"Value for '{op}' must be a list or tuple.")

                safe_values = []
                for item in value:
                    if isinstance(item, str):
                        safe_values.append('"' + item.replace('"', '\\"') + '"')
                    else:
                        safe_values.append(str(item))
                where_clauses.append(f"{field} {op} ({', '.join(safe_values)})")
            elif op_lower == 'between':
                if not isinstance(value, (list, tuple)) or len(value) != 2:
                    raise ValueError(f"Value for 'between' must be a list or tuple of 2 elements.")

                safe_values = []
                for item in value:
                    if isinstance(item, str):
                        safe_values.append('"' + item.replace('"', '\\"') + '"')
                    else:
                        safe_values.append(str(item))
                where_clauses.append(f"{field} {op} ({', '.join(safe_values)})")
            else: # Handles =, !=, <, >, <=, >=, starts with, ends with, contains
                if isinstance(value, str):
                    safe_value = '"' + value.replace('"', '\\"') + '"'
                else:
                    safe_value = str(value)
                where_clauses.append(f"{field} {op} {safe_value}")

        aql = f'select {", ".join(datafields)} where {(" " + binder + " ").join(where_clauses)}'

        if limit:
            assert isinstance(limit, int), "Variable <limit> has to be an integer."
            assert limit > 0, "A limit can not be smaller than zero!"
            limits = [str(0), str(limit)]
            aql = f'{aql} limit {", ".join(limits)}'

        return aql

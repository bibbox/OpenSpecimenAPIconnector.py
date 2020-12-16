#! /bin/python3

from os_core.query import query
from os_core.req_util import OS_request_gen
from os_core.jsons import Json_factory
import json
import io
import pandas
import time

class query_util:

    #   Constructor
    def __init__(self, base_url, auth):

        self.query = query(base_url=base_url, auth=auth)
        self.jsons = Json_factory()
        


# Create a query

    def create_aql(self, cpid, aql, rowmode='OFF', coloumexpr='true', isodate='true'):
        
        params = self.jsons.create_aql(cpid, aql, rowmode, coloumexpr, isodate)

        r = self.query.create_aql(params)

        return r

# Execute a saved Query
    def execute_query(self,qryid, start, results, rowmode="OFF", drivingform="Participant"):

        params = self.jsons.execute_query(start, results, drivingform, rowmode)

        r = self.query.execute_query(qryid, params)

        return json.dumps(r)
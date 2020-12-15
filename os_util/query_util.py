#! /bin/python3

from os_core.query import query
from os_core.req_util import OS_request_gen
import json
import io
import pandas
import time

class query_util:

    #   Constructor
    def __init__(self, base_url, auth):

        self.query = query(base_url=base_url, auth=auth)


# Create a query

    def create_query(self, cpid, aql, rowmode, coloumexpr, isodate):

        params = '{\"cpId\":\"' + str(cpid) + '\",\"aql\":\"' + str(aql) + '\",\"wideRowMode\":\"' + str(rowmode) + '\",\"outputColumnExprs\":\"' \
                + str(coloumexpr) + '\",\"outputIsoDateTime\":\"' + str(isodate) + '\"}'

        r =query.execute_query(params)

        return json.loads(r.text)
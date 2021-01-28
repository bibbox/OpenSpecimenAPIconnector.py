#! /bin/python3

from os_core.csv_bulk import csv_bulk
from os_core.req_util import OS_request_gen
import io
import pandas
import time

class bulk_operations:

    #   Constructor
    def __init__(self, base_url, auth):

        self.csv_bulk = csv_bulk(base_url=base_url, auth=auth)

    def bulk_import(self, file, filename, schemaname, operation='CREATE',
                    dateformat=None, timeformat=None):

        fileid = self.csv_bulk.upload_csv(filename, file)
        upload_ = self.csv_bulk.run_upload(schemaname=schemaname, fileid=fileid, operation=operation,
                                           dateformat=dateformat, timeformat=timeformat)

        jobid = upload_[0]    

        #Job report has to be created, if there is no sleep, there is an error, 
        time.sleep(5)

        r = self.csv_bulk.job_report(jobid)
        print(r)

        data = io.StringIO(r)
        ret_val = pandas.read_csv(data, sep=",")
        ret = ret_val.iloc[:, [2, -2, -1]]

        return ret

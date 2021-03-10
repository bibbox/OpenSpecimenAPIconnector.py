#! /bin/python3

from ..os_core.csv_bulk import csv_bulk
import io
import pandas
import time
import json

class bulk_operations:

    """Handles the OpenSpecimen CSV Bulk Importer via API.

    Handles the API calls of the OpenSpecimen's Bulk Importer for all the different schemas. 
    This class makes and executes an Import JOB.

    Note
    ----
    The OpenSpecimen Documentation of Bulk Import can be seen at 
    https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/440434702/Bulk+Import+via+API .
    """

    def __init__(self):

        """Constructor of the class csv_bulk

        Constructor of the class csv_bulk. It also connects this class to the os_core class csv_bulk.
        """
        self.csv_bulk = csv_bulk()

    def bulk_import(self, file, filename, schemaname, operation='CREATE',
                    dateformat=None, timeformat=None):
        
        """Make and Run a CSV-bulk import job

        Make a JOB, precisely upload a file to OpenSpecimen, extract the file-ID token from this return
        and then execute it with the right schema and operation (Create or Update). To use this function one has to
        know which entity should be created or updated and which fields are mandatory. 

        Parameters
        ----------
        file : binary
            The file to upload, is a CSV-file with separator ','.
        
        filename : string
            Name of the file with ending (.csv)
        
        schemaname : string
            The schemaname in OpenSpecimen with permissable values are: cp, cpr, user, userRoles,
            site, shipment, institute, dpRequirement, distributionProtocol, distributionorder,
            storagecontainer, storagecontainerType, containerShipment, cpe, masterSpecimen, participant,
            sr, visit, specimenAliquot, specimenDerivative, specimendisposal, consent

        operation : string
            String with Information if the file updates data or create it. Default value = 'CREATE'.
            Permissable values are CREATE or UPDATE
        
        dateformat : string
            If another dateformat than in the OpenSpecimen System configuration is taken, this has to be specified.
        
        timeformat : string
           If another timeformat than in the OpenSpecimen System configuration is taken, this has to be specified.

        Returns
        -------
        Pandas DataFrame 
            Data Frame with label, OS_IMPORT_STATUS OS_IMPORT_MESSAGE as column headers.
        """

        fileid = self.csv_bulk.upload_csv(filename, file)
        upload_ = self.csv_bulk.run_upload(schemaname=schemaname, fileid=fileid, operation=operation,
                                           dateformat=dateformat, timeformat=timeformat)

        jobid = upload_[0]
        job_pending = True    
        while job_pending:
            status = json.loads(self.csv_bulk.get_job_status(jobid))
            time.sleep(0.05) # limit request rate
            if status["status"] == "FAILED" or status["status"] == "COMPLETED":
                job_pending = False

        r = self.csv_bulk.job_report(jobid)

        data = io.StringIO(r)
        ret = pandas.read_csv(data, sep=",").fillna("0")
        found = ret[ret["OS_IMPORT_STATUS"].str.contains('SUCCESS')]
        found_same = ret[ret["OS_ERROR_MESSAGE"].str.contains('same', na=False)]

        check = found_same.count()["OS_IMPORT_STATUS"] + found.count()["OS_ERROR_MESSAGE"]
        
        assert check == len(ret["OS_IMPORT_STATUS"]), "Error creating {} by CSV: \n".format(schemaname) + str(ret)
        assert not ret.empty, "Error creating {} by CSV: Empty Return".format(schemaname)
        return ret

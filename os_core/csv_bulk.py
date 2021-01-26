#! /bin/python3

import pandas
import json
import io
import requests

from datetime import datetime

from os_core.req_util import OS_request_gen
from os_core.jsons import Json_factory


class csv_bulk:
    """Handles the OpenSpecimen CSV Bulk Importer via API.

    Handles the API calls of the OpenSpecimen's Bulk Importer for all the different schemas. 
    this class can get the templates to a schema, upload the csv-files, run the job, get the job status
    and get the job report.

    Note
    ----
    The OpenSpecimen Documentation of Bulk Import can be seen at 
    https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/440434702/Bulk+Import+via+API .
    File uploading in OpenSpecimen are two calls, which here are two seperated calls, via the
    function bulk_import fron the os_util class bulk_operations this calls get one call.
    """

    def __init__(self, base_url, auth):

        """Constructor of the class csv_bulk

        Constructor of the class csv_bulk. It also connects this class to the OpenSpecimen specific requests class
        OS_request_gen, and the OpenSpecimen standard JSON-dict generater clas JSON_factory
        """
       
        self.OS_request_gen = OS_request_gen(auth)
        self.Json_fact = Json_factory()
        self.base_url = base_url + '/import-jobs'
        self.auth = auth


    def ausgabe(self):

        """Testing of the URL and authentification.

        If there are unexpected errors one can easily test if the URL and login data is correctly spelled.
        the function prints the URL and login data, handed over to the class, to the output terminal.
        """

        print(self.base_url, self.OS_request_gen.auth)


    def get_template(self, schemaname):
    
        """Get the Templates to the corresponding schema

        Get the Templates of a OpenSpecimen schema and loads it into an empty pandas dataframe,
        where the OpenSpecimen specific keys are the header of the dataframe. To use this class one has to know the 
        schemanames which are used in OpenSpecimen. They are written in camelCase.

        Note
        ----
        The schemanames can be seen at: https://docs.google.com/spreadsheets/d/1fFcL91jSoTxusoBdxM_sr6TkLt65f25YPgfV-AYps4g/edit#gid=0

        Parameters
        ----------
        schemaname : string
            String in camelCase of the schema, permissable values are: cp, specimen, cpr, user, userRoles, site, shipment,
            institute, dpRequirement, distributionProtocol, distributionOrder, storageContainer, storageContainertype,
            containerShipment, cpe, masterSpecimen, participant, sr, visit, specimenAliquot, specimenDerivatice,
            specimenDisposal, consent

        Returns
        -------
        pandas core dataframe
            Empty dataframe with OpenSpecimen's keys to the corresponding schema.
        """

        endpoint = '/input-file-template?schema=' + str(schemaname)
        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url)

        data = io.StringIO(r.text)
        ret_val = pandas.read_csv(data, sep=",",encoding='UTF-8', engine='python')

        return ret_val



    def upload_csv(self, filename, file):

        """Upload a CSV file to OpenSpecimen

        First part of uploading a CSV file to OpenSpecimen. This creates a job with a file-id.
        With the file-id the job then can be started via the function run_upload.

        Note
        ----
        The values are separeted by comma ','. This is the OpenSpecimen standard format.

        Parameters
        ----------
        filename : string
            The name of the file which should get uploaded as string with the ending, here .csv .
        
        file : binary
            The file itself which should get uploaded.

        Returns
        -------
        list
            The Job-Id as list with length 1.
        """

        endpoint = '/input-file'
        url = self.base_url + endpoint
        files = [('file', (filename, file, 'text/csv'))]

        r = self.OS_request_gen.post_request(url=url, files=files)

        return json.loads(r.text)["fileId"]


    def run_upload(self, schemaname, fileid, operation = 'CREATE', dateformat = None, timeformat = None):

        """Run a the job which is already created.

        Runs a Job, which is already created. The schema and fileid have to be known. Moreover one has to specify if 
        the Job updates already existing objects or create new ones.

        Note
        ----
        The date and timeformat can be left empty if it is compatible with OpenSpecimen.

        Parameters
        ----------
        schemaname : string
            String in camelCase of the schema, permissable values are: cp, specimen, cpr, user, userRoles, site, shipment,
            institute, dpRequirement, distributionProtocol, distributionOrder, storageContainer, storageContainertype,
            containerShipment, cpe, masterSpecimen, participant, sr, visit, specimenAliquot, specimenDerivative,
            specimenDisposal, consent

        fileid : string
            The file-id, from OpenSpecimen generated , which is generated when the file is uploaded.

        operation : string
            The permissable operations are 'CREATE' and 'UPDATE'.

        dateformat : string
            An optional parameter, which has to be specified if the format is not compatible with OpsenSpeimen.

        timeformat : string
            An optional parameter, which has to be specified if the format is not compatible with OpsenSpeimen. 


        Returns
        -------
        string
            A tupple with the format ('JOBID', 'Response Text').
        """

        url = self.base_url
        payload = self.Json_fact.create_cpr_part_import_job(schemaname=schemaname, operation=operation, fileid=fileid,
                                                            dateformat=dateformat, timeformat=timeformat)
        r = self.OS_request_gen.post_request(url, data=payload)

        return (json.loads(r.text)["id"], r.text)


    def get_job_status(self, jobid):

        """Get the Job status.

        Get the status of a job with zje ID ::jobid:: . The status of the job has to be known and 
        can be seen via GUI in JOBS. The number after # in the title is the ID. The codes are:
        200 : Bulk Import request was successfully processed.
        401 : Authorisation failed, user doesn’t have the authority.
        500 : Internal server error, encountered server error while performing operations.

        Parameters
        ----------
        jobid : string or int
            ID of the job, which status has to be looked after.

        Returns
        -------
        string
            A string with the status code as mentioned above.
        """

        endpoint = '/'+ str(jobid)
        url = self.base_url + endpoint
        
        r = self.OS_request_gen.get_request(url)

        return r.text


    def job_report(self, jobid):

        """Download a job report.

        Get the status of a job with zje ID ::jobid:: . The status of the job has to be known and 
        can be seen via GUI in JOBS or in the corresponding schema with View Past Imports . The number 
        after # in the title is the ID. Generates a JSON-dict of the JOB containing the information
        which were uploaded and the additional fields OS_IMPORT_STATUS, OS_ERROR_MESSAGE.
        The Status and Error message can be extracted, when converted to a list with location [-2,-1],
        or when converted to a dict with keys ['OS_IMPORT_STATUS'] and ['OS_ERROR_MESSAGE'].

        Parameters
        ----------
        jobid : string or int
            ID of the job, which status has to be looked after.

        Returns
        -------
        string
            Job details as CSV like string separeted by ','
        """

        endpoint = '/' + str(jobid) + '/output'
        url = self.base_url + endpoint

        r = self.OS_request_gen.get_request(url)

        return r.text

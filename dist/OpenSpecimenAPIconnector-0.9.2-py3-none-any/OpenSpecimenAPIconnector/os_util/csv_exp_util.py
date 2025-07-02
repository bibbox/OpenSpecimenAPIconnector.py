#! /bin/python3

from ..os_core.csv_export import CSV_exporter
from ..os_core.jsons import Json_factory
import json
import io
import pandas
import time


class csv_exporter:

    """Handles the export of CSV files from open specimen for different entities like collection protocols, specimens etc etc.

    This class handles the CSV export of various different entities and creates CSV files of the requested entities like collection protocols, institutes etc.
    
    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. 
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Examples
    --------

    A code Examples, where the Institutes are handled is in the Jupyter-Notebook:

    $ jupyter notebook main.ipynb
    """
    def __init__(self):

        """Constructor of the Class csv_export

        Constructor of the class csv export holds the base parameters for the corresponding OpenSpecimen instance 

        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consists of two strings ( loginname , password)
        """

        self.export = CSV_exporter()
        self.json = Json_factory()


    def csv_export(self, objecttype, recordids=None, cpid=None, ppids=None,  entitytype=None, formname=None, 
                            specimenlabels=None, csv=False):

        """Export CSV for the given entity

        Export function for collection protocols 

        Parameters
        ----------
        objecttype: string 
            Identifying the general object to be exported.
            Permissible Values: institute, site, user, cpr, specimen, extensions, storageContainer
        recordids: list or string
            Comma seperated list of record ids for fetching selected entries by their identifier. (Sites, Institutes, Users and Containers) 
        cp_id: string 
            Collection protocol id of export target not neccesary for objects higher in the hierachy like institue or site.
            For all others it can be specified or set to -1 which means all data in the system.
        ppids: list or string
            List of comma seperated participant identifiers; String if its a singular participant to be exported
            Used in combination with specimen object type as a parameter
        entitytype: string
            Paramter defining the entity for data extraction (e.g. attached form at participant level)
            used with the extension object type
        formname: string
            Defines the form to be downloaded in context of the extension object type together with the specified entity 
        specimenlabels: list or string
            List of comma seperated specimen identifiers or str if its a singular specimen to be exported        
        Returns
        -------
        job: Pandas DataFrame or CSV binary File
            Returns the csv file as Pandas data frame or CSV binary string
        """
        

        data = self.json.create_csv_export_job(objecttype = objecttype, cpid = cpid,
                entitytype = entitytype, formname = formname)
        
        job_id = self.export.create_export_job(data = data)

        job = self.export.get_job_output(job_id = job_id)

        if csv:
           job = job.to_csv(index=False)

        return job

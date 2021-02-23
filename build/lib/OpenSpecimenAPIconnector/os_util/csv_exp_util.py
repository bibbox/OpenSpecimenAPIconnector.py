#! /bin/python3

from ..os_core.csv_export import CSV_exporter
from ..os_core.req_util import OS_request_gen
from ..os_core.jsons import Json_factory
import json
import io
import pandas
import time

## TODO Add all the other entities currently in export operations. Da sollten wir nochmal drüber sprechen

class csv_export:

    """Handles the export of CSV files from open specimen for different entities like collection protocols, specimens etc etc.

    This class handles the CSV export of various different entities and creates CSV files of the requested entities like collection protocols, institutes etc.
    Notes
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. 
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Example
    -------

    A code example, where the Institutes are handled is in the Jupyter-Notebook:

    $ jupyter notebook main.ipynb
    """
    def __init__(self, base_url, auth):

        """Constructor of the Class csv_export

        Constructor of the class csv export holds the base parameters for the corresponding OpenSpecimen instance 

        Parameters
        ----------
        base_url : string
            URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
            Consists of two strings ( loginname , password)
        """

        self.export = CSV_exporter(base_url = base_url, auth = auth)
        self.json = Json_factory()


    def cp_csv_export(self, objecttype, cpid, entitytype=None, formname=None):

        """Export CV for entity collection protocol

        Export function for collection protocols 

        Parameters
        ----------
        objecttype : None
            Not really clear what exactly this signifies right now
        cpid : string
            OpenSpecimen ID of the collection protocol to be exported
        entitype : None
            Not really clear what this is needed for, since the function exports Collection protocols
        formname : None
            Not really clear what exactly this signifies right now
        """

        data = self.json.create_cp_csv_export_job(objecttype = objecttype, cpid = cpid,
                entitytype = entitytype, formname = formname)
        
        job_id = self.export.create_export_job(data = data)

        job = self.export.get_job_output(job_id = job_id)

        return job

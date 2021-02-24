import json
import io
import requests
import json
import tempfile
import time

from ..os_core.csv_export import CSV_exporter
from ..os_core.jsons import Json_factory

class Export_OP():

    """Handles the API calls for Export_OP

    This class weaves together the base methods defined in OpenSpecimenAPIconnector.os_core.csv_export(*args)
    and provides the necessary JSON-formated data string, which is fetched in OpenSpecimenAPIconnector.os_core.Json_factory().
    Returns a pandas.DataFrame() containing the file information.    

    Notes
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes one can
    just pass the parameters via JSON-formatted string. The user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Currently, not all entity types are implemented. Further, Collection protocoll still does not support 
    CSV export. 

    Example
    -------

    Call export_file = export_file(**args) and provide a valid entity type. Additional 
    parameter can be passed to identify details about the entity to be exported (e.g collection protocol id) 
    See the calls in .export_file() and the Json_factory blueprints to
    get more information from the source code. 
    """

    def __init__(self):

        """Constructor of the Class Export_OP        

        Parameters
        ----------
        base_url : string
        URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
        Consists of two strings (loginname , password)
        """

        self.Json_fac = Json_factory()
        self.exporter = CSV_exporter()

    def export_file(self, entity=None, param=None):
        """Fetch the output 

        Parameters
        ----------
        entity : String 
            Representing the entity(collection protocol, institute, etc.) for identifying the necessary JSON data string
        param: String 
            Representing the various additional necessary parameters. E.g.: The Collection protocoll identifier 

        Returns
        -------
        export_file: pandas.DataFrame()
        A pandas data frame containing the CSV files information. You can easily recover the original file
        by using the pandas.to_csv() method.
        """        
        # temporary solution until template file handling is clear

        if entity == "institute":
            data = self.Json_fac.create_institue_export_job_json()
        elif entity == "user":
            data = self.Json_fac.create_user_export_job()
        elif entity == "site":
            data = self.Json_fac.create_site_export_job_json(record_ids=param)
        elif entity == "cp":
            objecttype = None
            entitytype = None
            formname = None
            data = self.json.create_cp_csv_export_job(objecttype = objecttype, cpid = param,
                entitytype = entitytype, formname = formname)
        elif entity == "cpr":
            data = self.Json_fac.create_cpr_export_job_json(cp_id=param)
        elif entity == "visit":
            data = self.Json_fac.create_visit_export_job_json(cp_id=param)
        elif entity == "specimen":
            data = self.Json_fac.create_specimen_export_job_json(cp_id=param)

        job_id = self.exporter.create_export_job(data)
        export_file = self.exporter.get_job_output(job_id)

        return export_file

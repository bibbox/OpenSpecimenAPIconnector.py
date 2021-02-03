import json
import io
import requests
import json
import tempfile
import time

from ..os_core.csv_export import CSV_exporter
from ..os_core.jsons import Json_factory
from ..os_core.req_util import OS_request_gen

class Export_OP():

    """Handles the API calls for Export_OP

    This class weaves together the base mehtods defined in OpenSpecimenAPIconnector.os_core.csv_export(*args)
    and providing the neccesary JSON-formated data string, which is fetched in OpenSpecimenAPIconnector.os_core.Json_factory().
    Returns a pandas.DataFrame() containing the file information.    

    Notes
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes one can
    just pass the parameters via JSON-formatted string. The user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Currently not all entitiy types are implemented. Further at the moment Collection protocoll still does not support 
    CSV export. 

    Example
    -------

    Call export_file = export_file(**args) and provide a valid entity type. In cases an additional 
    parameter param can be passed to the JSON generator definig various things like for example the
    target collection protocoll. See the calls in .export_file() and the Json_factory blueprints to
    get more information from the source code. 
    """

    def __init__(self, base_url, auth):

        """Constructor of the Class Export_OP        

        Parameters
        ----------
        base_url : string
        URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
        Consits of two strings (loginname , password)
        """

        self.base_url = base_url
        self.auth = auth
        self.Json_fac = Json_factory()
        self.exporter = CSV_exporter(self.base_url, self.auth)

    def export_file(self, entity=None, param=None):
        """Fetch the output 

        Parameters
        ----------
        entity : String representing the entity(collection protocoll) for identifying the necessary JSON data string
        param: String representing the various additional neccesary parameters. E.g.: The Collection protocoll identifier 

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
            data = self.Json_fac.create_cp_export_job_json(cp_id=param)
        elif entity == "cpr":
            data = self.Json_fac.create_cpr_export_job_json(cp_id=param)
        elif entity == "visit":
            data = self.Json_fac.create_visit_export_job_json(cp_id=param)
        elif entity == "specimen":
            data = self.Json_fac.create_specimen_export_job_json(cp_id=param)

        job_id = self.exporter.create_export_job(data)
        export_file = self.exporter.get_job_output(job_id)

        return export_file

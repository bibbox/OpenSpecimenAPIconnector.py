import pandas as pd
import zipfile
import json
import time
import io
from .req_util import OS_request_gen
from .. import config_manager

class CSV_exporter():
    """Handles the API calls for CSV file export

    This class provides methods to create and fetch the resutls of an internal OpenSpecimen export job.

    Note
    -----
    In order to use this and also the other classes, the user has to know OpenSpecimen. In the core classes one can
    just pass the parameters via JSON-formatted string. This means the user has to know the keywords.
    The API calls are documented in https://openspecimen.atlassian.net/wiki/spaces/CAT/pages/1116035/REST+APIs and 
    the calls refer to this site. More details can be seen in the documentation.

    Examples
    ---------
    Just call create export job with the correct data json String like
    my_id = CSV_exporter().create_export_job() or supply a job id to call
    my_pd_data_frame = CSV_exporter().get_job_output() to retrieve a pandas data frame
    """

    def __init__(self):
        
        """Constructor of the Class CSV_exporter

        Handles the basic API-calls for export-job fetching and creation. Either creates or fetches the outcome of an 
        specific export job

        Parameters
        ----------
        base_url : string
        URL to openspecimen, has the format: http(s)://<host>:<port>/openspecimen/rest/ng
        auth : tuple
        Consits of two strings (loginname , password)
        """
        self.base_url = config_manager.get_url()
        self.auth = config_manager.get_auth()
        self.OS_request_gen = OS_request_gen(self.auth)

    def create_export_job(self, data):

        """Create export job method with the entity (Collection Protocoll, Institutes etc.)
        encoded within the data JSON-formated-string.

        Parameters
        ----------
        data : JSON-formatted-string 
            Containing the information needed by the API. 
            See OpenSpecimenAPIconnector.os_util.Export_OP().export_file to find the JSON 
            blueprint methods in OpenSpecimenAPIconnector.os_core.Json_Factory().

        Returns
        -------
        job_id: String
            A string representing the id (integer number) assigned by the OpenSpecimen API
        """        

        job_endpoint = "/export-jobs/"
        job_url = self.base_url + job_endpoint
        done = False
        
        while not done:
            r = self.OS_request_gen.post_request(job_url, data)
            assert r.status_code == 200, "Error creating Job:\n {}".format(r.text)
            req_json = json.loads(r.text)
            if req_json["status"] == "IN_PROGRESS":
                print("Waiting for job to finish")
                time.sleep(5)
            else:
                done = True
        
        job_id = req_json["id"]
        
        return job_id

    def get_job_output(self, job_id):

        """Fetch the output 

        Parameters
        ----------
        job_id : 
            String representing the ID for identifying the output file

        Returns
        -------
        job_data: pandas.DataFrame()
            A pandas data frame containing the CSV files information. You can easily recover the original file
            by using the pandas.to_csv() method.
        """        
	

        job_out_endpoint = "/export-jobs/{}/output".format(job_id)
        job_out_url = self.base_url + job_out_endpoint

        r = self.OS_request_gen.get_request(job_out_url, stream=True)
        assert isinstance(r.content, bytes), "Error getting job Output either check job status or see attached error:\n {}".format(r.text)
        file = io.BytesIO(r.content)

        with zipfile.ZipFile(file, "r") as archive:
            job_data = archive.open("output.csv", "r")
            job_data = pd.read_csv(job_data)

        return job_data




import requests
import json
import pickle
import json
import requests
import uuid
import faker
from faker import Factory
import names
import random
import time
import datetime
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta

from request_factory import RequestFactory
from site_factory import SiteFactory
from file_factory import File_factory
from Forms import Form_factory
from jsons import Json_factory
from cp_factory import Cp_factory
from Part_fact import Participant_Fact
from query_factory import Query_Factory
from user_factory import User_factory
from specimen_factory import Specimen_Factory
from OS_BBMRI_merge import OS_BBMRI_merge

class OS_BBMRI_conn():

    def __init__(self, auth, base_url):

        self.base_url = base_url
        self.auth = auth
        
        # json templates
        self.Json_Fact = Json_factory()
        # files
        self.File_Fact = File_factory()
        # requests
        self.Req_Fact = RequestFactory(self.auth)
        # site operations
        self.Site_Fact = SiteFactory(self.base_url, self.Json_Fact, self.Req_Fact, self.File_Fact)
        # user operations
        self.User_Fact = User_factory(self.base_url, self.Json_Fact, self.Req_Fact, self.File_Fact, self.Site_Fact)
        # form operations
        self.Form_Fact = Form_factory(self.base_url, self.Json_Fact, self.Req_Fact, self.File_Fact)
        # CP operations
        self.CP_Fact = Cp_factory(self.base_url,  self.Json_Fact, self.Req_Fact, self.File_Fact, self.Site_Fact,
                                  self.Form_Fact)
        # Participant Operations
        self.Part_Fact = Participant_Fact(self.base_url, self.Json_Fact, self.Req_Fact, self.File_Fact, 
                                                 self.CP_Fact)
        # specimen operations
        self.Spec_Fact = Specimen_Factory(self.base_url, self.Json_Fact, self.Req_Fact, self.File_Fact, 
                                                 self.CP_Fact, self.Part_Fact)
        # Query operations
        self.Query_fact = Query_Factory(self.base_url, self.Json_Fact, self.Req_Fact, self.File_Fact, 
                                                 self.CP_Fact, self.Part_Fact, self.Spec_Fact)

        self.PS_BBMRI_merge = OS_BBMRI_merge(self.base_url, self.Json_Fact, self.Req_Fact, self.File_Fact,
                                                 self.CP_Fact, self.Part_Fact, self.Spec_Fact, self.Query_fact)
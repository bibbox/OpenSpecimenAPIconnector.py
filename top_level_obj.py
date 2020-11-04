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
import qrcode
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

class OS_BBMRI_conn():

    def __init__(self, auth, base_url):

        self.base_url = base_url
        self.auth = auth
        self.headers = {'content-type': "application/json", 'cache-control': "no-cache"}
        # json templates
        self.Json_Fact = Json_factory()
        # files
        self.File_Fact = File_factory()
        # requests
        self.Req_Fact = RequestFactory(self.headers, self.auth)
        # site operations
        self.Site_Fact = SiteFactory(self.base_url, self.Json_Fact, self.Req_Fact)
        # form operations
        self.Form_Fact = Form_factory(self.base_url, self.Json_Fact, self.Req_Fact)
        # CP operations
        self.CP_Fact = Cp_factory(self.base_url, self.Req_Fact, self.Site_Fact, self.Json_Fact, self.Form_Fact)
        # Participant Operations
        self.Participant_Fact = Participant_Fact(self.base_url, self.Json_Fact, self.Req_Fact, self.CP_Fact)




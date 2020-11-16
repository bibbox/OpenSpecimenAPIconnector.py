# imports to be cleaned later

import requests
import json
import pickle
import numpy as np
import json
import requests
import uuid
import faker
from faker import Factory
import names
import random
import time
import datetime
import pandas as pd
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import zipfile
import tempfile
from os_core.req_util import OS_request_gen
## TODO

    # additional imports; idealy these base methods do not need any cross importing of other modules
    # but this has to be checked on time of creation


# modules can be specified according to the underlying base
# these Base modules only contain

class CollectionProtocol():

    def __init__(self):


        self.OS_request_gen = OS_request_gen()
        ## define class members here
        # eg auth
        # eg headers
        #eg base url

        pass

    def cp_get_cps_json(self):
        endpoint = "/collection-protocols"
        url = self.base_url + endpoint
        r = self.Req_Fact.get_request(url)
        req_json = json.loads(r.text)

        return req_json

    # basic filtering is tolerable on core layer or not ?
    def cp_get_cp_ids(self, record_ids=None):

        endpoint = "/collection-protocols"
        url = self.base_url + endpoint
        r = self.Req_Fact.get_request(url)
        req_json = json.loads(r.text)
        ids = np.zeros(len(req_json))
        for i, item in enumerate(req_json):
            ids[i] = item["id"]

        return ids


    def class_method_module_post_entity_operation(self):
        pass

    def class_method_module_put_entity_operation(self):
        pass

    def class_method_module_delete_entity(self):
        pass
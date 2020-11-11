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
from request_factory import RequestFactory
from jsons import Json_factory
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import zipfile
import tempfile


## TODO

    # additional imports; idealy these base methods do not need any cross importing of other modules
    # but this has to be checked on time of creation


# modules can be specified according to the underlying base
# these Base modules only contain

class api_module_base_method():

    def __init__(self):

        ## define class members here
        # eg auth
        # eg headers
        #eg base url

        pass

    def class_method_module_get_entity(self):
        pass

    def class_method_module_post_entity_operation(self):
        pass

    def class_method_module_put_entity_operation(self):
        pass

    def class_method_module_delete_entity(self):
        pass
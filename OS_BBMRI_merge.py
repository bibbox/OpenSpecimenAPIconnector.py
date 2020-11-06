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
import pandas as pd
import numpy as np
import tempfile

from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta


class OS_BBMRI_merge():

    def __init__(self, base_url, Json_Fact, Req_Fact, File_Fact,
                CP_Fact, Part_Fact, Spec_Fact, Query_fact):

        self.base_url = base_url
        self.Json_Fact = Json_Fact
        self.Req_Fact = Req_Fact
        self.File_Fact = File_Fact
        self.CP_Fact = CP_Fact
        self.Part_Fact = Part_Fact
        self.Spec_Fact = Spec_Fact
        self.Query_fact = Query_fact

    def get_BBMRIbiobank_pandas(self):
        pass

    def get_BBMRICollection_pandas(self):
        pass

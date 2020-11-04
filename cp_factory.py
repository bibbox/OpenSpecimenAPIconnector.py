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

class Cp_factory():

    def __init__(self, base_url, Req_fact, Site_fact, Json_Fact, Form_Fact):

        self.base_url = base_url
        self.Req_Fact = Req_fact
        self.Json_Fact = Json_Fact
        self.Site_Fact = Site_fact
        self.Form_Fact = Form_Fact

    def create_CP(self, data):
        pass
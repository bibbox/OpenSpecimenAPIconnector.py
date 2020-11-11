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


class User_factory():

    def __init__(self, base_url, Json_Fact, Req_Fact, File_Fact, Site_Fact):

        self.base_url = base_url
        self.Json_Fact = Json_Fact
        self.Req_Fact = Req_Fact
        self.File_Fact = File_Fact
        self.Site_Fact = Site_Fact
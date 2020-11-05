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

class Participant_Fact():

    def __init__(self, base_url, Json_Fact, Req_Fact, File_Fact, CP_fact):

        self.base_url = base_url
        self.CP_Fact = CP_Fact
        self.Json_Fact = Json_Fact
        self.Req_Fact = Req_Fact
        self.File_Fact = File_Fact
        self.CP_Fact = CP_fact

    def participant_generator(self):
        pass

    def create_part(self):
        pass
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


def _strTimeProp(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))

def _randomDate(start, end, prop):
    return _strTimeProp(start, end, '%Y-%m-%d', prop)

def _random_participant():

    participant_inner = []
    participant_outer = []
    fake = Factory.create('de_AT')
    p = fake.profile()
    print(p['sex'])
    if p['sex'] == 'F':
        fn = fake.first_name_female()
        pr = fake.prefix_female()
        gender = "Female"
    else:
        fn = fake.first_name_male()
        pr = fake.prefix_male()
        gender = "Male"
    ln = fake.last_name()

    email = fn + "." + ln + "@" + fake.free_email_domain()
    regDate = _randomDate("1984-1-1", "2009-12-31", random.random())
    vdt = datetime.strptime(regDate, "%Y-%m-%d")
    earliestBirthDate = vdt - relativedelta(years=99)
    latesttBirthDate = vdt - relativedelta(years=30)
    birthdate = _randomDate(earliestBirthDate.strftime("%Y-%m-%d"), latesttBirthDate.strftime("%Y-%m-%d"),
                            random.random())

    p['birthdate'] = birthdate

    bdt = datetime.strptime(p['birthdate'], "%Y-%m-%d")
    age = relativedelta(date.today(), bdt.date()).years
    ageAtReg = relativedelta(datetime.strptime(regDate, "%Y-%m-%d").date(), bdt.date()).years

    # only patients above 25year get a title (name prefix)
    if (age < 25) or (random.random() < 0.75):
        pr = ""

    print(pr, fn, ln, email)
    participant_protocol_identifier = str(uuid.uuid4())

    participant_inner.append(fn)
    participant_inner.append(ln)
    participant_inner.append(birthdate)
    participant_inner.append(gender)
    participant_outer.append(regDate)
    participant_outer.append(participant_protocol_identifier)

    return participant_outer, participant_inner

class Participant_Fact():

    def __init__(self, base_url, Json_Fact, Req_Fact, File_Fact, CP_fact):

        self.base_url = base_url
        self.Json_Fact = Json_Fact
        self.Req_Fact = Req_Fact
        self.File_Fact = File_Fact
        self.CP_Fact = CP_fact

    def participant_generator(self, cp_id=None, num_part=0, data_arr=None):

        ##TODO make data array an pandas data frame. If there is more than two dimenisions, ther is than one
        ## Collection Protocoll to be filled with data entries, the keys should either be the Cp Id
        ## directly, or a value enabling to find it ---> check Api documentation for possible methods

        # this assertion is tepporary until the data_arr is implemented all values should be fetched from there
        assert cp_id is not None, "Please Specify the Collection Protocol by ID (see CP factory get methods)"

        # enable random generation of participants
        if data_arr is None:
            assert num_part != 0, "No Data Array given please enter number of random Participants to be generated"
            for num_par in range(num_part):
                self.create_part(cp_id)
        else:
            for entry in data_arr:
                self.create_part(entry)

    ##TODO This works but it is not the right way ... CSV Bulk import should be used ... also for export
    ## rewriting starting tommorow

    def create_part(self, cp_id=None, data=None):

        assert cp_id is not None, "Please Specify the Collection Protocol by ID (see CP factory get methods)"

        part_reg_endpoint = '/collection-protocol-registrations/'
        part_reg_url = self.base_url + part_reg_endpoint

        # get ramdom participant
        if data is None:
            data_outer, data_inner = _random_participant()
            part_json = self.Json_Fact.create_participant_json()
            i = 0
            k = 0
            for outer_key in part_json.keys():
                inner_key = "participant"
                if part_json[outer_key]:
                    if outer_key == inner_key:
                        for in_key in part_json[inner_key].keys():
                            if part_json[inner_key][in_key] and isinstance(part_json[inner_key][in_key], bool):
                                part_json[inner_key][in_key] = data_inner[k]
                                k += 1
                            elif in_key == "cpId":
                                part_json[inner_key][in_key] = cp_id
                    else:
                        part_json[outer_key] = data_outer[i]
                        i += 1
                elif outer_key == "cpId":
                    part_json[outer_key] = cp_id
                else:
                    continue
        else:
            part_json = self.Json_Fact.create_participant_json()
            for i, item in enumerate(part_json.keys()):
                part_json[item] = data[i]

        print(json.dumps(part_json, indent=4, sort_keys=True))
        r = self.Req_Fact.get_post_request(part_reg_url, json.dumps(part_json))
        print(json.loads(r.text))
        input()
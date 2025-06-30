#! /bin/python3
#### This is online for testing reasons only
from ..os_core.users import users
from ..os_core.specimen import specimen
from ..os_core.mandatory import mark_mandatory
from ..os_core.csv_bulk import csv_bulk
from ..os_core.visit import visit
from ..os_core.participant import participant
from ..os_core.collection_protocol import collection_protocol
from ..os_core.collection_protocol_registration import collection_protocol_registration
from ..os_core.collection_protocol_event import collection_protocol_event
from ..os_core.query import query
from ..os_core.jsons import Json_factory

from .cpevent_util import cpevent_util
from .bulk_operations import bulk_operations
from .query_util import query_util
from .cpr_util import cpr_util
from .visit_util import visit_util
from.csv_exp_util import csv_exporter
import json
import pandas
import random
import numpy as np
from datetime import datetime

class aggregator():

    def __init__(self):
        
        self.jsons = Json_factory()
        self.schemes = ['cp', 'specimen', 'cpr', 'user', 'userRoles', 'site', 'shipment', 
              'institute', 'dpRequirement', 'distributionProtocol', 'distributionOrder', 
              'storageContainer', 'storagecontainerType', 'containerShipment', 'cpe',
              'masterSpecimen', 'participant', 'sr', 'visit', 'specimenAliquot', 
              'specimenDerivative', 'specimenDisposal', 'consent']
        self.now = datetime.now()
        

    def extract_age_fields(self, cp_csv, cp_data, cp_id):

        age_array = []
        for date in cp_csv["Date Of Birth"]:
            age_array.append(float(self.now.year) - float(date.split("-")[-1]))
        age_array = np.array(age_array)
        print("Age high: ",np.max(age_array))
        print("Age low: ", np.min(age_array))
        print("Age mean: ", age_array.mean())
        for i, item in enumerate(cp_data["extensionDetail"]["attrs"]):
            if cp_data["extensionDetail"]["attrs"][i]["name"] == "AgeLow":
                cp_data["extensionDetail"]["attrs"][i]["value"] = str(int(np.min(age_array)))
                cp_data["extensionDetail"]["attrs"][i]["displayValue"] = str(int(np.min(age_array)))
            elif cp_data["extensionDetail"]["attrs"][i]["name"] == "AgeHigh":
                cp_data["extensionDetail"]["attrs"][i]["value"] = str(int(np.max(age_array)))
                cp_data["extensionDetail"]["attrs"][i]["displayValue"] = str(int(np.max(age_array)))
        return cp_data

    def run_aggregation(self, sel_schema, ids=None):
        """
        General purpose aggreation for fields in attached forms 
        under developement. 
        TODO: See which entities are stored with extension detail
        -
        and where to use''--_'
        """
        cp_tools = collection_protocol()
        csv_export =  csv_exporter()
        if sel_schema == "cpr":
            for i, cp_id in enumerate(ids):
                up_cp_data = self.extract_age_fields(csv_export.csv_export(sel_schema, cpid=cp_id), 
                                                    cp_tools.get_collection_protocol(cp_id), cp_id)
                r = cp_tools.update_collection_protocol(str(cp_id), json.dumps(up_cp_data)) 
            if r.get("extensionDetail"):
                print("Aggregation sucessfull")
        else:
            print("In this Demo the only fields to be aggregated are ", 
            "attached to Collection Protocols")
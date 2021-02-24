#! /bin/python3
#### This is online for testing reasons only
from ..os_core.users import users
from ..os_core.specimen import specimen
from ..os_core.mandatory import mark_mandatory
from ..os_core.csv_bulk import csv_bulk
from ..os_core.visit import visit
from ..os_core.participant import participant
from ..os_core.collection_protocoll import collection_protocol
from ..os_core.collection_protocol_registration import collection_protocol_registration
from ..os_core.collection_protocol_event import collection_protocol_event
from ..os_core.query import query
from ..os_core.jsons import Json_factory

from .cpevent_util import cpevent_util
from .bulk_operations import bulk_operations
from .query_util import query_util
from .cpr_util import cpr_util
from .visit_util import visit_util
import json
import pandas
import random
import numpy as np

class aggregator():

    def __init__(self):
        
        self.jsons = Json_factory()

    def extract_age_fields(self):
        pass

    def run_aggregation(self, cp_ids):
        """
        General purpose aggreation for fields in attached forms 
        under developement. 
        TODO: See which entities are stored with extension detail
        -
        and where to use''--_'
        """

        cp_tools = collection_protocol(self.base_url, self.auth)
        csv_files= csv_bulk(self.base_url, self.auth)
        bulk_op= bulk_operations(self.base_url, self.auth)
        csv_export = Export_OP(self.base_url, self.auth)
        
        export_cps_csv = []
        export_cps_def = []
        if len(cp_ids) != 1:
            for cp_id in cp_ids:
                export_cps_csv.append(csv_export_7_2.export_file(sel_schema, cp_id))
                export_cps_def.append(cp_tools_target.get_cp_def(cp_id))
        else:
            export = csv_export.export_file(sel_schema, cp_id_target)
            cp_def = cp_tools.get_cp_def(cp_id)

        if export_cps_csv:
            for i, cp in enumerate(export_cps_csv):
                age_array = []
                for date in cp["Date Of Birth"]:
                    age_array.append(2020 - float(date.split("-")[-1]))
                age_array = np.array(age_array)
                cp_data = export_cps_def[i]
                for j, item in enumerate(cp_data["extensionDetail"]["attrs"]):
                    if cp_data["extensionDetail"]["attrs"][j]["name"] == "AgeLow":
                        cp_data["extensionDetail"]["attrs"][j]["value"] = str(int(np.min(age_array)))
                        cp_data["extensionDetail"]["attrs"][j]["displayValue"] = str(np.min(age_array))
                    elif cp_data["extensionDetail"]["attrs"][j]["name"] == "AgeHigh":
                        cp_data["extensionDetail"]["attrs"][j]["value"] = str(int(np.max(age_array)))
                        cp_data["extensionDetail"]["attrs"][j]["displayValue"] = str(np.max(age_array))
            
        # in case of only one target:
        else: 
            age_array = []
            # crude example of age calculation
            for item in export["Date Of Birth"]:
                age_array.append(2020 - float(item.split("-")[-1]))

            age_array = np.array(age_array)
            #rewrite our custom Aggregtion fields (there is a better way to do this)
            for i, item in enumerate(cp_target["extensionDetail"]["attrs"]):

                if cp_def["extensionDetail"]["attrs"][i]["name"] == "AgeLow":
                    cp_def["extensionDetail"]["attrs"][i]["value"] = str(int(np.min(age_array)))
                    cp_def["extensionDetail"]["attrs"][i]["displayValue"] = str(np.min(age_array))
                elif cp_def["extensionDetail"]["attrs"][i]["name"] == "AgeHigh":
                    cp_def["extensionDetail"]["attrs"][i]["value"] = str(int(np.max(age_array)))
                    cp_def["extensionDetail"]["attrs"][i]["displayValue"] = str(np.max(age_array))
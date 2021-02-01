#! /bin/python3


'''
    Road to official version:
    ::::::TODO::::::
    - Extend TODO-List
    - Person_Extensions in openspecimen
    - Some_fields in Collections have to be loaded separatly
    - Header should be borderless, and non-bold
    - Format of cells
    - use OpenSpecimenBBMRIconnector.py pip package instead
    - Bring it in a JUPYTER NoteBook
    - Extend Dokumentation, or maybe via JUPYTER NoteBook
    -- optional: functionize it?!?

'''
from ..mg_core.mappings import bbmri_mapping 
from ..os_core.site import sites
from ..os_core.jsons import Json_factory
from ..os_core.users import users
from ..os_core.collection_protocol_registration import collection_protocol_registration
from ..os_core.collection_protocoll import collection_protocol

import json
import pandas as pd
import xlsxwriter
from openpyxl import load_workbook


class ExecuteMapping:

    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth
    
    def run_mapping(self):
        #sheetnames:
        bb_sheet = "eu_bbmri_eric_biobanks"
        per_sheet = "eu_bbmri_eric_persons"
        cp_sheet = "eu_bbmri_eric_collections"

        #file_output
        output_file = "test.xlsx"

        # Design header for writing to xlsx
        # here we create a format object for header. 

        # Load headers of BBMRI_ERIC Directory
        template_file_name="empty_eric_duo.xlsx"
        bbmri_file = pd.read_excel(template_file_name, sheet_name = None)

        #initialize Users,CollectionProtocols, Sites
        protocols = collection_protocol(base_url = self.base_url, auth = self.auth)
        user = users(base_url=self.base_url, auth=self.auth)
        site = sites(base_url=self.base_url, auth=self.auth)

        #load Openspecimen Collection Protocols
        cps = protocols.get_all_collection_protocols()

        # get all CP-IDs
        collection_protocol_ids=[]
        for cp in cps:
            collection_protocol_ids.append(cp['id'])
        collection_protocol_ids = collection_protocol_ids[1:] #One CP is empty

        index_=0
        #writing all Collection protocols to the bbmri-dict
        for cp_id, index_ in collection_protocol_ids:
            cp = protocols.get_collection_protocol(cpid = str(cp_id))

            #extract User
            OS_user_id = cp['principalInvestigator']['id']
        OS_user = user.get_user(userId = OS_user_id)

        #extractSite
        OS_site_name = cp['cpSites'][0]['siteName']
        OS_sites = site.get_all_sites()
        for i in range(len(OS_sites)):
            if OS_sites[i]['name']==OS_site_name:
                OS_site_id=OS_sites[i]['id']
        OS_site=site.get_site(siteid = OS_site_id)


        #check if user exists
        #if bbmri_file[per_sheet]['id'].values()
        #  fill the bbmri_persons_dict
        for key in bbmri_file[per_sheet].keys():
            
            # fileds which can't generated by OpenSpecimen for now
            if key in persons_extensions.keys():
                bbmri_file[per_sheet].at[index_, key]=persons_extensions[key]
                
            # standard fields in OpenSpecimen which are named differently to BBMRI
            elif key in person_map.keys():
                bbmri_file[per_sheet][key]=OS_user[person_map[key]]

        # fill the Biobank fields
        attrs = OS_site['extensionDetail']['attrs']     #extract BBMRI-Extension-Details
        # ExtensionFields are called differently in Openspecimen #TODO-for MIABIS Plugin
        for attr in attrs:
            key_string=attr["caption"]=attr["caption"].lower().replace(" ","_")
            value_string = ''
            if isinstance(attr['value'],list):
                for i in range(len(attr['value'])):
                    value_string+=attr['value'][i]+', '
                value_string=value_string[0:-2]
            else:
                value_string=attr['value'] 
            
            # append the OS_Biobank dict with the extensiondetails, such that there are lesser if statements
            OS_site[key_string]=value_string

        for key in bbmri_file[bb_sheet].keys():
            # The Persons ID is stored in the BIobank contact,
            if key =='contact':
                bbmri_file[per_sheet].at[index_,'id']=OS_site[key]

            # fileds which can't generated by OpenSpecimen for now
            if key in biobank_extensions.keys():
                bbmri_file[bb_sheet].at[index_,key]=biobank_extensions[key]

            # standard fields in OpenSpecimen which are named differently to BBMRI
            elif key in biobank_map.keys():
                bbmri_file[bb_sheet].at[index_,key]=OS_site[biobank_map[key]]

            # fields which are named same to BBMRI
            elif key in OS_site.keys():  
                bbmri_file[bb_sheet].at[index_,key]=OS_site[key]

        #fill the BBBMRI Biobank dict
        attrs = cp['extensionDetail']['attrs']     #extract BBMRI-Extension-Details
        # ExtensionFields are called differently in Openspecimen #TODO-for MIABIS Plugin
        for attr in attrs:
            key_string = attr['caption'].lower().replace(' ','_')
            value_string = ''
            if isinstance(attr['value'],list):
                for i in range(len(attr['value'])):
                    value_string += attr['value'][i] + ', '
                value_string = value_string[0:-2]
            else:
                value_string = attr['value']
            
            # append the OS_Biobank dict with the extensiondetails, such that there are lesser if statements
            cp[key_string] = value_string

        ##fill json-dict, with OpenSpecimen standard fields
        for key in bbmri_file[cp_sheet]:
            if key in collection_map.keys():
                bbmri_file[cp_sheet].at[index_,key]=cp[collection_map[key]]
            elif key in cp.keys():
                bbmri_file[cp_sheet].at[index_,key]=cp[key]

        #Write excel-file
        with pd.ExcelWriter(output_file,engine='openpyxl') as writer:
            for sheet_name in bbmri_file.keys():
                df = bbmri_file[sheet_name]
                df.to_excel(writer, sheet_name=sheet_name,index=False)


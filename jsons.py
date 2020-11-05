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

class Json_factory():

    def __init__(self):
        pass

    # creation jsons:
    # participant
    def create_participant_json(self, fn, ln, birthdate, gender, cp_id, reg_date, pp_id, death_date=None,
                             vital_status="Unknown", pmis=None, eth=None, activity="Active", phi=True,
                             registeredCps=None, cpId=-1, reqRegInfo=False, forceDelete=False):

        '''
        :param fn:
        :param ln:
        :param birthdate:
        :param gender:
        :param cp_id:
        :param reg_date:
        :param pp_id:
        :param death_date:
        :param vital_status:
        :param pmis:
        :param eth:
        :param activity:
        :param phi:
        :param registeredCps:
        :param cpId:
        :param reqRegInfo:
        :param forceDelete:
        :return:
        '''

        if registeredCps is None:
            registeredCps = []

        participantRegistration = {
            "participant": {
                "firstName": fn,
                "lastName": ln,
                "middleName": "",
                "birthDate": birthdate,
                "deathDate": death_date,
                "gender": gender,
                "races": [],
                "vitalStatus": vital_status,
                "pmis": pmis,
                "ethnicities": eth,
                "activityStatus": activity,
                "phiAccess": phi,
                "registeredCps": registeredCps,
                "cpId": cpId,
                "reqRegInfo": reqRegInfo,
                "forceDelete": forceDelete
            },
            "cpId": cp_id,
            "registrationDate": reg_date,
            "ppid": pp_id
        }

        return json.dumps(participantRegistration)

    # Collection Protocoll

    def create_CP_json(self, short_title, title, pi_mail, time_start, time_end, sites, man_id=False, coords=None,
                           consentsWaived=False,eth_cons_id=None, part_no=None, desc_url=None, visitNameFmt=None,
                           man_visit_name=False, man_spec_label=True, aliquots_in_same=None, activity="Active"):

        '''
        :param short_title:
        :param title:
        :param pi_mail:
        :param sites:
        :param man_id:
        :param coords:
        :param consentsWaived:
        :param eth_cons_id:
        :param part_no:
        :param desc_url:
        :param visitNameFmt:
        :param man_visit_name:
        :param man_spec_label:
        :param aliquots_in_same:
        :param activity:
        :return:
        '''

        site_arr = []
        for item in sites:
            site_arr.append(
                {
                    "siteName": item[0],
                    "code": item[1]
                }
            )

        CP_reg = {
            "shortTitle": short_title,
            "title": title,
            "code": None,
            "principalInvestigator":
                {
                    "loginName": pi_mail,
                    "domain": "openspecimen"
                },
            "startDate": time_start,
            "endDate": time_end,
            "ppidFmt": "DWP%05d",
            "manualPpidEnabled": man_id,
            "coordinators": coords,
            "cpSites": site_arr,
            "consentsWaived": consentsWaived,
            "irbId": eth_cons_id,
            "anticipatedParticipantsCount": part_no,
            "descriptionUrl": desc_url,
            "specimenLabelFmt": "%PPI%.%SP_TYPE%.%SYS_UID%",
            "derivativeLabelFmt": "%PPI%.%SP_TYPE%.%SYS_UID%",
            "aliquotLabelFmt": "%PSPEC_LABEL%.%PSPEC_UID%",
            "visitNameFmt": visitNameFmt,
            "manualVisitNameEnabled": man_visit_name,
            "manualSpecLabelEnabled": man_spec_label,
            "aliquotsInSameContainer": aliquots_in_same,
            "activityStatus": activity
        }

        return json.dumps(CP_reg)

    # Collection Protocol event

    def create_cp_event_json(self):
        pass

    def create_spec_json(self, lineage, visit_id, av_qty, user, visitDate, init_qty, spec_class, spec_type, anat_site, 
                         stor_loc=None, status="Collected", cont=None, proced=None, qual="Acceptable", concent=None,  
                         path=None, laterality=None):
        '''
        :param lineage:
        :param visit_id:
        :param av_qty:
        :param user:
        :param visitDate:
        :param init_qty:
        :param spec_class:
        :param spec_type:
        :param anat_site:
        :param stor_loc:
        :param status:
        :param cont:
        :param proced:
        :param qual:
        :param concent:
        :param path:
        :param laterality:
        :return:
        '''

        spec = {
            "lineage": lineage,
            "visitId": visit_id,
            "status": status,
            "availableQty": av_qty,
            "storageLocation": stor_loc,
            "collectionEvent":
                {
                    "user": user,
                    "time": visitDate,
                    "container": cont,
                    "procedure": proced,
                },
            "receivedEvent":
                {
                    "user": user,
                    "time": visitDate,
                    "receivedQuality": qual
                },
            "initialQty": init_qty,
            "concentration": concent,
            "label": label,
            "specimenClass": spec_class,
            "type": spec_type,
            "pathology": path,
            "anatomicSite": anat_site,
            "laterality": laterality
            }

        return json.dumps(spec)

    # Export Jsons

    # Export Sites

    def create_site_export_job_json(self, record_ids=None):

        site_json = {"objectType": "site", "recordIds": record_ids}

        return json.dumps(site_json)

    ##TODO

    # Import collection protocols
    
    def create_site_import_job_json(self, record_ids=None):

        site_json = {"objectType": "site", "recordIds": record_ids}

        return json.dumps(site_json)

    
    def create_cp_import_job_json(self, record_ids=None):

        site_json = {"objectType": "site", "recordIds": record_ids}

        return json.dumps(site_json)
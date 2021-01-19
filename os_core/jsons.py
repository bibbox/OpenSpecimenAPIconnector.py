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

class Json_factory():

    def __init__(self):
        pass

    ##TODO Decide upon way of json creation/storage for OS operations, the current idea is to set mandatory values to
    ## boolean true by default. than a random generator can create the values in fixed order and they can be set
    ## according to the boolean. Even better would be the restriction to use pandas data frames directly and create the
    ## json once data entry is done. Another important question is how to deal with custom value fields in various cases.
    ## Further, where possible, the csv import option should be used and json creation should be left to the numerous
    ## methods within Open Specimen
    ## first approach to be overhauled

    # creation jsons:
    # participant
    def create_participant_json(self, fn=True, ln=True, birthdate=True, gender=True, cp_id=None, reg_date=True,
                            pp_id=True, death_date=None, vital_status="Unknown", pmis=None, eth=None,
                            activity="Active", phi="true", registeredCps=None, cpId=-1, reqRegInfo=False,
                            forceDelete=False):

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

        return participantRegistration

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

    def create_spec_json(self, lineage, visit_id, av_qty, user, visitDate, init_qty, spec_class, spec_type, anat_site, label, 
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

    def create_cpr_export_job_json(self, cp_id=None):

        part_json = {"objectType": "cpr", "params": {"cpId": cp_id}}

        return json.dumps(part_json)

    ##TODO

    # Import collection protocols
    
    def create_site_import_job_json(self, record_ids=None):

        site_json = {"objectType": "site", "recordIds": record_ids}

        return json.dumps(site_json)
    
#   Create  Any AQL Query
    def create_aql(self, cpid, aql, rowmode='OFF', coloumexpr='true', isodate='true'):

        params = {
            "cpId" : cpid,
            "aql" : aql,
            "wideRowMode" : rowmode,
            "outputColoumnExprs" : coloumexpr,
            "outputIsoDateTime" : isodate
        }

        return json.dumps(params)

# Execute Saved Query
    def execute_query(self, start, results, drivingform="Participant", rowmode="OFF"):

        params= {
            "drivingForm": drivingform,
            "wideRowMode": rowmode,
            "startAt": start,
            "maxResults":results
        }

        return json.dumps(params)

    def create_cpr_part_import_job(self, schemaname=None, operation=None, fileid=None,
                                   dateformat=None, timeformat=None):

        part_cpr_json = {"objectType": schemaname,
                    "importType": operation,
                    "inputFileId": fileid,
                    "dateFormat":dateformat,
                    "timeFormat":timeformat
                    }

        return json.dumps(part_cpr_json)

    def get_registrations(self, cpid=None, registrationdate=None, ppid=None, name=None, birthdate=None, uid=None, specimen=None,
                                    includestats=None, startat=None,maxresults=None):

        params = {
            "cpId": cpid,
            "registrationDate": registrationdate,
            "ppid": ppid,
            "name": name,
            "dob": birthdate,
            "uid": uid,
            "specimen": specimen,
            "includeStats": includestats,
            "startAt": startat,
            "maxResults": maxresults
        }

        return json.dumps(params)

    def create_cp_event_json(self, label, point, cp, site, diagnosis, status, activity, unit, code=None):

        params = {
            "eventLabel": label,
            "clinicalDiagnosis": diagnosis,
            "clinicalStatus": status,
            "collectionProtocol": cp,
            "defaultSite": site,
            "activityStatus": activity,
            "eventPoint": point,
            "eventPointUnit": unit
        }

        return json.dumps(params)

    def add_visit_json(self,cprid, name, site,eventid=None,eventlabel=None,ppid=None, cptitle=None, cpshorttitle=None,
                        diagnosis=None, clinicalstatus=None, activity=None, visitstatus="COMPLETE", missedreason=None,
                        missedby=None, comments=None,pathologynumber=None,cohort=None, visitdate=None, cpid=None):

        params = {
            "cprId": cprid,
            "eventId": eventid,
            "eventLabel": eventlabel,
            "ppid": ppid,
            "cpTitle": cptitle,
            "cpShortTitle":cpshorttitle,
            "cpId": cpid,
            "name": name,
            "clinicalDiagnoses": diagnosis,
            "clinicalStatus": clinicalstatus,
            "activityStatus": activity,
            "site": site,
            "status": visitstatus,
            "missedReason": missedreason,
            "missedBy": missedby,
            "comments": comments,
            "surgicalPathologyNumber": pathologynumber,
            "cohort": cohort,
            "visitDate": visitdate
        }
        
        return json.dumps(params)

    def storage_location_json(self, id=None, name=None, xpos=None, ypos=None):

        params = {
            "id": id,
            "name": name,
            "positionX": xpos,
            "positionY": ypos
        }

        return json.dumps(params)

    def create_cp_csv_export_job(self, objecttype, cpid, entitytype=None, formname=None):

        data = {
            "objectType": objecttype,
            "params":{
                "entityType": entitytype,
                "formName": formname,
                "cpId": cpid
            }
        }

        return json.dumps(data)

    def site_search_url_gen(self, sitename=None, institutename=None, maxresults=100):

        url_string = '/?'

        if sitename!=None:
            if isinstance(sitename,list):
                for name in sitename:
                    url_string += 'name=' + str(name).replace(' ', '+') + '&'
            else:
                url_string += 'name=' + str(sitename).replace(' ', '+') + '&'

        if institutename!=None:
            if isinstance(institutename,list):
                for name in institutename:
                    url_string += 'institute=' + str(name).replace(' ','+') + '&'
            else:
                url_string += 'institute=' + str(institutename).replace(' ','+') + '&'
        
        url_string += 'maxResults=' + str(maxresults)

        return url_string
    


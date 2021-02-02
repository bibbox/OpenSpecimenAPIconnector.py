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
    def create_participant_json(self, regdate, id = None, cpid = None, cptitle = None, cpshorttile = None, ppid = None,
                                firstname = None, middlename = None, lastname = None, uid = None, birthdate = None, vitalstatus = None,
                                deathdate = None, gender = None, race = None, ethnicities = None, sexgenotype = None, pmis = None,
                                mrn = None, sitename = None, empi = None):

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


        participantRegistration = {
            "participant": {
                "firstName": firstname,
                "middleName": middlename,                
                "lastName": lastname,
                "uid" : uid
                "birthDate": birthdate,
                "vitalStatus": vitalstatus,
                "deathDate": deathdate,
                "gender": gender,
                "race": race,
                "ethnicities": eth,
                "sexGenotype":sexgenotype,
                "pmis": pmis,
                "mrn": mrn,
                "siteName": sitename,
                "empi": empi
            },
            "cpId": cpid,
            "cpTitle": cpTitle,
            "cpShorttitle":cpshorttitle, 
            "registrationDate": regdate,
            "ppid": ppid
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

    def create_specimen_json(self, label = None, specimenclass = None, specimentype = None , pathology = None, anatomic = None,
                            laterality = None, initqty = None, avaqty = None, visitid = None, userid = None, colltime = None,
                            rectime = None, recqlt = None, lineage = 'New', status = 'Collected', storloc = None, concetration = None, 
                            biohazard = None, comments = None,  collproc=None, conttype=None, extension =None):
        

        spec = {
            "label": label,
            "specimenClass": specimenclass,
            "type": specimentype,
            "pathology": pathology,
            "anatomicSite": anatomic,
            "laterality": laterality,
            "initialQty": initqty,
            "availableQty": avaqty,
            "visitId": visitid,
            "status": status,
            "storageLocation": {storloc},
            "concetration": concentration,
            "biohazard": biohazard,
            "comments": comments,
            "collevent": {
                "user": {"id": user},
                    "time": colltime,
                    "container": conttype,
                    "procedure": procedure
                     },
            "receivedEvent":{
                "user":{"id": userid},
                "time": rectime,
                "receivedQuality": recqlt
            },
            "extensionDetail": {extension}
            }

        return json.dumps(spec)

    def create_extension(self, attrsmap, extensiondict, useudn="false"):

        data = {
            "useUdn": useudn,
            "attryMap": attrsmap,
            "value": extensiondict
        }

        return json.dumps(data)
    
   # Export Institute CSV
    def create_institue_export_job_json(self):

        institute_json = {"objectType": "institute"}
        return json.dumps(institute_json)


    # Export Sites CSV
    def create_site_export_job_json(self, record_ids=None):

        site_json = {"objectType": "site"}
        return json.dumps(site_json)


    # Export User CSV
    def create_user_export_job(self):

        user_json = {"objectType": "user"}
        return json.dumps(user_json)


    # Export CP Registaration CSV
    def create_cp_export_job_json(self, cp_id=None):

        cp_json = {"objectType": "cp", "params": {"cpId": cp_id}}
        return json.dumps(cp_json)


    # Export CP Registaration CSV
    def create_cpr_export_job_json(self, cp_id=None):

        cpr_json = {"objectType": "cpr", "params": {"cpId": cp_id}}
        return json.dumps(cpr_json)


    # Export Vist CSV
    def create_visit_export_job_json(self, cp_id=None):

        visit_json = {"objectType": "specimen", "params": {"cpId": cp_id}}
        return json.dumps(visit_json)


    # Export Specimen CSV
    def create_specimen_export_job_json(self, cp_id=None):

        specimen_json = {"objectType": "specimen", "params": {"cpId": cp_id}}
        return json.dumps(specimen_json) 


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
    def create_aql(self, cpid, aql, rowmode='OFF', columnexpr='true', isodate='true'):

        params = {
            "cpId" : cpid,
            "aql" : aql,
            "wideRowMode" : rowmode,
            "outputColoumnExprs" : columnexpr,
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

    def create_cp_event_json(self, label = None, point = None, cp = None, site = None, diagnosis = None, 
                            status = None, activity = None, unit = None, code=None):

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

    def merge_cps(self, src_cp, trg_cp):
        
        data = {
            "srcCpShortTitle": src_cp,
            "tgtCpShortTitle": trg_cp
        }

        return json.dumps(data)

    def create_institute(self, institutename):

        data = {
            "name": institutename
        }

        return json.dumps(data)

    def get_participants(self, lastname = None, uid = None, birthdate = None, pmi = None, empi = None, reqreginfo = None):

        data ={
            "lastName" : lastname,
            "pmi":{
                "mrn" : str(pmi[0]),
                "siteName" : pmi[1]
            },
            "birthDate" : birthdate,
            "uid" : uid,
            "empi" : empi,
            "reqRegInfo" : reqreginfo
        }
        
        return json.dumps(data)


    def create_site(self, name, institutename, type_, coordinators = None, address = None):

        params = {
            "name": name,
            "instituteName": institutename,
            "coordinators" : coordinators,
            "type": type_,
            "address": address
        }

        return json.dumps(data)
        

    



